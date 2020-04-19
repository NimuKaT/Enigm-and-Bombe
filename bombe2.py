from Enigma import Enigma
import queue

def charToInt(char):
    return ord(char.upper()) - 65

def intToChar(num):
    return chr(num + 65)

def boolListToInt(array):
    newList = []
    for i in range(0, len(array)):
        newList.append(1 if array[i] else 0)
    return newList

class Menu():
    def __init__(self):
        self.menu = []
        self.expected = []
        self.size = 1
        for i in range(0, 26):
            self.expected.append([])
    # Adds a node that connects the two characters with weight n
    def addNode(self, c1, c2, n):
        # if len(c1) != 1 or not c1.isalpha() or len(c2) != 1 or not c2.isalpha() != 1 or n <= 0:
        #     return False
        self.menu.append((c1, c2, n))
        self.expected[charToInt(c1)].append((c2, n))
        self.expected[charToInt(c2)].append((c1, n))
        self.size += 1
        # print("Added node")

    def getExpected(self, char):
        return self.expected[charToInt(char)]

    def getSize(self):
        for i in range(0, 26):
            print(len(self.expected[i]))
        return self.size

class Bombe():
    def __init__(self, menu, rotors="412", rotorPositions="AAA", reflector="2"):
        self.menu = menu
        self.baseEnigma = Enigma(rotors=rotors, rotorPositions=rotorPositions, reflector=reflector)
        self.q = queue.Queue()
        self.visited = set()
        self.resetDiagonalBoard()

    def run(self):
        enigmas = [self.baseEnigma.copy()]
        for i in range(1, self.menu.getSize()):
            enigmas.append(enigmas[i-1].copyNext())
        if(self.q.empty()):
            self.printDiagonalBoard()
        while not self.q.empty():
            plugs = self.q.get()
            # print(plugs)
            for setting in [(plugs[0], plugs[1]), (plugs[1], plugs[0])]:
                # print(setting)
                if setting in self.visited:
                    continue
                self.visited.add(setting)

                toEncode = setting[0]
                # print(toEncode)

                for expected in self.menu.getExpected(setting[0]):
                    # print(expected)
                    output = enigmas[expected[1]-1].encode(setting[1], step=False)
                    newPlugSetting = (output, expected[0])
                    # print(newPlugSetting)
                    if newPlugSetting in self.visited:
                        continue
                    self.q.put(newPlugSetting)

                    self.diagonalBoard[charToInt(output)][charToInt(expected[0])] = True
                    self.diagonalBoard[charToInt(expected[0])][charToInt(output)] = True


    def resetDiagonalBoard(self):
        self.diagonalBoard = []
        for i in range(0, 26):
            self.diagonalBoard.append([])
            for j in range(0, 26):
                self.diagonalBoard[i].append(False)
                    
    def setAssumptions(self, assumptions):
        self.q.put(assumptions)
        self.diagonalBoard[charToInt(assumptions[1])][charToInt(assumptions[0])] = True
        self.diagonalBoard[charToInt(assumptions[0])][charToInt(assumptions[1])] = True
        # self.printDiagonalBoard()

    def printDiagonalBoard(self):
        print()
        for i in range(0, 26):
            print(intToChar(i) + str(boolListToInt(self.diagonalBoard[i])))



def menuFromText(crib, cipher):
    if len(crib) != len(cipher):
        return None
    menu = []
    for i in range(0, len(crib)):
        menu.append([crib[i], cipher[i], i+1])
    return menu


if __name__ == "__main__":
    menu = Menu()
    crib = input("Please enter the crib: ")
    cipher = input ("Please enter the cipher: ")
    nodes = menuFromText(crib, cipher)
    # print(nodes)
    for n in nodes:
        menu.addNode(n[0], n[1], n[2])

    # node = input("Please enter a node in the menu in the format 'c c n': ")
    # while node:
    #     nodeValues = node.split(' ')
    #     menu.addNode(nodeValues[0].upper(), nodeValues[1].upper(), int(nodeValues[2]))
    #     node = input("Please enter a node in the menu in the format 'c c n': ")
    assumption = input("Please make an assumption about the plug setting: ").split(' ')
    rotorOrder = input("Please enter the rotor order (3 unique numbers between 1-5): ")[0:3]
    print(rotorOrder)
    rotorPositions = input("Please enter the ring setting (3 letters): ").upper()
    print(rotorPositions)
    reflector = input("Please enter the reflector type (1-3): ")
    if (not reflector):
        bombe = Bombe(menu, rotors=rotorOrder, rotorPositions=rotorPositions)
    else:
        bombe = Bombe(menu, rotors=rotorOrder, rotorPositions=rotorPositions, reflector=reflector)
    bombe.setAssumptions((assumption[0], assumption[1]))
    bombe.run()
    bombe.printDiagonalBoard()
