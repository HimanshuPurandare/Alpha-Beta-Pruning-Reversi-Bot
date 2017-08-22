import copy
from collections import defaultdict
from collections import OrderedDict
import math

cutoffdepth = 0

EvalMatrix = [[0 for x in range(8)] for y in range(8)]
EvalMatrix = [[99,-8,8,6,6,8,-8,99],[-8,-24,-4,-3,-3,-4,-24,-8],[8,-4,7,4,4,7,-4,8],[6,-3,4,0,0,4,-3,6],[6,-3,4,0,0,4,-3,6],[8,-4,7,4,4,7,-4,8],[-8,-24,-4,-3,-3,-4,-24,-8],[99,-8,8,6,6,8,-8,99]]

#Class begins:
#Node Class depicting nodes in tree.

class node:
	def __init__(self, Board, player, move, parent, value, alpha, beta, depth):
		self.Board = copy.deepcopy(Board)
		self.player=player	
		self.ValidPositionsForX = defaultdict(list)
		self.ValidPositionsForO = defaultdict(list)
		self.depth = depth
		self.value = value
		self.alpha = alpha
		self.beta = beta
		self.MoveToPlay = []
		self.MoveToPlay = copy.deepcopy(move)
		self.isTerminal = False
		self.parent=parent
		self.children = []
		self.isTerminalNode()
		self.makeMove()
		#self.printMatrix(self.Board) 
		
	def generateChildren(self):
		if self.player == 'X':
			self.findValidPositions()
			for validmoves in self.ValidPositionsForX:
				self.children.append(node(self.Board, self.getOpponent(self.player), self.ValidPositionsForX[validmoves], self, self.value, self.alpha, self.beta, self.depth+1))
		elif self.player == 'O':
			self.findValidPositions()
			for validmoves in self.ValidPositionsForO:
				self.children.append(node(self.Board, self.getOpponent(self.player), self.ValidPositionsForO[validmoves], self, self.value, self.alpha, self.beta, self.depth+1))
				
		
	def getOpponent(self,Player):
		if Player=="X":
			return "O"
		else:
			return "X"
	
	def printMatrix(self,BoardToBePrinted):
		FinalMatrix=""
		for line in BoardToBePrinted:
			for element in line:
				FinalMatrix+=str(element)
			FinalMatrix+="\n"
		print FinalMatrix

	#VALID POSTIONS FOR PLAYER
	def findValidPositions(self):
		if self.player=="X":
			for rows in range(0,8):
				for cols in range(0,8):
					if self.Board[rows][cols]=="X":
						self.checkSouth(rows+1, cols, self.player)	#check south
						self.checkNorth(rows-1, cols, self.player)	#check north
						self.checkEast(rows, cols+1, self.player)	#check east
						self.checkWest(rows, cols-1, self.player)	#check west
						self.checkSouthEast(rows+1, cols+1, self.player)	#check south-east
						self.checkNorthEast(rows-1, cols+1, self.player)	#check north-east
						self.checkSouthWest(rows+1, cols-1, self.player)	#check south-west
						self.checkNorthWest(rows-1, cols-1, self.player)	#check north-west
			self.ValidPositionsForX = OrderedDict(sorted(self.ValidPositionsForX.items(), key=lambda t: t[0]))
			if not self.ValidPositionsForX:
				print "Pass"
		else:
			for rows in range(0,8):
				for cols in range(0,8):
					if self.Board[rows][cols]=="O":
						self.checkSouth(rows+1, cols, self.player)	#check south
						self.checkNorth(rows-1, cols, self.player)	#check north
						self.checkEast(rows, cols+1, self.player)	#check east
						self.checkWest(rows, cols-1, self.player)	#check west
						self.checkSouthEast(rows+1, cols+1, self.player)	#check south-east
						self.checkNorthEast(rows-1, cols+1, self.player)	#check north-east
						self.checkSouthWest(rows+1, cols-1, self.player)	#check south-west
						self.checkNorthWest(rows-1, cols-1, self.player)	#check north-west
			self.ValidPositionsForO = OrderedDict(sorted(self.ValidPositionsForO.items(), key=lambda t: t[0]))
			if not self.ValidPositionsForO:
				print "Pass"
			
								
	def checkNorth(self,rows, cols, Player):
		inirows=rows+1
		if Player == "X":
			ReachedEndWithoutFindingO = True
		else:
			ReachedEndWithoutFindingX = True
		
		for northdir in xrange(rows, 0, -1):
			if self.Board[northdir][cols]==str(self.getOpponent(Player)):
				if Player == "X":
					ReachedEndWithoutFindingO=False
				else:
					ReachedEndWithoutFindingX=False
				continue
			if self.Board[northdir][cols]==str(Player):
				break
			if self.Board[northdir][cols]=="*":
				if Player == "X":
					if not ReachedEndWithoutFindingO:
						self.ValidPositionsForX[(northdir,cols)].append((northdir,cols))
						for count in range(northdir, inirows):
							self.ValidPositionsForX[(northdir,cols)].append((count,cols))
				else:
					if not ReachedEndWithoutFindingX:
						self.ValidPositionsForO[(northdir,cols)].append((northdir,cols))
						for count in range(northdir, inirows):
							self.ValidPositionsForO[(northdir,cols)].append((count,cols))
				break
	
	def checkSouth(self,rows, cols, Player):
		#check south
		inirow = rows-1
		if Player == "X":
			ReachedEndWithoutFindingO = True
		else:
			ReachedEndWithoutFindingX=True
		for southdir in range(rows, 8):
			if self.Board[southdir][cols]==str(self.getOpponent(Player)):
				if Player == "X":
					ReachedEndWithoutFindingO=False
				else:
					ReachedEndWithoutFindingX=False
				continue
			if self.Board[southdir][cols]==str(Player):
				break
			if self.Board[southdir][cols]=="*":
				if Player == "X":
					if not ReachedEndWithoutFindingO:
						self.ValidPositionsForX[(southdir,cols)].append((southdir,cols))
						for count in range(inirow, southdir):
							self.ValidPositionsForX[(southdir,cols)].append((count,cols))
				else:
					if not ReachedEndWithoutFindingX:
						self.ValidPositionsForO[(southdir,cols)].append((southdir,cols))
						for count in range(inirow, southdir):
							self.ValidPositionsForO[(southdir,cols)].append((count,cols))
				break
			
	def checkEast(self,rows, cols, Player):
		#check East
		inicols=cols-1
		if Player == "X":
			ReachedEndWithoutFindingO = True
		else:
			ReachedEndWithoutFindingX = True
		for eastdir in range(cols, 8):
			if self.Board[rows][eastdir]==str(self.getOpponent(Player)):
				if Player == "X":
					ReachedEndWithoutFindingO=False
				else:
					ReachedEndWithoutFindingX=False
				continue
			if self.Board[rows][eastdir]==str(Player):
				break
			if self.Board[rows][eastdir]=="*":
				if Player == "X":
					if not ReachedEndWithoutFindingO:
						self.ValidPositionsForX[(rows,eastdir)].append((rows,eastdir))
						for count in range(inicols, eastdir):
							self.ValidPositionsForX[(rows,eastdir)].append((rows, count))
				else:
					if not ReachedEndWithoutFindingX:
						self.ValidPositionsForO[(rows,eastdir)].append((rows,eastdir))
						for count in range(inicols, eastdir):
							self.ValidPositionsForO[(rows,eastdir)].append((rows, count))
				break
			
	def checkWest(self,rows, cols, Player):
		#check East
		inicols = cols+1
		if Player == "X":
			ReachedEndWithoutFindingO = True
		else:
			ReachedEndWithoutFindingX = True

		for westdir in xrange(cols, 0, -1):
			if self.Board[rows][westdir]==str(self.getOpponent(Player)):
				if Player == "X":
					ReachedEndWithoutFindingO=False
				else:
					ReachedEndWithoutFindingX=False
				continue
			if self.Board[rows][westdir]==str(Player):
				break
			if self.Board[rows][westdir]=="*":
				if Player == "X":
					if not ReachedEndWithoutFindingO:
						self.ValidPositionsForX[(rows,westdir)].append((rows,westdir))
						for count in range(westdir,inicols):
							self.ValidPositionsForX[(rows,westdir)].append((rows, count))
				else:
					if not ReachedEndWithoutFindingX:
						self.ValidPositionsForO[(rows,westdir)].append((rows,westdir))
						for count in range(westdir,inicols):
							self.ValidPositionsForO[(rows,westdir)].append((rows, count))
				break

	def checkSouthEast(self,rows, cols, Player):
		#check south east
		inirows = rows-1
		inicols = cols-1
		if Player == "X":
			ReachedEndWithoutFindingO = True
		else:
			ReachedEndWithoutFindingX = True

		for southdir,eastdir in zip(range(rows, 8),range(cols, 8)):
			if southdir >= 8 or eastdir >=8:
				break
			if self.Board[southdir][eastdir]==str(self.getOpponent(Player)):
				if Player == "X":
					ReachedEndWithoutFindingO=False
				else:
					ReachedEndWithoutFindingX=False
				continue
			if self.Board[southdir][eastdir]==str(Player):
				break
			if self.Board[southdir][eastdir]=="*":
				#my_list=[]
				if Player == "X":
					if not ReachedEndWithoutFindingO:
						self.ValidPositionsForX[(southdir,eastdir)].append((southdir,eastdir))
						for count1, count2 in zip(range(inirows, southdir),range(inicols,eastdir)):
							self.ValidPositionsForX[(southdir,eastdir)].append((count1, count2))
				else:
					if not ReachedEndWithoutFindingX:
						self.ValidPositionsForO[(southdir,eastdir)].append((southdir,eastdir))
						for count1, count2 in zip(range(inirows, southdir),range(inicols,eastdir)):
							self.ValidPositionsForO[(southdir,eastdir)].append((count1, count2))
				break
			
	def checkNorthEast(self,rows, cols, Player):
		#check north east
		inirows = rows+1
		inicols = cols-1
		if Player == "X":
			ReachedEndWithoutFindingO = True
		else:
			ReachedEndWithoutFindingX = True

		for northdir,eastdir in zip(xrange(rows, 0, -1),range(cols, 8)):
			if northdir < 0 or eastdir >=8:
				break
			if self.Board[northdir][eastdir]==str(self.getOpponent(Player)):
				if Player == "X":
					ReachedEndWithoutFindingO=False
				else:
					ReachedEndWithoutFindingX=False
				continue
			if self.Board[northdir][eastdir]==str(Player):
				break
			if self.Board[northdir][eastdir]=="*":
				if Player == "X":
					if not ReachedEndWithoutFindingO:
						self.ValidPositionsForX[(northdir,eastdir)].append((northdir,eastdir))
						for count1, count2 in zip(xrange(inirows,northdir,-1),range(inicols,eastdir)):
							self.ValidPositionsForX[(northdir,eastdir)].append((count1, count2))
				else:
					if not ReachedEndWithoutFindingX:
						self.ValidPositionsForO[(northdir,eastdir)].append((northdir,eastdir))
						for count1, count2 in zip(xrange(inirows,northdir,-1),range(inicols,eastdir)):
							self.ValidPositionsForO[(northdir,eastdir)].append((count1, count2))
				break

	def checkSouthWest(self,rows, cols, Player):
		#check south west
		inirows = rows-1
		inicols = cols+1
		if Player == "X":
			ReachedEndWithoutFindingO = True
		else:
			ReachedEndWithoutFindingX = True

		for southdir,westdir in zip(range(rows, 8),xrange(cols, 0, -1)):
			if southdir >= 8 or westdir < 0:
				break
			if self.Board[southdir][westdir]==str(self.getOpponent(Player)):
				if Player == "X":
					ReachedEndWithoutFindingO=False
				else:
					ReachedEndWithoutFindingX=False
				continue
			if self.Board[southdir][westdir]==str(Player):
				break
			if self.Board[southdir][westdir]=="*":
				if Player == "X":
					if not ReachedEndWithoutFindingO:
						self.ValidPositionsForX[(southdir,westdir)].append((southdir,westdir))
						for count1, count2 in zip(range(inirows, southdir),xrange(inicols,westdir,-1)):
							self.ValidPositionsForX[(southdir,westdir)].append((count1,count2))
				else:
					if not ReachedEndWithoutFindingX:
						self.ValidPositionsForO[(southdir,westdir)].append((southdir,westdir))
						for count1, count2 in zip(range(inirows, southdir),xrange(inicols,westdir,-1)):
							self.ValidPositionsForO[(southdir,westdir)].append((count1,count2))
				break

	def checkNorthWest(self,rows, cols, Player):
		#check North west
		inirows = rows+1
		inicols = cols+1
		if Player == "X":
			ReachedEndWithoutFindingO = True
		else:
			ReachedEndWithoutFindingX = True

		for northdir,westdir in zip(xrange(rows, 0, -1),xrange(cols, 0, -1)):
			if northdir < 0 or westdir < 0:
				break
			if self.Board[northdir][westdir]==str(self.getOpponent(Player)):
				if Player == "X":
					ReachedEndWithoutFindingO=False
				else:
					ReachedEndWithoutFindingX=False
				continue
			if self.Board[northdir][westdir]==str(Player):
				break
			if self.Board[northdir][westdir]=="*":
				if Player == "X":
					if not ReachedEndWithoutFindingO:
						self.ValidPositionsForX[(northdir,westdir)].append((northdir,westdir))
						for count1, count2 in zip(xrange(inirows, northdir, -1),xrange(inicols, westdir, -1)):
							self.ValidPositionsForX[(northdir,westdir)].append((count1, count2))
				else:
					if not ReachedEndWithoutFindingX:
						self.ValidPositionsForO[(northdir,westdir)].append((northdir,westdir))
						for count1, count2 in zip(xrange(inirows, northdir, -1),xrange(inicols, westdir, -1)):
							self.ValidPositionsForO[(northdir,westdir)].append((count1, count2))
				break

	def makeMove(self):
		if self.MoveToPlay:
			for move in self.MoveToPlay:
				self.Board[move[0]][move[1]] = self.getOpponent(self.player)

		'''
		print "MoveToPlay: ", self.MoveToPlay
		print "Player: ", self.player
		print "alpha: ", self.alpha
		print "value: ", self.value
		print "beta: ", self.beta
		self.utility()
		print "utility value: ", self.value
		print "Board:"
		self.printMatrix(self.Board)
		self.findValidPositions()
		print "ValidPositionsForX: "
		print self.ValidPositionsForX
		print "\n"
		for item in self.ValidPositionsForX:
			print item, " : ", self.ValidPositionsForX[item]
			
		print "ValidPositionsForO: "
		for item in self.ValidPositionsForO:
			print item, " : ", self.ValidPositionsForO[item]
		'''
		
	def utility(self):
		SumP = 0
		SumO = 0
		for row in range(8):
			for col in range(8):
				if self.Board[row][col] == self.player:
					SumP = SumP + EvalMatrix[row][col]
				elif self.Board[row][col] == self.getOpponent(self.player):
					SumO = SumO + EvalMatrix[row][col]
		self.value = SumP - SumO
		
	def isTerminalNode(self):
		global cutoffdepth
		#print cutoffdepth == self.depth, self.depth, cutoffdepth
		if cutoffdepth == self.depth:
			self.isTerminal = True
			#print "Terminal"
		
