"""Backup automático de arquivos antes de qualquer alteração."""
import os
from datetime import datetime

from .erros import BackupError


def criar_backup(caminho, pasta_backup="backups"):
    """Copia o arquivo original para `pasta_backup` com carimbo de data/hora.

    Retorna o caminho do backup, ou None se o arquivo ainda não existe
    (nada a preservar). Lança BackupError se a cópia falhar.
    """
    if not os.path.exists(caminho):
        print(f"[BACKUP] '{caminho}' ainda não existe; backup não necessário.")
        return None

    nome, extensao = os.path.splitext(os.path.basename(caminho))
    carimbo = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    destino = os.path.join(pasta_backup, f"{nome}_{carimbo}{extensao}")

    try:
        os.makedirs(pasta_backup, exist_ok=True)
        # Cópia binária com with open: preserva o conteúdo byte a byte.
        with open(caminho, "rb") as origem, open(destino, "wb") as copia:
            copia.write(origem.read())
    except OSError as erro:
        raise BackupError(f"não foi possível copiar '{caminho}' "
                          f"({erro.strerror or erro}).") from erro

    print(f"[BACKUP] Cópia criada em '{destino}'.")
    return destino
