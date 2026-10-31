"""Tratamento centralizado de erros de entrada/saída."""
import csv
import json


class DadosInvalidosError(Exception):
    """Conteúdo do arquivo fora do formato esperado."""


class BackupError(Exception):
    """Falha ao criar o backup; a escrita é abortada."""


def descrever_erro(erro, caminho):
    """Converte uma exceção em mensagem clara para o usuário."""
    if isinstance(erro, FileNotFoundError):
        return f"Arquivo não encontrado: '{caminho}'. Verifique o nome e o caminho."
    if isinstance(erro, PermissionError):
        return f"Sem permissão para acessar ou modificar '{caminho}'."
    if isinstance(erro, IsADirectoryError):
        return f"'{caminho}' é uma pasta, não um arquivo."
    if isinstance(erro, UnicodeDecodeError):
        return (f"Erro de codificação ao ler '{caminho}': o arquivo não está em UTF-8. "
                "Salve-o novamente como UTF-8.")
    if isinstance(erro, json.JSONDecodeError):
        return (f"JSON inválido em '{caminho}' (linha {erro.lineno}, "
                f"coluna {erro.colno}): {erro.msg}.")
    if isinstance(erro, csv.Error):
        return f"CSV malformado em '{caminho}': {erro}."
    if isinstance(erro, DadosInvalidosError):
        return f"Dados inválidos em '{caminho}': {erro}"
    if isinstance(erro, BackupError):
        return f"Operação cancelada, pois o backup falhou: {erro}"
    if isinstance(erro, OSError):
        return f"Erro de entrada/saída com '{caminho}': {erro.strerror or erro}."
    return f"Erro inesperado com '{caminho}': {erro}"


def executar_seguro(operacao, caminho, *args, **kwargs):
    """Executa `operacao` sem encerrar o programa em caso de erro.

    Retorna (sucesso, resultado). Em falha, imprime a mensagem e
    resultado é None.
    """
    try:
        return True, operacao(*args, **kwargs)
    except (OSError, ValueError, csv.Error,
            DadosInvalidosError, BackupError) as erro:
        # UnicodeDecodeError e JSONDecodeError são subclasses de ValueError
        print(f"[ERRO] {descrever_erro(erro, caminho)}")
        return False, None