#Class definition Completed
		
def readInput():
		global cutoffdepth
		Board = [['.' for x in range(8)] for y in range(8)]
		fname="input.txt"

		with open(fname) as f:
			content=f.readlines()
	
		content=[x.strip() for x in content]

		lineno = 0
		rows=0
		cols=0
		for x in content:
			if lineno==0:
				player=x
			elif lineno==1:
				cutoffdepth=int(x)
			else:
				cols=0
				for character in x:
					Board[rows][cols] = str(character)
					cols=cols+1
				rows=rows+1
			lineno+=1
		return Board, player
		
def MaxValue(Node):
	if Node.isTerminal:
		Node.utility()
		if Node.MoveToPlay:
			print Node.MoveToPlay[0], Node.depth, Node.value, Node.alpha, Node.beta, Node.player
		else:
			print "Pass", Node.depth, Node.value, Node.alpha, Node.beta, Node.player
		return Node.value
		
	v = -float("inf")
	#Node.findValidPositions()
	Node.generateChildren()
	
	for child in Node.children:
		if Node.MoveToPlay:
			print Node.MoveToPlay[0], Node.depth, Node.value, Node.alpha, Node.beta, Node.player
		else:
			print "Pass", Node.depth, Node.value, Node.alpha, Node.beta, Node.player
		v=max(v,MinValue(child))
		if v >= Node.beta:
			Node.value = v
			if Node.MoveToPlay:
				print Node.MoveToPlay[0], Node.depth, Node.value, Node.alpha, Node.beta, Node.player
			else:
				print "Pass", Node.depth, Node.value, Node.alpha, Node.beta, Node.player
			return v
		Node.alpha=max(v,Node.alpha)
	Node.value = v
	if Node.MoveToPlay:
		print Node.MoveToPlay[0], Node.depth, Node.value, Node.alpha, Node.beta, Node.player
	else:
		print "Pass", Node.depth, Node.value, Node.alpha, Node.beta, Node.player
	return v
		
