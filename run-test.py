"""
Executa os testes
"""
import os
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
        'rules': (
            'info_patrim.csv',
            'info_orc.csv',
            'info_controle.csv',
            'suprim.csv',
            'parcerias_apropriar.csv',
            'precatorios_apagar.csv',
            'rpps_apagar.csv',
            'rgps_apagar.csv',
            'fgts_apagar.csv',
            'rpp_apagar.csv',
            'pasep_apagar.csv',
            'prev_rec_inicial.csv',
            'prev_ded_fundeb_inicial.csv',
            'prev_outras_ded_inicial.csv',
            'reestimativa_receita.csv',
            'dotacao_inicial.csv',
            'credito_suplementar.csv',
            'credito_especial.csv',
            'credito_especial_reaberto.csv',
            'credito_extraordinario.csv',
            'credito_superavit.csv',
            'credito_excesso.csv',
            'credito_anulacao.csv',
            'credito_reabertura.csv',
            'anulacao_dotacao.csv',
            'emissao_empenhos.csv',
            'rpnp_inscritos.csv',
            'rpnp_inscritos_anterior.csv',
            'rpnp_inscricao_exe.csv',
            'rpp_inscritos.csv',
            'rpp_inscritos_anterior.csv',
            'rpp_inscricao_exe.csv',
            'receita_arealizar.csv',
            'receita_realizada.csv',
            'deducao_receita_fundeb.csv',
            'deducao_receita_renuncia.csv',
            'deducao_receita_outras.csv',
            'empenhado_aliquidar.csv',
            'liquidado_apagar.csv',
            'pago.csv',
            'rpnp_aliquidar.csv',
            'rpnp_apagar.csv',
            'rpnp_pago.csv',
            'rpnp_cancelado.csv',
            'rpp_pago.csv',
            'rnp_cancelado.csv',
            'niveis_orc.csv',
            'niveis_controle.csv',
            'disponibilidades.csv',
            'resultado_financeiro.csv',
            'resultado.csv',
            'situacao.csv',
            'ddr_disponivel.csv',
            'ddr_empenhada.csv',
            'ddr_liquidada.csv',
            'ddr_utilizada.csv'
        )
    },
    1: {
        'orgaos': (12,),
        'nome': 'FPSM',
        'rules': (
            'info_patrim.csv',
            'info_orc.csv',
            'info_controle.csv',
            'suprim.csv',
            'rpps_apagar.csv',
            'rpp_apagar.csv',
            'pasep_apagar.csv',
            'prev_rec_inicial.csv',
            'prev_outras_ded_inicial.csv',
            'reestimativa_receita.csv',
            'dotacao_inicial.csv',
            'credito_suplementar.csv',
            'credito_especial.csv',
            'credito_especial_reaberto.csv',
            'credito_extraordinario.csv',
            'credito_superavit.csv',
            'credito_excesso.csv',
            'credito_anulacao.csv',
            'credito_reabertura.csv',
            'anulacao_dotacao.csv',
            'emissao_empenhos.csv',
            'rpnp_inscritos.csv',
            'rpnp_inscritos_anterior.csv',
            'rpnp_inscricao_exe.csv',
            'rpp_inscritos.csv',
            'rpp_inscritos_anterior.csv',
            'rpp_inscricao_exe.csv',
            'receita_arealizar.csv',
            'receita_realizada.csv',
            'deducao_receita_outras.csv',
            'empenhado_aliquidar.csv',
            'liquidado_apagar.csv',
            'pago.csv',
            'rpnp_aliquidar.csv',
            'rpnp_apagar.csv',
            'rpnp_pago.csv',
            'rpnp_cancelado.csv',
            'rpp_pago.csv',
            'rnp_cancelado.csv',
            'niveis_orc.csv',
            'niveis_controle.csv',
            'disponibilidades.csv',
            'resultado_financeiro.csv',
            'resultado.csv',
            'situacao.csv',
            'ddr_disponivel.csv',
            'ddr_empenhada.csv',
            'ddr_liquidada.csv',
            'ddr_utilizada.csv'
        )
    },
    2: {
        'orgaos': (1,),
        'nome': 'Câmara de Vereadores',
        'rules': (
            'info_patrim.csv',
            'info_orc.csv',
            'info_controle.csv',
            'suprim.csv',
            'rpps_apagar.csv',
            'rgps_apagar.csv',
            'fgts_apagar.csv',
            'rpp_apagar.csv',
            'pasep_apagar.csv',
            'dotacao_inicial.csv',
            'credito_suplementar.csv',
            'credito_especial.csv',
            'credito_especial_reaberto.csv',
            'credito_extraordinario.csv',
            'credito_superavit.csv',
            'credito_anulacao.csv',
            'credito_reabertura.csv',
            'anulacao_dotacao.csv',
            'emissao_empenhos.csv',
            'rpnp_inscritos.csv',
            'rpnp_inscritos_anterior.csv',
            'rpnp_inscricao_exe.csv',
            'rpp_inscritos.csv',
            'rpp_inscritos_anterior.csv',
            'rpp_inscricao_exe.csv',
            'empenhado_aliquidar.csv',
            'liquidado_apagar.csv',
            'pago.csv',
            'rpnp_aliquidar.csv',
            'rpnp_apagar.csv',
            'rpnp_pago.csv',
            'rpnp_cancelado.csv',
            'rpp_pago.csv',
            'rnp_cancelado.csv',
            'niveis_orc.csv',
            'niveis_controle.csv',
            'disponibilidades.csv',
            'resultado_financeiro.csv',
            'resultado.csv',
            'situacao.csv',
            'ddr_disponivel.csv',
            'ddr_empenhada.csv',
            'ddr_utilizada.csv'
        )
    },
    9: {
        'orgaos': (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12),
        'nome': 'Município (Agregado)',
        'rules': (
            'receita_despesa_intra.csv',
            'intra_ofss_ativo_passivo.csv',
            'intra_ofss_resultado.csv',
            'contribuicao_previdenciaria_areceber.csv'
        )
    }
}
rulesdir = r'rules'
padcsvdir = r'C:\Users\Everton\OneDrive\Prefeitura\PAD'
outputdir = r'output'
templatesdir = r'templates'
datasetspath = r'datasets/datasets.xlsx'

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

