class treeNode:
	def __init__(self, board):
		"""
		|	Initializes class variables
		|	Arguments	   : board    | Data struct
		|	Class Variables: board    | Datastruct
		|				   : worth    | int value
		|				   : treeList | list of treeNode class objects
		"""
		self.board = list(board)
		self.worth = self.worthCalc()
		self.childList = []

	def worthCalc(self):
		"""
		|	Calculates the worth of the board based on 'Reinfeld Values'
		|	Arguments: None
		|	Returns  : Numeric sum of the 'worth' of piece on the board
		"""
		worthList = [1, 3, 3, 5, 9, 10000]  # Based on 'Reinfeld Values'
		worth = 0
		for piece in self.board:  # For every piece
			if piece == 0: continue  # If null piece, ignore
			pieceType = piece%10  # Finding piece type
			colour = piece - pieceType  # finding the colour
			if colour == 10: colour = 1  # if it should be plus or minus
			else: colour = -1  
			worth += colour*worthList[pieceType]  # Add the worth
		return(worth)
	
	def genTree(self, player, depth, alpha=-99999999, beta=99999999):
		"""
		|	Generates a tree based on the current board, w/ depth limit
		|	Arguments: depth | the depth limit, current node is depth 0
		|	Arguments: player| the next turn of the tree
		|	Returns  : True or success
		"""
		self.childList = []  # Clearing any pre existing values
		if depth <= 0:  # exit case, if depth is 0 or less than 0
			return(self.worth)  # Return the value of the final node

		# Defining variables
		playerList = [20, 10]
		modeList = [max, min]
		maxEvalList = [-99999999, 99999999]
		totalPosList = []

		nextPlayer = playerList[int(player/10)-1]  # If white, next player is black
		mode = modeList[int(player/10)-1]  # Goal of white is to max black is to min
		maxEval  = maxEvalList[int(player/10)-1]  # Defining a value that will always be smaller for white, and larger for black 

		playerPos = GetPlayerPositions(self.board, player)
		for pos in playerPos:
			moves = GetPieceLegalMoves(self.board, pos)
			for move in moves:
				totalPosList += [[pos, move]]
				
		for move in totalPosList:
			copyBoard = altBoard(self.board, move[0], move[1])
			copyNode = treeNode(copyBoard)
			self.childList += [copyNode]
			mmValue = copyNode.genTree(nextPlayer, depth-1, alpha, beta)

			maxEval = mode(maxEval, mmValue)
			if player == 10: alpha = mode(alpha, mmValue)
			else: beta = min(alpha, mmValue)

			if beta<=alpha:
				break
		return(maxEval)


	def genChildren(self, player):
		"""
		|	Generates Children of Current Board, saves it to self.worthList
		|	Arguments: player | numeric value. 10: white, 20: black
		|	Returns  : True or success
		"""

		'''
		self.childList = []  # Initialising childList to be a non-null value
		playerPositions = GetPlayerPositions(self.board, player)  # Getting all player positions
		for pos in playerPositions:
			moves = GetPieceLegalMoves(self.board, pos)  # Generating moves for given piece
			for move in moves:
				copyBoard =	altBoard(self.board, pos, move)
				self.childList += [treeNode(copyBoard)]
		return(True)
		'''
	def returnByDepth(self):
		"""
		|	Is recursively run, returns a tree in list format and the mmValue 
		|	Arguments: None
		|	Returns  : A tree in list format [worth, board, [[worth1, board1, [...]], [worth2, board2, [...]]]]
		"""
		output = [self.worth, self.board, []]
		for obj in self.childList:
			output[2] +=  obj.returnByDepth()
		return(output)

def genPreCalc(root, player, depth):
	file = open('chessPlayer_Precalc.py', 'w+')
	root.genTree(player, depth)
	file.write('root='+str(root.returnByDepth()))

	'''
	def getmmValue(self, mode):
		"""
		|	Gets the min max value of each node, returns a list of nodes with highest mmValue
		|	Arguments: node | an object of class treeNode
		|			 : mode | 0 for max, 1 for min
		|	Returns  : A list of objects of treeNode
		"""
		"""
		modeList = [max, min]
		modeFunc = modeList[mode]
		nextModeList = [1, 0]
		nextMode = nextModeList[mode]
		worthList = []
		if self.childList == []:
			return(self.worth)
		for childNode in self.childList:
			worthList += [childNode.getmmValue(nextMode)]
		return(modeFunc(worthList))
		"""
	'''
