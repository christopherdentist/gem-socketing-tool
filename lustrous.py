import random
import sys
import csv
import re

classValues = {"Ornamental Stones":18.0, "Hardstones":1.0, "Semiprecious Stones":40.0, "Fancy Stones":84.0, "Precious Stones":143.0, "Gem Stones":626.0, "Jewel Stones":836.0, "God Stones":0.0}
debug = False

class Gem:
	row = []
	colNames = []
	baseValue = 1.0
	cutModifier = 1.0
	size = 9.0
	sizeTier = "Moderate"
	sizeModifier = 1.0
	magicModifier = 1.0
	magicType = 0
	cutQuality = 1.0
	cutType = "Flawless"
	name = "Phosphophyllite"
	description = "The most wonderful gem. Evidence: http://a.co/d/cdzJ80D"
	type = "God Stones"
	
	def __init__(self, type, columnNames, rowData):
		self.colNames = columnNames
		self.row = rowData
		if (type not in classValues):
			print ("Error: " + str(type) + " is not a known type of gem! The options are:")
			for k,v in classValues.iterItems():
				print ("\t" + str(k))
			print("Double check 's's and capitalization. God Stones will be used as default instead.")
		else:
			self.type = type
		if debug:
			print("Creating new Gem item of type " + str(self.type) + "...")
		self.baseValue = classValues[self.type]
		self.name = self.getName()
		self.description = self.getDescription()
		self.size = self.getSize()
		self.sizeModifier = self.getSizeMod()
		self.magicModifier = self.getMagic()
		self.baseValue = self.baseValue * self.getRarity()
		self.cutQuality, self.cutModifier = self.getCut()
		if debug:
			print(" Done.")

	def getName(self):
		if (len(self.row) < 1):
			return self.name
		return self.row[0].strip()
		
	def getSize(self):
		category = random.randint(1, 100)
		if debug:
			print("\t-- Size tier rolled: " + str(category) + "%", end='')
		self.cutType = self.getCutType(category)
		if category <= 50:
			category = 0
			self.sizeTier = "Small"
			if debug:
				print("; small", end='')
		elif category <= 97:
			category = 1
			self.sizeTier = "Medium"
			if debug:
				print("; medium", end='')
		else:
			category = 2
			self.sizeTier = "Large"
			if debug:
				print("; large", end='')
		if debug:
			print(" and " + self.cutType.lower() + ".")
		w = random.randrange(1, 100)
		if debug:
			print("\t-- Exact size rolled: " + str(w) + "%.")
		if category == 0:
			if w > 96:
				return 8
			elif w > 90:
				return 7
			else:
				return (w - 1) / 15 + 1
		if category == 1:
			if w <= 60:
				return (w - 1) / 15 + 9
			elif w < 80:
				return (w - 61) / 10 + 13
			else:
				return 0.02619 * (w * w) - 4.307 * w + 191.8
		if category == 2:
			if w <= 88:
				return 0.005769 * (w * w) + 0.08423 * w + 29.91
			else:
				return 6.640 * (w * w) - 1207 * w + 5.489e+4

	def getSizeMod(self):
		return -0.00006074 * (self.size * self.size) + 0.1364 * self.size - 0.03630

	def getMagic(self):
		if ('(' in self.name):
			if debug:
				print("\t-- Is magical!")
			count = self.name.count('(')
			if (count > 1):
				self.magicType = 3
				if debug:
					print("\t-- BOTH types of magic!")
				return 3.0
			else:
				if self.name[self.name.index('(') + 1] == 'M':
					self.magicType = 1
					if debug:
						print("\t-- Just M!")
				else:
					self.magicType = 2
					if debug:
						print("\t-- Just I!")
				return 2.0
		return 1.0
		
	def getRarity(self):
		index = -1
		if ("Rarity" in self.colNames):
			index = self.colNames.index("Rarity")
		elif ("rarity" in self.colNames):
			index = self.colNames.index("rarity")
		if (index < 0 or len(self.row[index]) < 1):
			return 1.0
		rarity = self.row[index].strip()
		return float(rarity)
		
	def getDescription(self):
		index = -1
		if ("Description" in self.colNames):
			index = self.colNames.index("Description")
		elif ("description" in self.colNames):
			index = self.colNames.index("description")
		if (index < 0 or len(self.row[index]) < 1):
			return self.description
		return self.row[index].strip()
		
	def getCut(self):
		w = random.randint(1, 100)
		if debug:
			print("\t-- Cut quality rolled: " + str(w) + "%.")
		if w >= 99:
			return ("Quadruple value", 4.0)
		elif w >= 91:
			return ("Triple value", 3.0)
		elif w >= 81:
			return ("Double value", 2.0)
		elif w >= 71:
			return ("Above value", 1.39)
		elif w >= 56:
			return ("Below value", 0.16)
		elif w >= 31:
			return ("Half value", 0.5)
		return ("Uncut", 0.1)
		
	def getCutType(self, factor):
		if factor > 98:
			return "Smooth Polished Cube"
		elif factor > 96:
			return "Smooth Polished Pear"
		elif factor > 94:
			return "Smooth Polished Oval"
		elif factor > 92:
			return "Smooth Polished Sphere"
		elif factor > 90:
			return "Cushion"
		elif factor > 85:
			return "Baguette"
		elif factor > 80:
			return "Scissors"
		elif factor > 75:
			return "Marquise"
		elif factor > 70:
			return "Triangular"
		elif factor > 65:
			return "Pear"
		elif factor > 60:
			return "Oval"
		elif factor > 50:
			return "Emerald"
		elif factor > 45:
			return "Square"
		elif factor > 40:
			return "Table"
		elif factor > 35:
			return "Oval"
		return "Round"
		
	def getValue(self, decimals=2):
		v = self.baseValue * self.cutModifier * self.sizeModifier * self.magicModifier
		if v < 0:
			return 0.1
		else:
			return round(v, decimals)
		
	def getValueGP(self):
		gp = int(self.getValue())
		return gp
	
	def getValueSP(self):
		sp = int(round(self.getValue() * 10, 0))
		return sp
		
	def __str__(self):
		n = self.name
		if self.magicType > 0:
			o = n[:n.index('(')]
			return o.strip()
		return n.strip()

