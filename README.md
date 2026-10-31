# TED03 – Persistência de Dados em CSV e JSON

Módulo em Python para gerenciar dados persistidos em arquivos **CSV** e **JSON**, com conversão entre os dois formatos, tratamento de exceções de entrada/saída e **backup automático** antes de qualquer alteração de arquivo.

## Integrantes

- [NOME COMPLETO DO INTEGRANTE 1]
- [NOME COMPLETO DO INTEGRANTE 2]

**Instituição:** UniBalsas
**Curso:** Sistemas de Informação
**Disciplina:** [NOME DA DISCIPLINA]

## Funcionalidades

- **Leitura de CSV** e conversão dos registros para **JSON**, sem perda de informações.
- **Leitura de JSON** e conversão dos registros para **CSV**, sem perda de informações.
- **Atualização de registros** em arquivos `.csv` ou `.json`, localizando o registro por um campo-chave.
- **Gerenciamento seguro de arquivos:** todas as aberturas usam `with open(...)`, com codificação UTF-8 explícita, e o fechamento é automático, inclusive em caso de exceção.
- **Backup automático:** antes de qualquer escrita ou atualização, o arquivo original é copiado para a pasta `backups/` com data e hora no nome. Se o backup falhar, a escrita é cancelada.
- **Tratamento de exceções** com mensagens claras, sem encerrar a aplicação:
  - `FileNotFoundError` (arquivo inexistente)
  - `PermissionError` (sem permissão)
  - `UnicodeDecodeError` (arquivo fora de UTF-8)
  - JSON malformado, CSV malformado, pasta no lugar de arquivo e dados fora do formato esperado

## Estrutura do projeto

```
ted03/
├── main.py                 # menu interativo no terminal
├── testes.py               # testes automáticos (casos válidos e de erro)
├── README.md
├── persistencia/
│   ├── __init__.py
│   ├── leitor.py           # ler_csv, ler_json
│   ├── escritor.py         # escrever_csv, escrever_json, atualizar_registro
│   ├── conversor.py        # csv_para_json, json_para_csv
│   ├── backup.py           # criar_backup
│   └── erros.py            # exceções próprias e mensagens ao usuário
├── dados/                  # arquivos de exemplo para teste
│   ├── clientes.csv
│   ├── clientes.json
│   └── invalido.json       # JSON malformado, usado para testar erro
└── relatorio/
    ├── TED03_Relatorio_Nome1_Nome2.pdf
    └── prints/             # capturas de tela usadas no relatório
```

## Requisitos

- Python 3.8 ou superior
- Nenhuma biblioteca externa (apenas `csv`, `json`, `os`, `datetime` da biblioteca padrão)

## Como executar

Abra um terminal **dentro da pasta do projeto** (`ted03`) e rode:

```
python main.py
```

Menu:

```
1 - Converter CSV para JSON
2 - Converter JSON para CSV
3 - Atualizar um registro (CSV ou JSON)
0 - Sair
```

Nas opções 1 e 2, apertar Enter nos dois campos usa os arquivos de exemplo (`dados/clientes.csv` → `saida/clientes.json` e `dados/clientes.json` → `saida/clientes_convertido.csv`).

Na opção 3, informe o caminho completo do arquivo, o campo-chave e seu valor, o campo a alterar e o novo valor. Exemplo:

```
Arquivo (.csv ou .json): dados/clientes.csv
Campo-chave (ex.: id): id
Valor do campo-chave: 2
Campo a alterar: cidade
Novo valor: Balsas
```

Antes de gravar, o programa informa a criação do backup em `backups/`.

## Como testar

### Testes automáticos

```
python testes.py
```

O script executa em uma pasta temporária (não altera os arquivos do projeto) e verifica:

1. Conversão CSV → JSON, com acentos preservados.
2. Conversão JSON → CSV, com união das colunas dos registros.
3. Atualização de registro com criação prévia do backup e conferência do conteúdo original.
4. Erros: arquivo inexistente, JSON malformado, arquivo fora de UTF-8, pasta no lugar de arquivo e falta de permissão (este último é pulado no Windows).

### Testes manuais

- **Arquivo inexistente:** na opção 1, informe `naoexiste.csv` como origem.
- **JSON inválido:** na opção 2, informe `dados/invalido.json` como origem.
- **Formato não suportado:** na opção 3, informe um arquivo que não seja `.csv` nem `.json`.

## Decisões de projeto

- **CSV → JSON** mantém os valores como texto, pois o CSV não guarda tipos de dados. Assim nenhuma informação é perdida.
- **JSON → CSV** reúne as chaves de todos os registros como colunas; campos ausentes ficam vazios, e listas ou objetos aninhados são gravados como texto JSON na célula.
- O CSV é lido com `utf-8-sig`, o que permite abrir arquivos exportados pelo Excel (com BOM).
- A pasta `backups/` e a pasta `saida/` são criadas automaticamente quando necessário.

## Relatório técnico

O relatório em PDF está em `relatorio/`.
