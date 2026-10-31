"""Conversão entre CSV e JSON."""
from .escritor import escrever_csv, escrever_json
from .leitor import ler_csv, ler_json


def csv_para_json(origem, destino):
    registros = ler_csv(origem)
    escrever_json(destino, registros)
    return len(registros)


def json_para_csv(origem, destino):
    registros = ler_json(origem)
    escrever_csv(destino, registros)
    return len(registros)
