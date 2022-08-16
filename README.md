# Testes de consistência contábil

Sistema que realiza testes de consistência dos dados contábeis.

## Origem dos dados

Os dados são os do SIAPC/PAD convertidos para CSV com o [pad-converter](https://github.com/iddrs/pad-converter).

## Regras

As regras são arquivos *CSV* dentro do diretório `rules`.

O formato dos campos dos arquivos de regras é:

rule
: Nome da regra

side
: left|right

dataset
: nome do arquivo CSV

field
: nome do campo dentro do arquivo CSV

filter
: filtro para ser aplicado pelo Python

minus
: ""|0|1 Se 0 ou vazio (""), o valor resultante é usado; se 1, o valor resultante é invertido o sinal.

É necessário ter ao menos uma linha *left* e outra *right*.

Um exemplo:

```
rule;side;dataset;field;filter;minus
Cancelamento/Anulação de dotações;left;balver;saldo_atual_debito;conta_contabil.str.startswith('5.2.2.1.9.04.');1
Cancelamento/Anulação de dotações;left;balver;saldo_atual_credito;conta_contabil.str.startswith('5.2.2.1.9.04.');
Cancelamento/Anulação de dotações;right;baldesp;reducao_dotacao;orgao>0;
```

A inclusão de novas regras deve ser feita dentro do arquivo `run-test.py`.

## Executando os testes

Para executar o teste, antes carregue o ambiente Python com `venv\Scripts\activate.*`. A extensão do script *activate* vai depender de qual shell estejas utilizando (cmd.exe, Power Shell, Linux, etc).

Uma vez carregado o ambiente Python, execute `python run-test.py [entidade] [mês] [ano]` substituindo os argumentos pelos valores adequados.

## Obtendo o resultado dos testes

O resultado de cada texte é escrito em `output\report.html`.
