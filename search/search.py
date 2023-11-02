# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem: SearchProblem):

    # inicializa a pilha para a busca em pronfudidade
    stack = util.Stack()

    # Criar um conjunto para rastear os nós vizinhos
    visited = set()

    # Comece com o estado inicial do problema
    start_stade = problem.getStartState()

    # empurre o estado inicial para a pilha com uma lista vazia de açoes
    stack.push((start_stade, []))

    while not stack.isEmpty():
        state, actions = stack.pop()

        # verifique se o estado atual é o objetivo
        if problem.isGoalState(state):
            return actions
        # marque o estado atual como visitado
        visited.add(state)

        # obtenha os sucessores do estado atual
        successors = problem.getSuccessors(state)
        for successor, action, _ in successors:
            if successor not in visited:
                new_actions = actions + [action]
                stack.push((successor, new_actions))
    # se nao encontrarmo uma soluçao, retornaremos uma lista vazia

    return []


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""

    # Inicializa a fila para a busca em largura
    queue = util.Queue()

    # Cria um conjunto para rastrear os nós vizinhos que já foram visitados
    visited = []

    # Comece com o estado inicial do problema
    start_state = problem.getStartState()

    # Empurre o estado inicial para a fila com uma lista vazia de ações
    queue.push((start_state, []))

    while not queue.isEmpty():
        state, actions = queue.pop()

        # Verifique se o estado atual é o objetivo
        if problem.isGoalState(state):
            return actions

        # Marque o estado atual como visitado
        visited.append(state)

        # Obtém os estados na fila (para evitar ciclos)
        queue_states = [t[0] for t in queue.list]

        # #No primeiro código, a verificação de sucessores não adiciona um sucessor à fila se o sucessor já estiver na fila.
        # Isso evita ciclos diretamente.
        # No segundo código, essa verificação é feita apenas para estados que já foram visitados (next_state not in visited).
        # A verificação para estados na fila é feita com queue_states.

        # Para cada gsucessor do estado atual
        for successor in problem.getSuccessors(state):
            next_state, action = successor[0], successor[1]

            # Verifica se o sucessor não foi visitado e não está na fila
            if next_state not in visited and next_state not in queue_states:
                # Adicione o sucessor à fila com as ações atualizadas
                queue.push((next_state, actions + [action]))


    # Retorna uma lista vazia se não encontrar o objetivo
    return []




    # se nao encontrarmo uma soluçao, retornaremos uma lista vazia

# function BREADTH - FIRST - SEARCH(problem)returns a solution node or failure
def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    # inicializa a pilha para a busca em pronfudidade
    queue = util.PriorityQueue()

    # Criar um conjunto para rastear os nós vizinhos
    visited = set()

    # Comece com o estado inicial do problema
    start_stade = problem.getStartState()

    # empurre o estado inicial para a pilha com uma lista vazia de açoes
    queue.push((start_stade, [], 0), 0)

    while not queue.isEmpty():
        state, actions, my_value = queue.pop()

        # verifique se o estado atual é o objetivo
        if problem.isGoalState(state):
            return actions

        # obtenha os sucessores do estado atual
        if state not in visited:
            successors = problem.getSuccessors(state)
            for successor, action, value in successors:
                new_actions = actions + [action]
                queue.push((successor, new_actions, my_value + value), my_value + value)

        # marque o estado atual como visitado
        visited.add(state)
    # se nao encontrarmo uma soluçao, retornaremos uma lista vazia

    return []


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    # Inicializa a fila de prioridade para a busca A*
    pqueue = util.PriorityQueue()

    # Cria um conjunto para rastrear os nós visitados
    visited = []

    # Comece com o estado inicial do problema
    start_state = problem.getStartState()

    # Empurre o estado inicial para a fila com uma lista vazia de ações e um custo acumulado inicial de 0
    pqueue.push((start_state, [], 0), 0)

    while not pqueue.isEmpty():
        state, actions, costs = pqueue.pop()

        # Verifique se o estado atual é o objetivo
        if not state in visited:
            visited.append(state)

            if problem.isGoalState(state):
                return actions

            for state, action , cost in problem.getSuccessors(state):
                if not state in visited:
                    heuristicCost = costs + cost + heuristic(state, problem)
                    pqueue.push((state, actions + [action], costs + cost), heuristicCost)

    # Se não encontrarmos uma solução, retornaremos uma lista vazia

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch


