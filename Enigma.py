# Rotor settings for the Enigma I from - https://www.cryptomuseum.com/
maxRotors = 3
#         ABCDEFGHIJKLMNOPQRSTUVWXYZ
rotor1 = "EKMFLGDQVZNTOWYHXUSPAIBRCJ"
rotor2 = "AJDKSIRUXBLHWTMCQGZNPYFVOE"
rotor3 = "BDFHJLCPRTXVZNYEIWGAKMUSQO"
rotor4 = "ESOVPZJAYQUIRHXLNFTGKDCMWB"
rotor5 = "VZBRGITYUPSDNHLXAWMJQOFECK"
         #TAG
rotor1Turn = "Q"
rotor2Turn = "E"
rotor3Turn = "V"
rotor4Turn = "J"
rotor5Turn = "Z"

rotors = [rotor1, rotor2, rotor3, rotor4, rotor5]
rotorTurnOver = [rotor1Turn, rotor2Turn, rotor3Turn, rotor4Turn, rotor5Turn]
#       ABCDEFGHIJKLMNOPQRSTUVWXYZ    
ekwa = "EJMZALYXVBWFCRQUONTSPIKHGD"
ekwb = "YRUHQSLDPXNGOKMIEBFZCWVJAT"
ekwc = "FVPJIAOYEDRZXWGCTKUQSBNMHL"

ekw = [ekwa, ekwb, ekwc]

class PlugBoard:
    def __init__(self, string):
        self.wiring = []
        self.leftDevice = None

        if (len(string) == 26):
            self.wiring = list(string)
        else:
            print("Error. Incorrect number of letters passed to PlugBoard.")

    def encode(self, letter):
        return self.wiring[ord(letter) - 65]

    def passValue(self, letter, step=False):
        encoded = self.encode(letter)

        if (not self.leftDevice == None):
            ret = self.leftDevice.passValue(encoded, step=step)
            return self.encode(ret)
        else:
            return encoded

    def setLeftDevice(self, device):
        if (not device == None):
            self.leftDevice = device

    def getSetting(self):
        if not self.leftDevice == None:
            return self.leftDevice.getSetting()
        else:
            return ""

    def next(self, step):
        if not self.leftDevice == None:
            self.leftDevice.next(step)

class Reflector:
    def __init__(self, string):
        self.wiring = []
        self.leftDevice = None
        self.rightDevice = None

        if (len(string) == 26):
            self.wiring = list(string)
        else:
            print("Error. Incorrect number of letters passed to Reflector.")

    def encode(self, letter):
        # print("Reflector letter in: " + letter)
        # print("Reflector letter out: " + self.wiring[ord(letter) - 65])
        return self.wiring[ord(letter) - 65]

    def passValue(self, letter, step=False):
        return self.encode(letter)

    def setLeftDevice(self, device):
        pass

    def getSetting(self):
        if not self.leftDevice == None:
            return self.leftDevice.getSetting()
        else:
            return ""

    def next(self, step):
        if not self.leftDevice == None:
            self.leftDevice.next(step)

class Rotor:
    def __init__(self, string, turnOver="A", position="A", isSecond=False):
        self.wiring = []
        self.outWiring = []
        self.leftDevice = None
        self.position = position 
        self.turnOver = turnOver
        self.index = ord(self.position) - 65
        self.turnIndex = ord(self.turnOver) - 65
        self.trunOverNext = False
        self.middle = isSecond

        self.turnLeft = False
        self.turnLater = False
        self.willTurn = False
        self.hasTurned = False


        if (len(string) == 26):
            self.wiring = list(string)
            for i in range(0, 26):
                self.outWiring.append("")
            for i in range(0, 26):
                self.outWiring[ord(self.wiring[i]) - 65] = chr(65+i)
        else:
            print(string)
            print("Error. Incorrect number of letters passed to Rotor.")

    def encode(self, letter):
        offSet = (ord(letter) - 65) + self.index
        if (offSet >= 26):
            offSet -=  26
        code = ord(self.wiring[offSet]) + self.index
        if (code > 90):
            code -= 26

        return chr(code)

    def encodeOut(self, letter):
        offSet = (ord(letter) - 65) - self.index
        if (offSet < 0):
            offSet +=  26
        code = ord(self.outWiring[offSet]) - self.index
        if (code < 65):
            code += 26

        return chr(code)

    def passValue(self, letter, step=False):
        # print("Rotor letter in: " + letter)
        encoded = self.encode(letter)
        # print("Rotor letter encoded: " + encoded)
        if (not self.leftDevice == None):
            self.isTurning(step)
            ret = self.leftDevice.passValue(encoded, step=self.turnLeft)
            # print("Rotor letter returned: " + ret)
            encoded = self.encodeOut(ret)
            # print("Rotor letter out: " + encoded)
            self.turn()
            return encoded
        else: 
            return self.wiring[ord(letter) - 65]

    def setLeftDevice(self, device):
        if (not device == None):
            self.leftDevice = device

    def turn(self):
        if (self.willTurn):
            self.willTurn = False
            self.index += 1
            if (self.index >= 26):
                self.index -= 26
            self.position = chr(self.index + 65)
        self.turnLeft = False
        # if (self.willTurn):
        #     self.willTurn = False
        #     self.turnLeft = False
        #     self.turnLater = False
        #     self.hasTurned = True
        #     self.index += 1
        #     if (self.index >= 26):
        #         self.index -= 26
        #     self.position = chr(self.index + 65)
        # else:
        #     self.hasTurend = False

    def isTurning(self, step):
        if (step):
            self.willTurn = True
        elif (self.middle and self.index == self.turnIndex):
            self.willTurn = True
        if (self.willTurn and self.index == self.turnIndex):
            self.turnLeft = True

        # if self.index == self.turnIndex:
        #     self.turnLeft = True
        # else:
        #     self.turnLeft = False

        # if (self.turnLeft and self.hasTurned and not isTurning):
        #     self.turnLater = True
        #     self.willTurn = True
        # if (self.turnLater or turnOver):
        #     self.turnLater = False
        #     self.willTurn = True

        # print(turnOver, isTurning)
        # print(self.willTurn, self.turnLeft, self.turnLater)

    def getSetting(self):
        if not self.leftDevice == None:
            return self.leftDevice.getSetting() + self.position
        else:
            return self.position

    def next(self, step):
        self.isTurning(step)
        if not self.leftDevice == None:
            self.leftDevice.next(self.turnLeft)
        self.turn()


