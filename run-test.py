"""
Executa os testes
"""

import argparse
import pandas as pd
from os import path
from charset_normalizer import from_path
from io import StringIO
from jinja2 import Environment, FileSystemLoader

# Configurações
entidades = {
    0: {
        'orgaos': (2, 3, 4, 5, 6, 7, 8, 9, 10, 11),
        'nome': 'Prefeitura',
        'rules': ('agnostic.csv', 'pm.csv')
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
profile = entidades[profile]

# Carrega as rules
rules = pd.DataFrame(columns=['rule', 'side', 'dataset', 'field', 'filter', 'subtract'])
for rulefile in profile['rules']:
    csv = StringIO(str(from_path(path.join('.', rulesdir, rulefile)).best()))
    ruledf = pd.read_csv(csv, sep=';')
    rules = pd.concat([rules, ruledf], join='outer', ignore_index=True)
rules.fillna(False, axis='columns', inplace=True)
rules['left_val'] = 0.0
rules['right_val'] = 0.0
rules['diff'] = None
# Carrega e prepara os csv do PAD
csvdir = path.join(padcsvdir, ano+'-'+mes)
datasets = {}

# bal_ver
dados = StringIO(str(from_path(path.join(csvdir, 'bal_ver.csv')).best()))
df = pd.read_csv(dados, sep=';', parse_dates=True, infer_datetime_format=True, decimal=',', thousands='.')
datasets['balver'] = df[
    (df['orgao'].isin(profile['orgaos']))
    & (df['escrituracao'] == 'S')
].copy()

# Cria a lista de nomes de regras
rulelist = rules['rule'].unique()

# Cria o df de resultados
results = pd.DataFrame(columns=['rule', 'side', 'dataset', 'field', 'filter', 'minus', 'left_val', 'right_val', 'diff'])

# Processa as rules
for rulename in rulelist:
    rulespec = rules[rules['rule'] == rulename]
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
            rules.at[key, 'rigth_val'] = val
            rval += val
    diff = round(lval - rval, 2)
    total = pd.DataFrame({
        'rule': rulename,
        'side': 'total',
        'dataset': None,
        'field': None,
        'filter': None,
        'minus': None,
        'left_val': lval,
        'right_val': rval,
        'diff': diff
    }, index=[0])
    results = pd.concat([results, total], ignore_index=True)

rules = pd.concat([rules, results], ignore_index=True)

# Salva os resultados
rules.to_excel(path.join('.', outputdir, 'result.xlsx'))

# Cria o relatório HTML
jinja_env = Environment(
    loader=FileSystemLoader(templatesdir)
)

template = jinja_env.get_template('report.html')

database = datasets['balver']['data_final'].unique()[0]

html = template.render(database=database, perfil=profile['nome'])

with open(path.join('.', outputdir, 'report.html'), 'w', encoding='utf-8') as f:
    f.write(html)