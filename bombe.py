from Enigma import Enigma
import queue
def charToInt(char):
    return ord(char.upper()) - 65

def intToChar(num):
    return chr(num + 65)

def findCribPosition(cipherText, crib):
    positions = []
    cipherText = cipherText.upper()
    crib = crib.upper()
    diff = len(cipherText) - len(crib)
    if diff < 0:
        return None
    for cipherTextOffset in range(0, diff + 1):
        isValidCrib = True
        for cribOffset in range(0, len(crib)):
            if cipherText[cribOffset + cipherTextOffset] == crib[cribOffset]:
                isValidCrib = False
                break
        if isValidCrib:
            positions.append(cipherTextOffset)
    return positions
def boolListToInt(array):
    newList = []
    for i in range(0, len(array)):
        newList.append(1 if array[i] else 0)
    return newList

class edge():
    def __init__(self, node, wegiht):
        self.node = node
        self.weight = weight

class node():
    def __init__(self, letter):
        self.letter = letter

    def addNode(self, node, weight):
        pass

class Menu():
    def __init__(self):
        self.letterCycles = []
        self.weightCycles = []
        self.diaganolBoard = []
        self.cycleCount = 0
        self.currCycle = 0
        self.menuSize = 0

    def addCycle(self, letters, weights):
        self.letterCycles.append(letters)
        self.weightCycles.append(weights)
        self.cycleCount += 1
        self.menuSize += len(letters)

    def getCycles(self):
        if self.currCycle >= self. cycleCount:
            return None
        return [self.letterCycles[self.currCycle], self.weightCycles[self.currCycle]]

    def getNextCycle(self):
        if self.currCycle >= self. cycleCount:
            return None
        self.currCycle += 1
        return [self.letterCycles[self.currCycle], self.weightCyclesp[self.currCycle]]

    def restCurrCycle(self):
        self.currCycle = 0

    def size(self):
        return self.menuSize


class testPlugBoard():
    def __init__(self):
        # self.permutation = range(0, 26)
        self.permutation = []
        for i in range(0, 26):
            self.permutation.append(i)

    def trySetting(self, letter1, letter2):
        print(letter1, letter2)
        letter1 = charToInt(letter1)
        letter2 = charToInt(letter2)
        rest = self.resetSetting(letter1)
        rest = rest or self.resetSetting(letter2)
        self.permutation[letter1] = letter2
        self.permutation[letter2] = letter1
        return rest

    def resetSetting(self, num, caller=-1):
        if not self.permutation[num] == num and not self.permutation[num] == caller:
            reset = self.resetSetting(self.permutation[num], num)
        self.permutation[num] = num

    def encode(self, letter):
        return self.permutation[charToInt(letter)]

    def CencodeC(self, letter):
        return intToChar(self.permutation[charToInt(letter)])

    def isSetC(self, letter):
        return letter == intToChar(self.permutation[charToInt(letter)])

    def isSetN(self, num):
        return num == self.permutation[charToInt(num)]

    def printBoard(self):
        print(self.permutation)


class Bombe():
    def __init__(self, menu):
        self.diagonalBoard = []
        self.menu = menu
        self.restDiagonalboard()
        self.baseEnigma = Enigma(rotors="412", rotorPositions="AAB", reflector="2")


    def restDiagonalboard(self):
        for i in range(0, 26):
            self.diagonalBoard.append([False]*26)


    def newPlugSetting(self, letterNum):
        for i in range(0, 26):
            if not self.diagonalBoard[letterNum][i]:
                return i
        return -1


    def loop(self, menu):
        self.baseEnigma = Enigma(rotors="123", rotorPositions="AAG", reflector="2")
        result = self.testMenu()
        while not result:
            self.baseEnigma.next()
            result = self.testMenu()

    def markDiagonalBoard(self, l1, l2):
        n1 = charToInt(l1)
        n2 = charToInt(l2)
        if self.diagonalBoard[n1][n2] and self.diagonalBoard[n2][n1]:
            return True
        self.diagonalBoard[n1][n2] = True
        self.diagonalBoard[n2][n1] = True
        return False



    def testMenu(self):
        enigmas = [self.baseEnigma.copy()]
        for i in range(1, self.menu.size()):
            enigmas.append(enigmas[i-1].copyNext())

        currCycle = self.menu.getCycles()
        if not currCycle:
            return False
        letters, weights = currCycle
        newSetting = "R" #intToChar(self.newPlugSetting(charToInt(letters[0])))
        print(newSetting)
        plugboard = testPlugBoard()
        # generate a plug setting
        plugboard.trySetting(letters[0], newSetting)
        self.markDiagonalBoard(letters[0], newSetting)

        contradiction = True
        while contradiction:
            print()
            contradiction = False
            for i in range(0, len(letters)):
                # Encode letter
                print("Starting letter: " + letters[i])
                encodedLetter = plugboard.CencodeC(letters[i])
                print("Plug board encodes: " + encodedLetter)
                print("weight is: " + str(weights[i]-1))
                encodedLetter = enigmas[weights[i]-1].encode(encodedLetter, step=False)
                encodedLetter = plugboard.CencodeC(encodedLetter)
                print("Letter it encodes to: " + encodedLetter)

                # Check encoded letter is next letter in cycle
                nextIndex = i + 1
                if nextIndex >= len(letters):
                    nextIndex = 0
                print(nextIndex)
                if (not encodedLetter == letters[nextIndex]):
                    print("What it needs to be: " + letters[nextIndex])
                    if (plugboard.isSetC(encodedLetter)):
                        encodedLetter = plugboard.CencodeC(encodedLetter)
                        contradiction = True
                    print("Trying new plugboard setting: " + encodedLetter + letters[nextIndex])
                    plugboard.trySetting(encodedLetter, letters[nextIndex])
                    if self.markDiagonalBoard(encodedLetter, letters[nextIndex]):
                        contradiction = False
                        break
                else:
                    self.markDiagonalBoard(encodedLetter, plugboard.CencodeC(encodedLetter))

        print(plugboard.printBoard())
        self.printDiagonalBoard()

    def printDiagonalBoard(self):
        for i in range(0, 26):
            print(intToChar(i) + str(boolListToInt(self.diagonalBoard[i])))





        # for i in range(0, len(letters)):
        #     encodedLetter = plugboard.encode(letter[i])
        #     encodedLetter = enigmas[weights[i]].encode(intToChar(encodedLetter), step=False)
        #     encodedLetter = plugboard.encode(encodedLetter)
        #     nextIndex = i + 1
        #     if nextIndex >= len(letters):
        #         nextIndex = 0
        #     if (not encodedLetter == letters[nextIndex]):
                # check if a plug board setting already exists
                # If it exist a contradiction is found, undo the 











if __name__ == "__main__":
    print(findCribPosition("zbssdidmso", "hello"))
    m = Menu()
    m.addCycle(["R", "B" , "L", "V", "A", "E", "C", "N", "Q"], [1, 8, 12, 18, 5, 10, 3, 14, 6])
    m.addCycle(["M", "E", "A"], [7, 14, 9])
    m.menuSize = 20
    b = Bombe(m)
    b.testMenu()


