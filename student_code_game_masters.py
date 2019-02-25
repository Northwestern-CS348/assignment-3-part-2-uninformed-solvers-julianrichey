from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        facts = ['fact: (on ?X peg1)', 'fact: (on ?X peg2)', 'fact: (on ?X peg3)']
        peglist = [[],[],[]]

        for i, fact in enumerate(facts):
            bindings = self.kb.kb_ask(parse_input(fact))
            if bindings:
                for disk in bindings:
                    for bind in disk.bindings:
                        peglist[i].append(int(str(bind.constant)[-1]))
        
        return (tuple(sorted(peglist[0])), tuple(sorted(peglist[1])), tuple(sorted(peglist[2])))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        disk = movable_statement.terms[0]
        pegA = movable_statement.terms[1]
        pegB = movable_statement.terms[2]

        self.kb.kb_retract(Fact(Statement(['on', disk, pegA])))
        self.kb.kb_assert(Fact(Statement(['on', disk, pegB])))
        self.kb.kb_retract(Fact(Statement(['on_top', disk, pegA])))
        self.kb.kb_assert(Fact(Statement(['on_top', disk, pegB])))

        state = self.getGameState()
        pegAcontents = state[int(str(pegA)[-1])-1]
        if pegAcontents:
            self.kb.kb_assert(Fact(Statement(['on_top', 'disk'+str(pegAcontents[0]), pegA])))
        else:
            self.kb.kb_assert(Fact(Statement(['empty', pegA])))
        
        pegBcontents = state[int(str(pegB)[-1])-1]
        if pegBcontents[1:]:
            self.kb.kb_retract(Fact(Statement(['on_top', 'disk'+str(pegBcontents[1]), pegB])))
        else:
            self.kb.kb_retract(Fact(Statement(['empty', pegB])))
        
    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        rowlist = [[0,0,0], [0,0,0], [0,0,0]]
        for y in range(3):
            for x in range(3):
                bindingslist = self.kb.kb_ask(parse_input('fact: (pos ?tile pos' + str(x+1) + ' pos' + str(y+1) + ')'))
                if bindingslist:
                    rowlist[y][x] = int(str(bindingslist).split(':')[2].split('\n')[0][-1])
                else:
                    rowlist[y][x] = -1
        return (tuple(rowlist[0]), tuple(rowlist[1]), tuple(rowlist[2]))

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        piece = movable_statement.terms[0]
        initX = movable_statement.terms[1]
        initY = movable_statement.terms[2]
        targX = movable_statement.terms[3]
        targY = movable_statement.terms[4]

        self.kb.kb_retract(Fact(Statement(['pos', piece, initX, initY])))
        self.kb.kb_assert(Fact(Statement(['pos', piece, targX, targY])))
        self.kb.kb_retract(Fact(Statement(['empty', targX, targY])))
        self.kb.kb_assert(Fact(Statement(['empty', initX, initY])))

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