def MinValue(Node):
	if Node.isTerminal:
		Node.utility()
		if Node.MoveToPlay:
			print Node.MoveToPlay[0], Node.depth, Node.value, Node.alpha, Node.beta, Node.player
		else:
			print "Pass", Node.depth, Node.value, Node.alpha, Node.beta, Node.player
		return Node.value
		
	v = float("inf")
	#Node.findValidPositions()
	Node.generateChildren()
	
	for child in Node.children:
		if Node.MoveToPlay:
			print Node.MoveToPlay[0], Node.depth, Node.value, Node.alpha, Node.beta, Node.player
		else:
			print "Pass", Node.depth, Node.value, Node.alpha, Node.beta, Node.player
		v=min(v,MaxValue(child))
		if v <= Node.alpha:
			Node.value = v
			if Node.MoveToPlay:
				print Node.MoveToPlay[0], Node.depth, Node.value, Node.alpha, Node.beta, Node.player
			else:
				print "Pass", Node.depth, Node.value, Node.alpha, Node.beta, Node.player
			return v
		Node.beta=min(v,Node.beta)
	Node.value = v
	if Node.MoveToPlay:
		print Node.MoveToPlay[0], Node.depth, Node.value, Node.alpha, Node.beta, Node.player
	else:
		print "Pass", Node.depth, Node.value, Node.alpha, Node.beta, Node.player
	return v
		
def main():
	iniboard = [['.' for x in range(8)] for y in range(8)]
	iniplayer = "X"

	iniboard, iniplayer = readInput()
	print "cutoffdepth", cutoffdepth
	root = node(iniboard, iniplayer, [], None, -float("inf"), -float("inf"), float("inf"), 0)
	print "Playing now"
	MaxValue(root)
	#root.findValidPositions()
	#root.generateChildren()
	#print root.children
	#print "---------------------------"
	#if root.ValidPositionsForX:
	#	new_node = node(root.Board, "O", root.ValidPositionsForX[root.ValidPositionsForX.keys()[0]])
	#	new_node.makeMove()

	#print "cutoffdepth: ",cutoffdepth
	
main()