def GetPlayerPositions(board, player):
	"""
	|	Gives a list of player positions
	|	Arguments: board  | Data struct
	|			 : player |	10 white 20 black
	|	Returns  : A list of player positions
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	posList = []

	for i in range(0, numCol*numRow):
		# Finding out if it is Black or White
		tile = board[i]
		cPlayer = tile-(tile%10)

		# Adding the position
		if cPlayer == player:
			posList += [i]
	return(posList)

def GetPieceLegalMoves(board, position):
	"""
	|	Returns a list of all legal positions - excludes moves that would jepordize king
	|	Arguments: board 	| Data structure
	|			 : position | int, index for board
	|	Returns  : A list of valid move positions
	"""
	# Defining Variables
	piece = board[position]
	pieceType = piece%10  # Finding piece type
	enemyList = [20, 10]
	
	ally = piece - pieceType
	enemy = enemyList[int((ally/10)-1)] # Finding Enemy and Ally
	
	moveList = []

	rawMoveList = RawGetPieceLegalMoves(board, position)  # Generating raw list of legal moves
	for move in rawMoveList:  # Filtering moves which would jepordize the king
		copyBoard = altBoard(board, position, move)
		kingPos = pieceFind(copyBoard, ally+5)  # Finding the king in this board
		if kingPos == (-1):  # If there is no king, assume it is an error case
			return(rawMoveList)
		if IsPositionUnderThreat(copyBoard, kingPos, ally) == False:
			moveList += [move]
	return(moveList)

def RawGetPieceLegalMoves(board, position):
	"""
	|	Returns a list of all legal positions - includes moves that would jepordize king
	|	Arguments: board 	| Data structure
	|			 : position | int, index for board
	|	Returns  : A list of valid move positions
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	piece = board[position]
	enemyList = [20, 10]
	helpFuncList = [pwnLegalMoves, knLegalMoves, biLegalMoves,
					roLegalMoves, quLegalMoves, kiLegalMoves]

	pType = piece%10  # Finding piece type
	ally = piece - pType
	enemy = enemyList[int((ally/10)-1)] # Finding Enemy and Ally
	moveList = []

	function = helpFuncList[pType]  # Selecting appropriate function

	# Finding list of allies and enemies
	allyList = GetPlayerPositions(board, ally)
	enemyList = GetPlayerPositions(board, enemy)

	# Calling function
	moveList = function(position, ally, allyList, enemyList)
	return(moveList)

def pwnLegalMoves(position, colour, allyList, enemyList):
	"""
	|	Returns the list of legal moves for the pawn
	|	Arguments: position | the index of the pawn
	|			 : colour	| the colour of the piece
	|			 : allyList | the list of allies
	|			 : enemyList| the list of enemies
	|	Returns  : A List of legal moves
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	direcList = [1, -1]
	moveList = []

	direc = direcList[int((colour/10)-1)]  # Defining Direction

	# Finding current row and column position
	row = int((position-position%numCol)/numCol)
	column = position%numCol

	if row+direc in range(0, numRow, 1):  # If row outside accepted range
		fPos = (row+direc)*numCol + column
		if (fPos not in allyList and fPos not in enemyList):  # Not in allyList or enemyList
			moveList += [fPos]
		if (column + 1 in range(0, numCol, 1) and fPos+1 in enemyList):  # Looking at the right
			moveList += [fPos+1]
		if (column - 1 in range(0, numCol, 1) and fPos-1 in enemyList):  # Looking at the left
			moveList = [fPos-1] + moveList

	return(moveList)

def knLegalMoves(position, colour, allyList, enemyList):
	"""
	|	Returns the list of legal moves for the knight
	|	Arguments: position | the index of the pawn
	|			 : colour	| the colour of the piece
	|			 : allyList | the list of allies
	|			 : enemyList| the list of enemies
	|	Returns  : A List of legal moves
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	direcList = [1, -1]
	moveList = []

	# Finding current row and column position
	row = int((position-position%numCol)/numCol)
	column = position%numCol

	for direc in direcList:  # For both directions
		xVector = direc  # Defining vector from origin
		yVector = 2
		for i in range(0, 4, 1):  # Rotating vector 4 times
			newRow = row + yVector  # If finding newRow and newCol
			newCol = column + xVector
			if newRow in range(0, numRow) and newCol in range(0, numCol):  # If the newRow and newCol is valid
				newPos = newRow*numCol + newCol  # Translating into position
				if newPos not in allyList:  # If there is no ally already in pos
					moveList += [newPos]
			xVector, yVector = yVector, -xVector  # Rotating vector by 90 degrees
	return(moveList)