# bal_desp
logging.debug('...BAL_DESP.txt')
dados = StringIO(str(from_path(path.join(csvdir, 'bal_desp.csv')).best()))
df = pd.read_csv(dados, sep=';', parse_dates=True, infer_datetime_format=True, decimal=',', thousands='.', dtype={'elemento': str})
datasets['baldesp'] = df[df['orgao'].isin(profile['orgaos'])].copy()
datasets['baldesp']['dotacao_atualizada'] = round(datasets['baldesp'].dotacao_inicial + datasets['baldesp'].atualizacao_monetaria + datasets['baldesp'].creditos_suplementares + datasets['baldesp'].creditos_especiais + datasets['baldesp'].creditos_extraordinarios - datasets['baldesp'].reducao_dotacao + datasets['baldesp'].suplementacao_recurso_vinculado - datasets['baldesp'].reducao_recurso_vinculado + datasets['baldesp'].transferencia + datasets['baldesp'].transposicao + datasets['baldesp'].remanejamento, 2)
datasets['baldesp']['a_empenhar'] = round(datasets['baldesp'].dotacao_atualizada - datasets['baldesp'].valor_empenhado, 2)
datasets['baldesp']['a_liquidar'] = round(datasets['baldesp'].valor_empenhado - datasets['baldesp'].valor_liquidado, 2)
datasets['baldesp']['a_pagar'] = round(datasets['baldesp'].valor_liquidado - datasets['baldesp'].valor_pago, 2)

# liquidacao
logging.debug('...LIQUIDACAO.txt')
dados = StringIO(str(from_path(path.join(csvdir, 'liquidacao.csv')).best()))
df = pd.read_csv(dados, sep=';', parse_dates=True, infer_datetime_format=True, decimal=',', thousands='.', dtype={'rubrica': str})
datasets['liquidacao'] = df[df['orgao'].isin(profile['orgaos'])].copy()

# pagamento
logging.debug('...PAGAMENTO.txt')
dados = StringIO(str(from_path(path.join(csvdir, 'pagamento.csv'), threshold=0.5).best()))
df = pd.read_csv(dados, sep=';', parse_dates=True, infer_datetime_format=True, decimal=',', thousands='.', dtype={'rubrica': str})
datasets['pagamento'] = df[df['orgao'].isin(profile['orgaos'])].copy()

# restos_pagar
logging.debug('...RESTOS_PAGAR.txt')
dados = StringIO(str(from_path(path.join(csvdir, 'restos_pagar.csv'), threshold=0.5).best()))
df = pd.read_csv(dados, sep=';', parse_dates=True, infer_datetime_format=True, decimal=',', thousands='.', dtype={'rubrica': str})
ano_base = datetime.strptime(df['data_final'].max(), '%Y-%m-%d').year
df['ano_base'] = ano_base
datasets['rp'] = df[df['orgao'].isin(profile['orgaos'])].copy()

# bal_rec_alt
logging.debug('...BAL_REC_ALT.txt')
dados = StringIO(str(from_path(path.join(csvdir, 'bal_rec_alt.csv'), threshold=0.5).best()))
df = pd.read_csv(dados, sep=';', parse_dates=True, infer_datetime_format=True, decimal=',', thousands='.', dtype={'codigo_receita': str})
datasets['balrec'] = df[
    (df['orgao'].isin(profile['orgaos']))
    & (df['tipo_nivel'] == 'A')
].copy()

# decreto
logging.debug('...DECRETO.txt')
dados = StringIO(str(from_path(path.join(csvdir, 'decreto.csv'), threshold=0.5).best()))
df = pd.read_csv(dados, sep=';', parse_dates=True, infer_datetime_format=True, decimal=',', thousands='.')
df['orgao'] = 2
df.loc[df['entidade'].str.startswith('CAMARA'), 'orgao'] = 1
df.loc[df['recurso_vinculado_suplementacao_demais_tce']==50, 'orgao'] = 12
df.loc[df['recurso_vinculado_reducao_tce']==50, 'orgao'] = 12
datasets['decreto'] = df[df['orgao'].isin(profile['orgaos'])].copy()

# Salva os datasets para auditoria e testes
logging.info('Salvando datasets...')
dsw = pd.ExcelWriter(datasetspath, engine='xlsxwriter')
for sheet, data in datasets.items():
    data.to_excel(dsw, sheet_name=sheet)
dsw.save()

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

print(r'file:///'+os.path.join(os.getcwd(), r'output/report.html').replace('\\', '/'))

logging.info('Processo terminado!')