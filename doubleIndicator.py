from Enigma import Enigma

def charToInt(char):
    return ord(char.upper()) - 65

def intToChar(num):
    return chr(num + 65)

class groups():
    def __init__(self):
        self.before = [""]*26
        self.after = [""]*26
        
    def addLetters(self, first, second):
        f = charToInt(first)
        s = charToInt(second)
        self.before[s] = first
        self.after[f] = second

    def getGroups(self):
        traversed = [False] * 26
        count = 0
        curr = 0
        groupList = []
        index = -1
        none = 0
        while (count < 26 and none < 26):
            if not traversed[curr]:
                none = 0
                index += 1
                groupList.append([])
                groupList[index].append(intToChar(curr))
                count += 1
                traversed[curr] = True
                curr = charToInt(self.after[curr])
                while not traversed[curr]:
                    groupList[index].append(intToChar(curr))
                    count += 1
                    traversed[curr] = True
                    curr = charToInt(self.after[curr])
            else:
                none += 1
                curr += 1
                if (curr >= 26):
                    curr -= 26
        return groupList

    def printGroups(self):
        msg = ""
        groupList = self.getGroups()
        groupList.sort(key=len)
        for i in range(0, len(groupList)):
            msg += "(" + "".join(groupList[i]) + ")"
        return msg







if __name__ == "__main__":
    rotorOrder = input("Please enter the rotor order (3 unique numbers between 1-5): ")[0:3]
    print(rotorOrder)
    rotorPositions = input("Please enter the ring setting (3 letters): ").upper()
    print(rotorPositions)
    reflector = input("Please enter the reflector type (1-3): ")
    if (not reflector):
        reflector = "1"
    plugboardSetting = input("Please enter the plug board setting. Make sure that the letters and positions match up. (NO checking): ")
    if (not plugboardSetting):
        enigma = Enigma(rotors=rotorOrder, rotorPositions=rotorPositions, reflector=reflector)
    else:
        enigma = Enigma(rotors=rotorOrder, rotorPositions=rotorPositions, plugSettings=plugboardSetting, reflector=reflector)

    cyclicGroups = [groups(), groups(), groups()]
    indicator = input("Please enter a 3 letter indicator or the 6 letter cipher text: ")
    while indicator:
        if len(indicator) == 3:
            indicator += indicator
            cipherText = ""
            nEnigma = enigma.copy()
            for i in range(0, 6):
                cipherText += nEnigma.encode(indicator[i])
            print(cipherText)
            for i in range(0, 3):
                cyclicGroups[i].addLetters(cipherText[i], cipherText[i+3])

        elif len(indicator) == 6:
            print(indicator)
            for i in range(0, 3):
                cyclicGroups[i].addLetters(indicator[i], indicator[i+3])

        else:
            print("Invalid indicator")


        indicator = input("Please enter a 3 letter indicator: ")
    print()
    for i in range(0, 3):
        print("Permutation " + str(i+1) + " and " + str(i+4) + " " + cyclicGroups[i].printGroups())



