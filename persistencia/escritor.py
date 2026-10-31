"""Escrita e atualização de arquivos CSV e JSON (sempre com backup)."""
import csv
import json
import os

from .backup import criar_backup
from .erros import DadosInvalidosError
from .leitor import ler_csv, ler_json


def _preparar_destino(caminho):
    """Faz o backup do arquivo existente e garante que a pasta exista."""
    criar_backup(caminho)  # ANTES de qualquer alteração
    pasta = os.path.dirname(caminho)
    if pasta:
        os.makedirs(pasta, exist_ok=True)


def _colunas(registros):
    """União das chaves de todos os registros, mantendo a ordem."""
    colunas = []
    for registro in registros:
        for chave in registro:
            if chave not in colunas:
                colunas.append(chave)
    return colunas


def _para_celula(valor):
    """Converte um valor para texto de célula CSV sem perder informação."""
    if valor is None:
        return ""
    if isinstance(valor, (dict, list)):
        return json.dumps(valor, ensure_ascii=False)
    return valor


def escrever_json(caminho, registros):
    _preparar_destino(caminho)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(registros, arquivo, ensure_ascii=False, indent=2)
    print(f"[OK] {len(registros)} registro(s) gravado(s) em '{caminho}'.")


def escrever_csv(caminho, registros):
    colunas = _colunas(registros)
    if not colunas:
        raise DadosInvalidosError("não há dados para gravar no CSV.")
    _preparar_destino(caminho)
    with open(caminho, "w", encoding="utf-8", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        for registro in registros:
            escritor.writerow({c: _para_celula(registro.get(c, ""))
                               for c in colunas})
    print(f"[OK] {len(registros)} registro(s) gravado(s) em '{caminho}'.")


def atualizar_registro(caminho, campo_chave, valor_chave, alteracoes):
    """Atualiza registros cujo `campo_chave` == `valor_chave`.

    Funciona para .csv e .json. O backup é feito antes da gravação.
    Retorna a quantidade de registros alterados.
    """
    extensao = os.path.splitext(caminho)[1].lower()
    if extensao == ".csv":
        ler, gravar = ler_csv, escrever_csv
    elif extensao == ".json":
        ler, gravar = ler_json, escrever_json
    else:
        raise DadosInvalidosError("formato não suportado (use .csv ou .json).")

    registros = ler(caminho)
    alterados = 0
    for registro in registros:
        if str(registro.get(campo_chave)) == str(valor_chave):
            registro.update(alteracoes)
            alterados += 1

    if alterados == 0:
        print(f"[AVISO] Nenhum registro com {campo_chave} = {valor_chave}. "
              "Nada foi alterado.")
        return 0
    gravar(caminho, registros)
    return alterados
