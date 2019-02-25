
from solver import *
import copy
import queue

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        for move in self.gm.getMovables():
            self.gm.makeMove(move)
            gamestate = GameState(self.gm.getGameState(), self.currentState.depth+1, move)
            self.gm.reverseMove(move)
            if gamestate not in self.visited:
                gamestate.parent = self.currentState
                self.currentState.children.append(gamestate)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        if self.currentState.state == self.victoryCondition:
            return True
        
        self.visited[self.currentState] = True
        for nextState in self.currentState.children:
            if nextState in self.visited:
                continue
            self.gm.makeMove(nextState.requiredMovable)
            self.currentState = nextState
            for move in self.gm.getMovables():
                self.gm.makeMove(move)
                gamestate = GameState(self.gm.getGameState(), self.currentState.depth+1, move)
                self.gm.reverseMove(move)
                if gamestate not in self.visited:
                    gamestate.parent = self.currentState
                    self.currentState.children.append(gamestate)
            return False
        
        if self.currentState.requiredMovable:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)
        self.gmc = copy.deepcopy(gameMaster)
        self.currentState.requiredMovable = []
        self.q = queue.Queue()

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        state = self.currentState
        if state.state == self.victoryCondition:
            return True
        self.gm = copy.deepcopy(self.gmc)
        self.q.put(state)
        while not self.q.empty():
            qpop = self.q.get()
            if qpop not in self.visited:
                break
            if qpop.requiredMovable != []:
                continue
            for move in self.gm.getMovables():
                self.gm.makeMove(move)
                gamestate = GameState(self.gm.getGameState(), state.depth+1, [move])
                self.gm.reverseMove(move)
                if gamestate not in self.visited:
                    gamestate.parent = qpop
                    self.q.put(gamestate)
        self.visited[qpop] = True
        
        for move in qpop.requiredMovable:
            self.gm.makeMove(move)
        
        for move in self.gm.getMovables():
            self.gm.makeMove(move)
            moves = copy.copy(qpop.requiredMovable)
            moves.append(move)
            gamestate = GameState(self.gm.getGameState(), state.depth+1, moves)
            self.gm.reverseMove(move)
            if gamestate not in self.visited:
                gamestate.parent = qpop
                self.q.put(gamestate)
                
        self.currentState = copy.deepcopy(qpop)
        return False
