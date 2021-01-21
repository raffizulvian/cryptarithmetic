import time


class Solver:
    def __init__(self, operand, answer):
        self.operand = operand
        self.answer = answer
        self.mapping = {}
        self.numOpr = []
        self.numAns = 0
        self.triesCount = 0

    def _initMapping(self):
        i = 0
        allWords = self.answer + self.operand
        for word in allWords:
            for letter in word:
                if letter not in self.mapping.keys():
                    self.mapping[letter] = i
                    i += 1
                else:
                    continue

    def _subtitute(self):
        answerNum = ''
        for letter in self.answer[0]:
            answerNum += str(self.mapping[letter])
        if answerNum[0] == '0':
            return None
        self.numAns = int(answerNum)
        for i in range(len(self.operand)):
            word = self.operand[i]
            num = ''
            for letter in word:
                num += str(self.mapping[letter])
            if num[0] == '0':
                return None
            self.numOpr.append(int(num))
        return (self.numOpr, self.numAns)

    def _evaluate(self):
        guess = sum(self.numOpr)
        return guess == self.numAns

    def _incr(self):
        i = -1
        key = list(self.mapping.keys())
        isFinish = False
        while not isFinish and i >= -1 * len(key):
            if self.mapping[key[i]] < 9:
                self.mapping[key[i]] += 1
                isFinish = True
            else:
                self.mapping[key[i]] = 0
                i -= 1

    def calculate(self):
        isFound = False
        self._initMapping()
        print(self.mapping)
        while not isFound:
            guess = self._subtitute()
            print(self.mapping)
            print(self.numOpr)
            print(self.numAns)
            if not guess:
                self._incr()
                self.triesCount += 1
                continue
            isFound = self._evaluate()
            if not isFound:
                self.triesCount += 1
                self.numOpr = []
                self.numAns = 0
                self._incr()
        return self.mapping


def read_file(path):
    operand = []
    answer = []
    with open(path) as f:
        lines = f.read().splitlines()
        print('PROBLEM', '=======', sep='\n')
        for line in lines:
            print(line)
        lines.pop(-2)
        answer.append(lines.pop(-1))
        lines[-1] = lines[-1].strip('+')
        operand.extend(lines)
        f.close()
    return (operand, answer)


operand, answer = read_file("cryptarithmetic_spec.txt")
solver = Solver(operand, answer)

print('\nSOLUTION', '========', sep='\n')
initialTime = time.time()
solver.calculate()
finalTime = time.time()

print("\nEXECUTION TIME: ", end='')
print(finalTime - initialTime)
print("\nTOTAL TRIES: ", end='')
print(solver.triesCount)