def main():
	colNames = []
	rows = []
	with open('All Stones - Ornamental Stones.csv', encoding='utf-8') as f:
		fReader = csv.reader(f, delimiter=",")
		lines = 0
		for row in fReader:
			if lines == 0:
				for col in row:
					colNames.append(col)
			else:
				rows.append(row)
			lines += 1

	if debug:
		print("Loaded " + str(len(rows)) + " " + colNames[0] + " with " + str(len(colNames) - 1) + " columns.")
	rNum = random.randint(0, len(rows) - 1)
	gem = Gem(colNames[0], colNames, rows[rNum])
	print("The gem that has been generated is " + str(gem) + ", of the " + gem.type + " classification.")
	print("It is " + str(round(gem.size, 1)) + "ct in size", end='')
	if gem.cutQuality != "Uncut":
		print(", with a", end='')
		if gem.cutQuality == "Above value":
			print("n", end='')
		print(" " + gem.cutQuality.lower() + " " + gem.cutType.lower() + " cut.")
	else:
		print(", uncut.")
	if gem.magicType == 1:
		print(" !! " + str(gem) + " is magical in nature !! ")
	if gem.magicType == 2:
		print(str(gem) + " is a luon stone.")
	if gem.magicType == 3:
		print(str(gem) + " is both a luon stone, and magical in nature.")
	print("The value of this " + gem.sizeTier.lower() + " " + str(gem) + " is", end='')
	if (gem.getValueGP() != 0):
		print(" " + str(gem.getValueGP()) + "gp", end='')
	if (gem.getValueSP() != 0):
		print(" " + str(gem.getValueSP() - 10 * gem.getValueGP()) + "sp", end='')
	print(".")
	print("\"" + gem.description + "\"")

if __name__ == "__main__":
	gemsToGenerate = 1
	if len(sys.argv) > 1:
		if sys.argv[1].isnumeric():
			gemsToGenerate = abs(int(sys.argv[1]))
		else:
			debug = True
	print()
	for i in range(gemsToGenerate):
		if (gemsToGenerate > 1):
			print("Gem #" + str(i + 1) + "...")
		main()
		print()
	