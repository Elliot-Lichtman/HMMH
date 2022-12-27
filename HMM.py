class State:

    def __init__(self, name):
        self.name = name
        self.connections = {}
        self.notes = {}
    
    def addConnection(self, state, odds):
        self.connections[state] = odds
    
    def addNote(self, note, odds):
        self.notes[note] = odds
    
    def toString(self):
        string = "STATE: " + self.name + "\n"
        string += "\nNOTES:\n"
        for note in self.notes:
            string += note + " - " + str(self.notes[note]) + "\n"
        string += "\nCHORDS:\n"
        for other in self.connections:
            string += other.name + " - " + str(self.connections[other]) + "\n"
        return string

class HMM:

    def __init__(self):
        self.states = []

    def printString(self):
        for state in self.states:
            print(state.toString())
            print()
    
    def readIn(self, fileName):
        file = open(fileName, "r")

        currentLine = file.readline()
        section = None
        
        while currentLine != "":

            if currentLine[0] == "$":
                section = currentLine[1:-1]

            else:
                if section == "CHORDS":
                    currentChord = ""
                    for letter in currentLine:
                        if letter == " ":
                            newChord = State(currentChord)
                            self.states.append(newChord)
                            currentChord = ""
                        else:
                            currentChord += letter
                    newChord = State(currentChord[0:-1])
                    self.states.append(newChord)
                
                elif section == "CHORD CONNECTIONS":
                    chord = currentLine[0:currentLine.index(" ")]
                    for state in self.states:
                        if state.name == chord:
                            currentState = state
                    
                    currentIndex = currentLine.index("-") + 2
                    currentOdds = ""
                    
                    for i in range(len(self.states)):
                        while currentLine[currentIndex] != "," and currentLine[currentIndex] != "\n":
                            currentOdds += currentLine[currentIndex]
                            currentIndex += 1
                        currentOdds = float(currentOdds)
                        currentState.addConnection(self.states[i], currentOdds)
                        currentOdds = ""
                        currentIndex += 1
                else:
                    note = currentLine[0:currentLine.index(" ")]
                    
                    currentIndex = currentLine.index("-") + 2
                    currentOdds = ""
                    
                    for i in range(len(self.states)):
                        while currentLine[currentIndex] != "," and currentLine[currentIndex] != "\n":
                            currentOdds += currentLine[currentIndex]
                            currentIndex += 1
                        currentOdds = float(currentOdds)
                        self.states[i].addNote(note, currentOdds)
                        currentOdds = ""
                        currentIndex += 1
                        





            currentLine = file.readline()

model = HMM()
model.readIn("model.txt")
model.printString()


        