def biLegalMoves(position, colour, allyList, enemyList):
	"""
	|	Returns the list of legal moves for the bishop
	|	Arguments: position | the index of the pawn
	|			 : colour	| the colour of the piece
	|			 : allyList | the list of allies
	|			 : enemyList| the list of enemies
	|	Returns  : A List of legal moves
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	xVector, yVector = 1, 1
	cnst = 1
	moveList = []

	# Finding current row and column position
	row = int((position-position%numCol)/numCol)
	column = position%numCol

	for i in range(0, 4, 1):  # 4 rotations
		while 1:  # For an undetermined time
			newRow = row + cnst*yVector  # Translating to row and col
			newCol = column + cnst*xVector
			if newRow in range(0, numRow, 1) and newCol in range(0, numCol, 1):
				newPos = newRow*numCol + newCol  # Translating into position
				if newPos not in allyList:  # If not an ally
					moveList += [newPos]  # Adding to move list
					if newPos in enemyList:  # If an enemy stopping here
						xVector, yVector = yVector, -xVector  # If an ally, rotate
						cnst = 1  # reset counter
						break
					cnst += 1  # If not stopped, increasing the constant
					continue  # Re-run while loop
			xVector, yVector = yVector, -xVector  # If an ally, rotate
			cnst = 1  # reset counter
			break  # stop while loop
	return(moveList)

def roLegalMoves(position, colour, allyList, enemyList):
	"""
	|	Returns the list of legal moves for the rook
	|	Arguments: position | the index of the pawn
	|			 : colour	| the colour of the piece
	|			 : allyList | the list of allies
	|			 : enemyList| the list of enemies
	|	Returns  : A List of legal moves
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	xVector, yVector = 0, 1
	cnst = 1
	moveList = []

	# Finding current row and column position
	row = int((position-position%numCol)/numCol)
	column = position%numCol

	for i in range(0, 4, 1):  # 4 rotations
		while 1:  # For an undetermined time
			newRow = row + cnst*yVector  # Translating to row and col
			newCol = column + cnst*xVector
			if newRow in range(0, numRow, 1) and newCol in range(0, numCol, 1):
				newPos = newRow*numCol + newCol  # Translating into position
				if newPos not in allyList:  # If not an ally
					moveList += [newPos]  # Adding to move list
					if newPos in enemyList:  # If an enemy stopping here
						xVector, yVector = yVector, -xVector  # If an ally, rotate
						cnst = 1  # reset counter
						break
					cnst += 1  # If not stopped, increasing the constant
					continue  # Re-run while loop
			xVector, yVector = yVector, -xVector  # If an ally, rotate
			cnst = 1  # reset counter
			break  # stop while loop
	return(moveList)

def quLegalMoves(position, colour, allyList, enemyList):
	"""
	|	Returns the list of legal moves for the queen
	|	Arguments: position | the index of the pawn
	|			 : colour	| the colour of the piece
	|			 : allyList | the list of allies
	|			 : enemyList| the list of enemies
	|	Returns  : A List of legal moves
	"""
	
	# Combination of bishop and rook legal moves
	moveList = []
	moveList += biLegalMoves(position, colour, allyList, enemyList)
	moveList += roLegalMoves(position, colour, allyList, enemyList)
	return(moveList)

