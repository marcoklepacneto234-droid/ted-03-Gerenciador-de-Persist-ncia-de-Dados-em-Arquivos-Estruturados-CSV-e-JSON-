"""Testes automáticos: casos válidos e situações de erro."""
import os
import shutil
import stat
import tempfile

from persistencia.conversor import csv_para_json, json_para_csv
from persistencia.erros import executar_seguro
from persistencia.escritor import atualizar_registro
from persistencia.leitor import ler_csv, ler_json

resultados = []


def verificar(nome, condicao):
    resultados.append(condicao)
    print(f"  [{'PASSOU' if condicao else 'FALHOU'}] {nome}")


def main():
    tmp = tempfile.mkdtemp()
    os.chdir(tmp)  # backups/ será criada aqui, sem sujar o projeto
    dados = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados")
    try:
        print("\n1) CSV -> JSON")
        ok, n = executar_seguro(csv_para_json, "x", f"{dados}/clientes.csv", "saida/c.json")
        verificar("converteu 3 registros", ok and n == 3)
        verificar("acentos preservados", ler_json("saida/c.json")[0]["nome"] == "João Ferreira")

        print("\n2) JSON -> CSV")
        ok, n = executar_seguro(json_para_csv, "x", f"{dados}/clientes.json", "saida/j.csv")
        verificar("converteu 2 registros", ok and n == 2)
        linhas = ler_csv("saida/j.csv")
        verificar("coluna 'email' criada e vazia onde não existia", linhas[0]["email"] == "")

        print("\n3) Atualização com backup")
        shutil.copy(f"{dados}/clientes.csv", "alvo.csv")
        ok, n = executar_seguro(atualizar_registro, "alvo.csv", "alvo.csv",
                                "id", "1", {"cidade": "Carolina"})
        verificar("1 registro alterado", ok and n == 1)
        verificar("backup criado", len(os.listdir("backups")) == 1)
        with open(os.path.join("backups", os.listdir("backups")[0]), encoding="utf-8") as f:
            verificar("backup guarda o valor original", "Balsas" in f.read())

        print("\n4) Situações de erro (o programa não deve encerrar)")
        ok, _ = executar_seguro(ler_csv, "nao_existe.csv", "nao_existe.csv")
        verificar("FileNotFoundError tratado", not ok)

        ok, _ = executar_seguro(ler_json, "invalido.json", f"{dados}/invalido.json")
        verificar("JSON malformado tratado", not ok)

        with open("latin1.csv", "w", encoding="latin-1") as f:
            f.write("id,nome\n1,João\n")
        ok, _ = executar_seguro(ler_csv, "latin1.csv", "latin1.csv")
        verificar("UnicodeDecodeError tratado", not ok)

        ok, _ = executar_seguro(ler_csv, ".", ".")
        verificar("pasta no lugar de arquivo tratada", not ok)

        if hasattr(os, "geteuid") and os.geteuid() != 0:
            shutil.copy(f"{dados}/clientes.csv", "bloqueado.csv")
            os.chmod("bloqueado.csv", 0)
            ok, _ = executar_seguro(ler_csv, "bloqueado.csv", "bloqueado.csv")
            os.chmod("bloqueado.csv", stat.S_IRUSR | stat.S_IWUSR)
            verificar("PermissionError tratado", not ok)
        else:
            print("  [PULADO] teste de permissão (Windows ou root)")
    finally:
        os.chdir(tempfile.gettempdir())
        shutil.rmtree(tmp, ignore_errors=True)

    print(f"\n{sum(resultados)}/{len(resultados)} verificações passaram.")


if __name__ == "__main__":
    main()
