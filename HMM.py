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

    def calculateOdds(self, notes):
        total = 1
        currentNote = ""
        for letter in notes:
            if letter == " ":
                total *= self.notes[currentNote]
                currentNote = ""
            else:
                currentNote += letter
        total *= self.notes[currentNote]
        return total 
            
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

def copyList(list):
    newList = []
    for item in list:
        newList.append(item)
    return newList

def copyDict(dict):
    newDict = {}
    for item in dict:
        newDict[item] = dict[item]
    return newDict

def permute(arr):

    if arr == []:
        return [[]]
    
    oneLessPermutations = permute(arr[1:])
    permutations = []
    for option in oneLessPermutations:
        for insertSpace in range(len(option)):
            newVersion = copyList(option)
            newVersion.insert(insertSpace, arr[0])
            permutations.append(copyList(newVersion))
        newVersion = copyList(option)
        newVersion.append(arr[0])
        permutations.append(copyList(newVersion))
    
    return permutations

def calculate(noteGroups, chain, model):

    chords = {}
    for chordNum in chain:
        chords[chordNum] = ""
    
    chordList = []
    for key in model.states:
        chordList.append(key.name)
    
    options = permute(chordList)

    max = 0
    maxPattern = []

    for option in options:
        odds = 1
        dict = {}
        for i in range(len(option)):
            for state in model.states:
                if state.name == option[i]:
                    dict[i] = state

        for notes in range(len(noteGroups)):
            odds *= dict[notes].calculateOdds(noteGroups[notes])
        
        prev = None
        current = None
        for link in chain:
            current = dict[link]

            if prev != None:
                odds *= prev.connections[dict[link]]
        

        if odds >= max:
            max = odds
            maxPattern = option
    
    return maxPattern



def viterbi(noteGroups, chain, model):
    odds = []

    # make the frame for the memoization array

    for state in range(len(chain)):
        odds.append({})

    
    # keep track of odds for each chord for each noteblock

    noteOdds = []

    for group in noteGroups:
        noteOdds.append({})
    
    for noteGroup in range(len(noteGroups)):
        for state in model.states:
            noteOdds[noteGroup][state.name] = state.calculateOdds(noteGroups[noteGroup])
    

    # do the "recursive" dynamic programming

    for state in model.states:
        odds[-1][state.name] = [noteOdds[chain[-1]][state.name], None, {chain[-1]:state.name}]
    
    print(odds)
    print()
    
    for link in range(len(chain)-2, -1, -1):
        for state in model.states:
            noteProb = noteOdds[chain[link]][state.name]

            max = 0
            maxNext = ""
            for nextState in model.states:

                try:
                    decided = copyDict(odds[link+1][nextState.name][2])
                    approved = True
                except:
                    approved = False
                try:
                    for key in decided:
                        if decided[key] == state.name and key != chain[link]:
                            approved = False
                        if key == chain[link] and decided[key] != state.name:
                            approved = False
                except:
                    pass

                if approved:
                    option = noteProb * odds[link+1][nextState.name][0] 
                    option *= state.connections[nextState]
                    if option > max:
                        max = option
                        maxNext = nextState.name

            try:
                decided = copyDict(odds[link+1][maxNext][2])
                decided[chain[link]] = state.name
                odds[link][state.name] = [max, maxNext, decided]
            except:
                pass

    print(odds)

    return odds



    






        


