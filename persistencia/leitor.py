"""Leitura de arquivos CSV e JSON."""
import csv
import json

from .erros import DadosInvalidosError


def ler_csv(caminho, delimitador=","):
    """Lê um CSV e retorna uma lista de dicionários (valores como texto).

    Usa utf-8-sig para aceitar arquivos exportados pelo Excel (com BOM).
    """
    with open(caminho, "r", encoding="utf-8-sig", newline="") as arquivo:
        leitor = csv.DictReader(arquivo, delimiter=delimitador)
        if leitor.fieldnames is None:
            raise DadosInvalidosError("o arquivo CSV está vazio.")
        registros = []
        for numero, linha in enumerate(leitor, start=2):
            if None in linha:
                raise DadosInvalidosError(
                    f"a linha {numero} tem mais campos que o cabeçalho.")
            registros.append(linha)
    return registros


def ler_json(caminho):
    """Lê um JSON e retorna uma lista de dicionários."""
    with open(caminho, "r", encoding="utf-8") as arquivo:
        dados = json.load(arquivo)
    if isinstance(dados, dict):
        dados = [dados]
    if not isinstance(dados, list) or not all(isinstance(r, dict) for r in dados):
        raise DadosInvalidosError(
            "esperada uma lista de objetos (registros) no JSON.")
    return dados
