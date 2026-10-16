"""
estrategias_frete.py
====================

Este módulo contém as ESTRATÉGIAS de cálculo de frete (Padrão de Projeto Strategy).

Ideia central do padrão Strategy:
    - Temos uma família de algoritmos que fazem "a mesma coisa" de jeitos
      diferentes (aqui: calcular o valor do frete).
    - Em vez de deixar todos esses algoritmos amontoados dentro de um
      if/elif na classe Pedido, cada algoritmo vira uma CLASSE própria.
    - Todas essas classes seguem um mesmo "contrato" (a interface
      EstrategiaFrete), então a classe Pedido pode usar qualquer uma delas
      sem saber qual é.

Papéis do padrão neste projeto:
    - Strategy (interface) ....... EstrategiaFrete
    - Concrete Strategies ........ FreteSedex, FretePac, FreteTransportadora,
                                   FreteMotoboy, FreteDrone, FreteRetiradaLocal
    - Context .................... Pedido (arquivo pedido.py)
    - Client ..................... main() (arquivo teste-frete.py)

Relação com o Princípio Aberto/Fechado (OCP):
    "Entidades de software devem estar ABERTAS para extensão, mas FECHADAS
    para modificação."
    -> Para criar um novo tipo de frete, basta criar uma NOVA classe aqui
       (extensão). A classe Pedido não precisa ser alterada (fechada).
"""

# 'ABC' (Abstract Base Class) e 'abstractmethod' vêm do módulo padrão 'abc'.
# Python não tem a palavra-chave "interface" como Java/C#; o jeito idiomático
# de criar uma interface é uma classe abstrata com métodos abstratos.
from abc import ABC, abstractmethod

# TYPE_CHECKING é False durante a execução e True só para ferramentas de
# análise de tipos (ex.: mypy, editores). Usamos isso para importar Pedido
# apenas para as dicas de tipo, evitando um import circular
# (pedido.py importa este arquivo, e este arquivo "precisaria" de pedido.py).
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pedido import Pedido


# ---------------------------------------------------------------------------
# PASSO 1 - A INTERFACE (Strategy)
# ---------------------------------------------------------------------------
class EstrategiaFrete(ABC):
    """
    Interface (classe abstrata) que define o CONTRATO de toda estratégia de frete.

    Qualquer classe que herde de EstrategiaFrete é OBRIGADA a implementar o
    método 'calcular'. Se não implementar, o Python lança um TypeError ao
    tentar criar um objeto dessa classe.

    Ela define uma única função, como pede a atividade.
    """

    @abstractmethod
    def calcular(self, pedido: "Pedido") -> float:
        """
        Calcula e retorna o valor do frete para o pedido recebido.

        Parâmetros:
            pedido: o objeto Pedido. A estratégia recebe o pedido inteiro
                    (e não só o peso) para poder usar qualquer informação
                    dele no futuro (peso, valor, destino...) sem precisar
                    mudar a assinatura do método.

        Retorno:
            O valor do frete em reais (float).
        """
        # Método abstrato não tem implementação: quem implementa são as
        # classes concretas abaixo.
        ...


# ---------------------------------------------------------------------------
# PASSO 2 - AS CLASSES CONCRETAS (Concrete Strategies)
# Cada uma contém a lógica que antes era um ramo do if/elif em Pedido.
# ---------------------------------------------------------------------------
class FreteSedex(EstrategiaFrete):
    """SEDEX: taxa fixa de R$ 10,00 + R$ 1,50 por kg."""

    TAXA_FIXA = 10.0      # constantes de classe deixam os números com nome
    VALOR_POR_KG = 1.5    # (evita "números mágicos" soltos no código)

    def calcular(self, pedido: "Pedido") -> float:
        # Lê o peso pelo getter (property) do pedido, sem acessar o
        # atributo privado _peso_kg diretamente (encapsulamento).
        return self.TAXA_FIXA + (pedido.peso_kg * self.VALOR_POR_KG)


class FretePac(EstrategiaFrete):
    """PAC: taxa fixa de R$ 5,00 + R$ 1,00 por kg."""

    TAXA_FIXA = 5.0
    VALOR_POR_KG = 1.0

    def calcular(self, pedido: "Pedido") -> float:
        return self.TAXA_FIXA + (pedido.peso_kg * self.VALOR_POR_KG)


class FreteTransportadora(EstrategiaFrete):
    """TRANSPORTADORA: taxa fixa de R$ 20,00 + R$ 3,00 por kg."""

    TAXA_FIXA = 20.0
    VALOR_POR_KG = 3.0

    def calcular(self, pedido: "Pedido") -> float:
        return self.TAXA_FIXA + (pedido.peso_kg * self.VALOR_POR_KG)


class FreteMotoboy(EstrategiaFrete):
    """MOTOBOY: valor fixo de R$ 15,00, independente do peso."""

    VALOR_FIXO = 15.0

    def calcular(self, pedido: "Pedido") -> float:
        # O parâmetro 'pedido' não é usado aqui, mas precisa existir para
        # respeitar o contrato da interface (mesma assinatura em todas).
        return self.VALOR_FIXO


# ---------------------------------------------------------------------------
# PASSO 5 - TESTE DA EXTENSIBILIDADE
# Novos requisitos do gerente de produto. Repare: para adicioná-los, só foi
# preciso CRIAR classes novas aqui. A classe Pedido NÃO foi tocada.
# É exatamente isso que o Princípio Aberto/Fechado pede.
# ---------------------------------------------------------------------------
class FreteDrone(EstrategiaFrete):
    """DRONE (novo requisito): taxa fixa de R$ 25,00."""

    VALOR_FIXO = 25.0

    def calcular(self, pedido: "Pedido") -> float:
        return self.VALOR_FIXO


class FreteRetiradaLocal(EstrategiaFrete):
    """RETIRADA_LOCAL (novo requisito citado no cenário): custo zero."""

    def calcular(self, pedido: "Pedido") -> float:
        # O cliente busca o produto na loja, então não há frete.
        return 0.0
