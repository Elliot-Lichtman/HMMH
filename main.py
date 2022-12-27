import HMM

model = HMM.HMM()
model.readIn("model.txt")
model.printString()

chain = [0, 1, 2, 3]

noteGroups = ["C D E", "G A B", "A B C", "F G"]

HMM.viterbi(noteGroups, chain, model)