class Enigma:
    # left most rotor has index 0
    def __init__(self, rotors="123", rotorPositions="AAA", plugSettings="ABCDEFGHIJKLMNOPQRSTUVWXYZ", reflector="1", nRotors=maxRotors):
        self.nRotors = nRotors
        self.reflector = None
        self.plugBoard = None
        self.rotors = [None, None, None]
        for i in range(0, nRotors):
            self.setRotor(i, int(rotors[i]), rotorPositions[i])
        self.setReflector(int(reflector))
        self.setPlugBoard(plugSettings)
        self.originalRotorOrder = rotors
        self.originalPlugSettings = plugSettings
        self.originalReflector = reflector

    def setRotor(self, rotorPosition, type, position):
        middle = (rotorPosition == 1)
        self.rotors[rotorPosition] = Rotor(rotors[type-1], rotorTurnOver[type-1], position, middle)
        if rotorPosition == 0:
            self.rotors[rotorPosition].setLeftDevice(self.reflector)
        else:
            self.rotors[rotorPosition].setLeftDevice(self.rotors[rotorPosition-1])
        
        if rotorPosition >= maxRotors - 1:    
            if (not self.plugBoard == None):
                self.plugBoard.setLeftDevice(self.rotors[rotorPosition])
        else:
            if (not self.rotors[rotorPosition+1] == None):
                self.rotors[rotorPosition+1].setLeftDevice(self.rotors[rotorPosition])

    def setReflector(self, type):
        self.reflector = Reflector(ekw[type])
        if (not self.rotors[0] == None):
            self.rotors[0].setLeftDevice(self.reflector)

    def setPlugBoard(self, setting):
        self.plugBoard = PlugBoard(setting)
        self.plugBoard.setLeftDevice(self.rotors[self.nRotors-1])

    def encode(self, letter, step=True):
        if letter.isalpha():
            letter = letter.upper()
            return self.plugBoard.passValue(letter, step=step)
        else:
            return None

    def getSetting(self):
        return self.plugBoard.getSetting()

    def copy(self):
        return Enigma(rotors=self.originalRotorOrder, rotorPositions=self.getSetting(),
         plugSettings=self.originalPlugSettings, reflector=self.originalReflector)

    def next(self):
        self.plugBoard.next(True)

    def copyNext(self):
        enigma = self.copy()
        enigma.step()
        return enigma


if __name__ == "__main__":
    rotorOrder = input("Please enter the rotor order (3 unique numbers between 1-5): ")[0:3]
    print(rotorOrder)
    rotorPositions = input("Please enter the ring setting (3 letters): ").upper()
    print(rotorPositions)
    plugboardSetting = input("Please enter the plug board setting. Make sure that the letters and positions match up. (NO checking): ")
    if (not plugboardSetting):
        enigma = Enigma(rotors=rotorOrder, rotorPositions=rotorPositions)
    else:
        enigma = Enigma(rotors=rotorOrder, rotorPositions=rotorPositions, plugSettings=plugboardSetting)

    text = str(input("Enter some plain/cipher text or EOF: "))
    while text:
        if (text.isalpha()):
            text = text.upper()
            print("Current rotor position: " + enigma.getSetting())
            print(text)
            cipherText = ""
            for letter in text:
                cipherText = cipherText + enigma.encode(letter, step=False)
            print(cipherText + "\r\n")
        else:
            print("Please enter text as all letter. The Enigma machine does not use SPACES!!")
        text = input("Enter another plain/cipher text or EOF: ")