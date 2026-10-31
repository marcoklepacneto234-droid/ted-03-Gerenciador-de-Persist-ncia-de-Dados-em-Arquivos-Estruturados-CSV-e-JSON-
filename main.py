"""Menu de linha de comando do módulo de persistência CSV/JSON."""
from persistencia.conversor import csv_para_json, json_para_csv
from persistencia.erros import executar_seguro
from persistencia.escritor import atualizar_registro

MENU = """
=== Persistência CSV/JSON ===
1 - Converter CSV para JSON
2 - Converter JSON para CSV
3 - Atualizar um registro (CSV ou JSON)
0 - Sair
"""


def opcao_converter(funcao, padrao_origem, padrao_destino):
    origem = input(f"Arquivo de origem [{padrao_origem}]: ").strip() or padrao_origem
    destino = input(f"Arquivo de destino [{padrao_destino}]: ").strip() or padrao_destino
    ok, total = executar_seguro(funcao, origem, origem, destino)
    if ok:
        print(f"Conversão concluída: {total} registro(s).")


def opcao_atualizar():
    arquivo = input("Arquivo (.csv ou .json): ").strip()
    campo = input("Campo-chave (ex.: id): ").strip()
    valor = input("Valor do campo-chave: ").strip()
    campo_novo = input("Campo a alterar: ").strip()
    valor_novo = input("Novo valor: ").strip()
    ok, total = executar_seguro(atualizar_registro, arquivo, arquivo,
                                campo, valor, {campo_novo: valor_novo})
    if ok and total:
        print(f"{total} registro(s) atualizado(s).")


def main():
    while True:
        print(MENU)
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            opcao_converter(csv_para_json, "dados/clientes.csv", "saida/clientes.json")
        elif escolha == "2":
            opcao_converter(json_para_csv, "dados/clientes.json", "saida/clientes_convertido.csv")
        elif escolha == "3":
            opcao_atualizar()
        elif escolha == "0":
            print("Encerrando.")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
