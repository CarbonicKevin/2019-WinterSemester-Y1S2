from chessPlayer_lib import *
from chess_board_lib import *

board = boardInit()
printBoard(board)
root = treeNode(board)
root.genTree(10, 4)
print(root.childList)

'''
root.genTree(20, 4)  # White goes first
print(len(root.childList))
print(root.childList)
'''
#print(root.getmmValue(0))