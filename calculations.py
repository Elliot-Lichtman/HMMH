import HMM

model = HMM.HMM()
model.readIn("model.txt")
model.printString()


# JINGLE BELLS
#chain = [0, 1, 0, 2]
#noteGroups = ["E E E E E E E G C D E F E E E E", "F F F F", "E D D E D G"]

# DONT STOP BELIEVING
#chain = [0, 1, 2, 3]
#noteGroups = ["C D E", "G A B", "A B C", "F F"]

# WILDEST DREAMS
#chain = [0, 1, 2, 3]
#noteGroups = ["C D C D C", "D D E D C", "D A D E D C", "D A C"]

# JET PLANE
#chain = [0, 1, 0, 1, 0, 2, 0]
#noteGroups = ["G E G E G G E G", "A G F G F G F E C F F E C", "E D E G"]

# LET IT BE
#chain = [0, 1, 2, 3]
#noteGroups = ["E E G G A E", "G G C D", "E E E D C", "D C C"]

# RIPTIDE
chain = [0, 1, 2, 0, 1, 2, 0, 1, 2]
noteGroups = ["A B C D A B C D E E", "E A G D E A G D E D E D", "E E D E D E G E"] 

def calculate(chain, noteGroups):
    options = HMM.viterbi(noteGroups, chain, model)

    max = 0

    sequence = [""]

    for key in options[0].keys():
        if options[0][key][0] > max:
            max = options[0][key][0]
            sequence[0] = key

    current = sequence[0]
    for chord in range(1, len(chain)):
        nextChord = options[chord-1][current][1]
        sequence.append(nextChord)
        current = nextChord
    
    return sequence

sequence = calculate(chain, noteGroups)
print()
print("HERE IS THE CHORD SEQUENCE")
print(sequence)