"""
pedido.py
=========

Representa um pedido em um sistema de comércio eletrônico.

No Padrão Strategy, a classe Pedido é o CONTEXTO:
    - Ela NÃO sabe mais COMO o frete é calculado.
    - Ela apenas guarda uma referência para uma estratégia (EstrategiaFrete)
      e DELEGA o cálculo para ela.

ANTES (versão com Code Smell):
    calcular_frete(tipo_servico) tinha um if/elif com todos os tipos de frete.
    Cada frete novo obrigava a abrir e modificar esta classe -> violava o
    Princípio Aberto/Fechado (OCP), deixava a classe frágil e arriscada de mexer.

DEPOIS (versão refatorada):
    Pedido depende apenas da ABSTRAÇÃO EstrategiaFrete, nunca das classes
    concretas (FreteSedex, FretePac...). Novos fretes = novas classes em
    estrategias_frete.py, sem modificar nenhuma linha deste arquivo.
"""

from typing import Optional

# Importa apenas a interface (abstração). Pedido não importa nenhuma
# estratégia concreta: ela não precisa conhecer SEDEX, PAC, DRONE etc.
from estrategias_frete import EstrategiaFrete


class Pedido:
    """Contexto do padrão Strategy: um pedido que delega o cálculo do frete."""

    def __init__(self, peso_kg: float):
        # Atributo "privado" com o peso do pedido.
        # Em Python, o prefixo _ é a convenção para indicar que o atributo
        # é de uso interno da classe e não deve ser acessado de fora.
        self._peso_kg = peso_kg

        # PASSO 3 - Novo atributo privado que guarda a estratégia de frete.
        # Começa como None: o pedido é criado sem frete definido, e o
        # cliente (main) "injeta" a estratégia depois, pelo setter.
        self._estrategia: Optional[EstrategiaFrete] = None

    # -----------------------------------------------------------------------
    # PASSO 3 - Setter público para a estratégia
    # -----------------------------------------------------------------------
    def set_estrategia(self, estrategia: EstrategiaFrete) -> None:
        """
        Define (injeta) qual estratégia de frete o pedido vai usar.

        Isso permite TROCAR o algoritmo em tempo de execução: o mesmo pedido
        pode calcular SEDEX, depois PAC, depois DRONE, só trocando a estratégia.
        """
        # Validação defensiva: garante que o objeto recebido realmente
        # segue o contrato da interface EstrategiaFrete.
        if not isinstance(estrategia, EstrategiaFrete):
            raise TypeError("A estratégia precisa implementar EstrategiaFrete.")
        self._estrategia = estrategia

    # -----------------------------------------------------------------------
    # PASSO 3 - Novo método calcular_frete() SEM parâmetros
    # (o método antigo calcular_frete(tipo_servico) com if/elif foi excluído)
    # -----------------------------------------------------------------------
    def calcular_frete(self) -> float:
        """
        Calcula o frete delegando o trabalho para a estratégia atual.

        Repare que não existe nenhum if/elif aqui: Pedido não sabe qual
        estratégia está usando. Ele só confia que ela tem o método
        'calcular', porque toda EstrategiaFrete é obrigada a ter.
        Isso é POLIMORFISMO: a mesma chamada executa algoritmos diferentes
        dependendo do objeto que está em self._estrategia.
        """
        if self._estrategia is None:
            raise ValueError(
                "Nenhuma estratégia de frete definida. Use set_estrategia() antes."
            )

        # type(...).__name__ pega o nome da classe da estratégia (ex.: "FreteSedex")
        # só para exibir no console, como a versão original fazia.
        print(f"Calculando frete para: {type(self._estrategia).__name__}")

        # DELEGAÇÃO: o pedido passa a si mesmo (self) para a estratégia,
        # que lê o que precisar (ex.: peso) e devolve o valor calculado.
        return self._estrategia.calcular(self)

    # -----------------------------------------------------------------------
    # Propriedades (getters) para acesso seguro aos atributos
    # -----------------------------------------------------------------------
    @property
    def peso_kg(self) -> float:
        """Permite ler o peso (pedido.peso_kg) sem expor o atributo privado."""
        return self._peso_kg
