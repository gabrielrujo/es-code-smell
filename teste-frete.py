"""
teste-frete.py
==============

Código CLIENTE (o "main") do Padrão Strategy.

PASSO 4: o cliente agora é o responsável por escolher e "injetar" a
estratégia de frete no pedido ANTES de pedir o cálculo.

Fluxo:
    1. Cria o pedido (contexto).
    2. Cria a estratégia desejada (ex.: FreteSedex()).
    3. Injeta a estratégia no pedido com set_estrategia(...).
    4. Chama pedido.calcular_frete(), sem parâmetros.
"""

from pedido import Pedido

# O cliente é quem conhece as estratégias concretas e decide qual usar.
from estrategias_frete import (
    FreteSedex,
    FretePac,
    FreteTransportadora,
    FreteMotoboy,
    FreteDrone,          # novo (Passo 5)
    FreteRetiradaLocal,  # novo (requisito citado no cenário)
)


def main():
    print("*" * 30)
    print("Executando Versão Refatorada (Strategy)")
    print("*" * 30)

    # 1) Cria o pedido. Ele ainda não tem nenhuma estratégia de frete.
    pedido = Pedido(peso_kg=2.5)

    # 2) Injeta a estratégia SEDEX e calcula.
    pedido.set_estrategia(FreteSedex())
    frete_sedex = pedido.calcular_frete()
    print(f"Valor do frete SEDEX: R$ {frete_sedex:.2f}")

    # 3) Troca a estratégia em tempo de execução: mesmo pedido, agora PAC.
    pedido.set_estrategia(FretePac())
    frete_pac = pedido.calcular_frete()
    print(f"Valor do frete PAC: R$ {frete_pac:.2f}")

    pedido.set_estrategia(FreteTransportadora())
    frete_transp = pedido.calcular_frete()
    print(f"Valor do frete TRANSPORTADORA: R$ {frete_transp:.2f}")

    pedido.set_estrategia(FreteMotoboy())
    frete_motoboy = pedido.calcular_frete()
    print(f"Valor do frete MOTOBOY: R$ {frete_motoboy:.2f}")

    # Segundo pedido, mais pesado.
    # Obs.: no código original havia um bug aqui: o pedido2 era criado mas o
    # cálculo usava 'pedido' (2,5 kg) em vez de 'pedido2' (10 kg).
    # Corrigido para usar pedido2.
    pedido2 = Pedido(peso_kg=10.0)
    pedido2.set_estrategia(FretePac())
    frete_pac2 = pedido2.calcular_frete()
    print(f"Valor do frete PAC (pedido de 10 kg): R$ {frete_pac2:.2f}")

    # -----------------------------------------------------------------------
    # PASSO 5 - Teste da extensibilidade
    # Os novos fretes funcionam sem NENHUMA alteração na classe Pedido.
    # -----------------------------------------------------------------------
    print("-" * 30)
    print("Novos fretes (sem modificar a classe Pedido)")
    print("-" * 30)

    pedido.set_estrategia(FreteDrone())
    frete_drone = pedido.calcular_frete()
    print(f"Valor do frete DRONE: R$ {frete_drone:.2f}")

    pedido.set_estrategia(FreteRetiradaLocal())
    frete_retirada = pedido.calcular_frete()
    print(f"Valor do frete RETIRADA_LOCAL: R$ {frete_retirada:.2f}")


# Ponto de entrada: só executa main() quando o arquivo é rodado diretamente
# (python teste-frete.py), e não quando é importado por outro módulo.
if __name__ == "__main__":
    main()
