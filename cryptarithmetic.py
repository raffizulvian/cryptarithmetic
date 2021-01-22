import time
import sys


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
        if len(self.operand[0]) == len(self.answer[0]):
            allWords = self.operand + self.answer
        else:
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
        isOk = True
        for val in list(self.mapping.values()):
            if list(self.mapping.values()).count(val) > 1:
                isOk = False
                break
        guess = sum(self.numOpr)
        return (guess == self.numAns) and isOk

    def _checkIsContain(self, val, mapping):
        if val in mapping.values():
            return True
        return False

    def _incr(self):
        i = -1
        key = list(self.mapping.keys())
        val = range(10)
        isFinish = False
        while not isFinish and i >= -1 * len(key):
            currVal = self.mapping[key[i]]
            nextPos = val.index(currVal) + 1
            if nextPos == 10:
                nextPos = 0
                self.mapping[key[i]] = nextPos
                i -= 1
            else:
                while self._checkIsContain(nextPos, self.mapping) and nextPos < 9:
                    nextPos += 1
                self.mapping[key[i]] = nextPos
                isFinish = True

    def calculate(self):
        isFound = False
        self._initMapping()
        while not isFound:
            guess = self._subtitute()
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

    def showSolution(self):
        opr = self.numOpr
        ans = self.numAns
        for i in range(len(opr)):
            space = len(str(ans)) - len(str(opr[i]))
            if len(opr) - 1 - i == 0:
                print(' '*space, opr[i], '+', sep='')
            else:
                print(' '*space, opr[i], ' '*10, sep='')
        print('-' * len(str(ans)))
        print(ans)


def readFile(path):
    operand = []
    answer = []
    with open(path) as f:
        lines = [line.strip() for line in f.read().splitlines()]
        lines.pop(-2)
        answer.append(lines.pop(-1))
        lines[-1] = lines[-1].strip('+')
        operand.extend(lines)
        f.close()
    return (operand, answer)


def showProblem(opr, ans):
    print('\nPROBLEM', '=======', sep='\n')
    for i in range(len(opr)):
        space = len(ans[0]) - len(opr[i])
        if len(opr) - 1 - i == 0:
            print(' '*space, opr[i], '+', sep='')
        else:
            print(' '*space, opr[i], sep='')
    print('-' * len(ans[0]))
    print(ans[0])


operand, answer = readFile("cryptarithmetic_spec.txt")
showProblem(operand, answer)

solver = Solver(operand, answer)

print('\nSOLUTION', '========', sep='\n')
initialTime = time.time()
print("Calculating...", end='\r')
solver.calculate()
sys.stdout.flush()
solver.showSolution()
finalTime = time.time()

print("\nEXECUTION TIME: ", end='')
print(finalTime - initialTime, end='')
print("\nTOTAL TRIES: ", end='')
print(solver.triesCount)
