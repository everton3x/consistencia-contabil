"""
Executa os testes
"""

import argparse
from datetime import datetime
import pandas as pd
import logging
import sys
from os import path
from charset_normalizer import from_path
from io import StringIO
from jinja2 import Environment, FileSystemLoader

#Configuração do logger
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ],
    format='%(asctime)s %(levelname)s %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S'
)

logging.info('Carregando as configurações...')
# Configurações
entidades = {
    0: {
        'orgaos': (2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
        'nome': 'Prefeitura',
        #'rules': ('agnostic.csv', 'pm.csv')
        'rules': ('agnostic.csv',)
    },
    1: {
        'orgaos': (12,),
        'nome': 'FPSM',
        'rules': ('agnostic.csv', 'rpps.csv')
    },
    2: {
        'orgaos': (1,),
        'nome': 'Câmara de Vereadores',
        'rules': ('agnostic.csv', 'cm.csv')
    },
    9: {
        'orgaos': (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
        'nome': 'Município (Agregado)',
        'rules': ('mun.csv',)
    }
}
rulesdir = r'rules'
padcsvdir = r'C:\Users\Everton\OneDrive\Prefeitura\PAD'
outputdir = r'output'
templatesdir = r'templates'

# Parse command line arguments
logging.info('Identificando argumentos da linha de comando...')
parser = argparse.ArgumentParser(
    prog='run-test',
    description='Executa os testes de consistência contábil',
)
parser.add_argument('profile', nargs=1, type=int, choices=entidades.keys(), help='Número da entidade', metavar='profile')
parser.add_argument('mes', nargs=1, type=int, choices=range(1, 13, 1), help='Número do mês para processar', metavar='mês')
parser.add_argument('ano', nargs=1, type=int, help='Ano para processar', metavar='ano')
profile = parser.parse_args().profile[0]
mes = str(parser.parse_args().mes[0]).rjust(2, '0')
ano = str(parser.parse_args().ano[0])

# Seleciona o profile
logging.info('Profile selecionado:')
profile = entidades[profile]
logging.debug(profile)


# Carrega as rules
logging.info('Carregando as regras de consistência...')
rules = pd.DataFrame(columns=['rule', 'side', 'dataset', 'field', 'filter', 'subtract'])
for rulefile in profile['rules']:
    csv = StringIO(str(from_path(path.join('.', rulesdir, rulefile)).best()))
    ruledf = pd.read_csv(csv, sep=';')
    rules = pd.concat([rules, ruledf], join='outer', ignore_index=True)
rules.fillna(False, axis='columns', inplace=True)
rules['left_val'] = 0.0
rules['right_val'] = 0.0
rules['diff'] = None

logging.info('Carregando o conjunto de dados...')
# Carrega e prepara os csv do PAD
csvdir = path.join(padcsvdir, ano+'-'+mes)
datasets = {}

# bal_ver
logging.debug('...BAL_VER.txt')
dados = StringIO(str(from_path(path.join(csvdir, 'bal_ver.csv')).best()))
df = pd.read_csv(dados, sep=';', parse_dates=True, infer_datetime_format=True, decimal=',', thousands='.')
datasets['balver'] = df[
    (df['orgao'].isin(profile['orgaos']))
    & (df['escrituracao'] == 'S')
].copy()

# Cria a lista de nomes de regras
logging.info('Montando lista de regras...')
rulelist = rules['rule'].unique()

# Cria o df de resultados
logging.info('Preparando armazém de resultados...')
results = pd.DataFrame(columns=['rule', 'side', 'dataset', 'field', 'filter', 'minus', 'left_val', 'right_val', 'diff'])
summary = pd.DataFrame(columns=['rule', 'left', 'right', 'diff'])

# Processa as rules
logging.info('Processando regras...')
for rulename in rulelist:
    rulespec = rules[rules['rule'] == rulename]
    logging.debug(f'...{rulename}')
    # Valor esquerdo
    lrule = rulespec[rulespec['side'] == 'left']
    lval = 0.0
    for key, item in lrule.iterrows():
        dataset = item['dataset']
        field = item['field']
        filter = item['filter']
        minus = item['minus']
        subset = datasets[dataset].query(filter)
        val = subset[field].sum()
        if minus is not False:
            val = val * -1
        val = round(val, 2)
        rules.at[key, 'left_val'] = val
        lval += val
        # Valor direito
        rrule = rulespec[rulespec['side'] == 'right']
        rval = 0.0
        for key, item in rrule.iterrows():
            dataset = item['dataset']
            field = item['field']
            filter = item['filter']
            minus = item['minus']
            subset = datasets[dataset].query(filter)
            val = subset[field].sum()
            if minus is not False:
                val = val * -1
            val = round(val, 2)
            rules.at[key, 'right_val'] = val
            rval += val
    diff = round(lval - rval, 2)
    total = pd.DataFrame({
        'rule': rulename,
        'side': 'total',
        'dataset': None,
        'field': None,
        'filter': None,
        'minus': None,
        'left_val': round(lval, 2),
        'right_val': round(rval, 2),
        'diff': round(diff, 2)
    }, index=[0])
    total_resume = pd.DataFrame({
        'rule': rulename,
        'left': round(lval, 2),
        'right': round(rval, 2),
        'diff': round(diff, 2)
    }, index=[0])
    results = pd.concat([results, total], ignore_index=True)
    summary = pd.concat([summary, total_resume], ignore_index=True)

rules = pd.concat([rules, results], ignore_index=True)

logging.info('Montando resultados detalhados...')
details = {}
for rulename in rulelist:
    logging.debug(f'...{rulename}')
    left = rules.query(f'rule=="{rulename}" & side == "left"')[['dataset', 'field', 'filter', 'left_val', 'minus']].to_dict('records')
    right = rules.query(f'rule=="{rulename}" & side == "right"')[['dataset', 'field', 'filter', 'right_val', 'minus']].to_dict('records')
    total = rules.query(f'rule=="{rulename}" & side == "total"')[['left_val', 'right_val', 'diff']].to_dict('records')
    details[rulename] = {'total': total}
    llen = len(left)
    rlen = len(right)
    if llen < rlen:
        left = left + [{'dataset': '', 'field': '', 'filter': '', 'left_val': '', 'minus': ''} for i in range(0, rlen-llen, 1)]
    if rlen < llen:
        right = right + [{'dataset': '', 'field': '', 'filter': '', 'right_val': '', 'minus': ''} for i in range(0, llen-rlen, 1)]
    lst = []
    for k in range(0, len(left)):
        lst.append({
            'l_dataset': left[k]['dataset'],
            'l_field': left[k]['field'],
            'l_filter': left[k]['filter'],
            'l_value': left[k]['left_val'],
            'l_minus': left[k]['minus'],
            'r_dataset': right[k]['dataset'],
            'r_field': right[k]['field'],
            'r_filter': right[k]['filter'],
            'r_value': right[k]['right_val'],
            'r_minus': right[k]['minus'],
        })
    details[rulename] = {
        'items': lst,
        'total': total[0]
    }

# Salva os resultados
logging.info('Salvando resultados...')
rules.to_excel(path.join('.', outputdir, 'result.xlsx'))

# Cria o relatório HTML
logging.info('Criando relatório HTML...')
jinja_env = Environment(
    loader=FileSystemLoader(templatesdir)
)

template = jinja_env.get_template('report.html')

database = datasets['balver']['data_final'].unique()[0]
datainicial = datasets['balver']['data_inicial'].unique()[0]
datageracao = datasets['balver']['data_geracao'].unique()[0]

html = template.render(database=database, perfil=profile['nome'], summary=summary, details=details, datetime=datetime, datainicial=datainicial, datageracao=datageracao)

logging.info('Salvando relatório HTML...')
with open(path.join('.', outputdir, 'report.html'), 'w', encoding='utf-8') as f:
    f.write(html)

logging.info('Processo terminado!')