def kiLegalMoves(position, colour, allyList, enemyList):
	"""
	|	Returns the list of legal moves for the king
	|	Arguments: position | the index of the pawn
	|			 : colour	| the colour of the piece
	|			 : allyList | the list of allies
	|			 : enemyList| the list of enemies
	|	Returns  : A List of legal moves
	"""
	# Defining Variables
	numCol, numRow = 8, 8
	xVector, yVector = 0, 1
	moveList = []

	# Finding current row and column position
	row = int((position-position%numCol)/numCol)
	column = position%numCol

	for n in range(0, 2, 1):
		for i in range(0, 4, 1):
			newRow = row + yVector  # Translating to row and col
			newCol = column + xVector
			if newRow in range(0, numRow, 1) and newCol in range(0, numCol, 1):
				newPos = newRow*numCol + newCol  # Translating into position
				if newPos not in allyList:  # If not an ally
					moveList += [newPos]
			xVector, yVector = yVector, -xVector  # If an ally, rotate
		xVector, yVector = 1, 1  # starting again with a different vector
	return(moveList)

def IsPositionUnderThreat(board, position, player):
	"""
	|	Returns true or false depending on is the position is under threat
	|	Arguments: board    | Data Structure
	|			 : position | int between [0, 64)
	|			 : player   | int, 10 for white, 20 for black
	|	Returns  : Boolean
	"""
	# Defining variables
	numCol, numRow = 8, 8

	playerTypes = [20, 10]
	direcList = [1, -1]
	direc = direcList[int((player/10)-1)]
	funcList = [pwnLegalMoves, knLegalMoves, biLegalMoves,
				roLegalMoves, quLegalMoves, kiLegalMoves]
	enemy = playerTypes[int((player/10)-1)]
	allyList = GetPlayerPositions(board, player)
	enemyList = GetPlayerPositions(board, enemy)

	# Finding current row and column position
	row = int((position-position%numCol)/numCol)
	column = position%numCol

	if row+direc in range(0, numRow):
		for di in direcList:
			if column+di in range(0, numCol):
				if enemy == board[(row+direc)*numCol+(column+di)]:
					return(True)

	for piece in [2, 3]:
		posList = funcList[piece](position, player, allyList, enemyList)
		for pos in posList:
			if enemy+piece == board[pos] or enemy+4 == board[pos]:
				return(True)

	posList = funcList[1](position, player, allyList, enemyList)
	for pos in posList:
			if enemy+1 == board[pos]:
				return(True)

	posList = funcList[5](position, player, allyList, enemyList)
	for pos in posList:
			if enemy+5 == board[pos]:
				board[pos]
				return(True)
	return(False)

def pieceFind(board, piece):
	"""
	|	Returns an index of the piece
	|	Arguments: board | Data Structure
	|			 : piece | int between [0, 64)
	|	Returns  : integer, if <0 failure, if >=0 valid index
	"""
	counter = 0
	for i in range(0, len(board)):
		if board[i] == piece:
			return(i)
	return(-1)

def altBoard(board, pos, move):
	"""
	|	Returns a varient on the current board 
	|	Arguments: board | Data Structure
	|			 : pos   | Current position
	|			 : move  | Move piece to
	|	Returns  : board | Data Structure
	"""
	copyBoard = list(board)
	copyBoard[move] = copyBoard[pos]
	copyBoard[pos] = 0
	return(copyBoard)

'''
def getmmValue(node, mode):
	"""
	|	Gets the min max value of each node, returns a list of nodes with highest mmValue
	|	Arguments: node | an object of class treeNode
	|			 : mode | 0 for max, 1 for min
	|	Returns  : A list of objects of treeNode
	"""
	modeList = [max, min]
	modeFunc = modeList[mode]
	nextModeList = [1, 0]
	nextMode = nextModeList[mode]
	worthList = []

	if node.childList == []:
		print(node.worth)
		return(node.worth)
	for childNode in node.childList:
		worthList += [getmmValue(childNode, nextMode)]
	return(modeFunc(worthList))
'''