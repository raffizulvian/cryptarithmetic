import sys
import time

from pathlib import Path


class CryptarithmeticSolver:
    """
    Kelas untuk menyelesaikan persoalan Cryptarithmetic dengan algoritma brute force.

    Parameters
    ----------
    operand : list
        Daftar string kata yang berperan sebagai operan.

    answer : list
        Daftar string kata yang berperan sebagai hasil.

    Attributes
    ----------
    operand : list
        Daftar string kata yang berperan sebagai operan.

    answer : list
        Daftar string kata yang berperan sebagai hasil.

    mapping : dict
        Pemetaan yang menunjukan asosiasi huruf-angka yang bersesuaian.

    numOpr : list
        Daftar integer yang merupakan hasil substitusi operan dengan angka yang bersesuaian.

    numAns : int
        Integer yang merupakan hasil substitusi hasil dengan angka yang bersesuaian.

    triesCount : int
        Menyimpan jumlah uji coba/percobaan untuk mencari pemetaan huruf-angka yang tepat.

    """

    def __init__(self, operand, answer):
        self.operand = operand
        self.answer = answer
        self.mapping = {}
        self.numOpr = []
        self.numAns = 0
        self.triesCount = 0

    def calculate(self) -> dict:

        isFound = False

        # Melakukan pemetaan awal pada huruf-angka
        self._initMapping()

        # Mengulagi proses sampai ditemukan solusi yang sesuai
        while not isFound:

            # Menyubstitusikan huruf-huruf pada operan dan hasil serta
            # melakukan pengecekan apakah percobaan saat ini sesuai aturan
            guess = self._subtitute()
            if not guess:

                # Melakukan inkremen pada huruf paling kanan dalam pemetaan
                self._incr()
                self.triesCount += 1
                self.numOpr = []
                self.numAns = 0
                continue

            # Mengecek hasil penjumlahan operan apakah sesuai dengan hasil
            isFound = self._evaluate()
            if not isFound:
                self.triesCount += 1
                self.numOpr = []
                self.numAns = 0
                self._incr()

        return self.mapping

    def showProblem(self):
        """
        Mencetak persoalan yang terdiri dari operan-operan, garis
        batas serta hasil kelayar dengan format yang ditentukan.

        """

        print('\nPROBLEM', '=======', sep='\n')

        # Mencetak operan-operan
        for i in range(len(self.operand)):
            space = len(self.answer[0]) - len(self.operand[i])
            if len(self.operand) - 1 - i == 0:
                print(' '*space, self.operand[i], '+', sep='')
            else:
                print(' '*space, self.operand[i], sep='')

        # Mencetak garis batas serta hasil
        print('-' * len(self.answer[0]))
        print(self.answer[0])

    def showSolution(self):
        """
        Mencetak solusi persoalan dengan format yang ditentukan.

        """

        opr = self.numOpr
        ans = self.numAns

        # Mencetak operan-operan
        for i in range(len(opr)):
            space = len(str(ans)) - len(str(opr[i]))
            if len(opr) - 1 - i == 0:
                print(' '*space, opr[i], '+', sep='')
            else:
                print(' '*space, opr[i], ' '*14, sep='')

        # Menyetak garis batas serta hasil
        print('-' * len(str(ans)))
        print(ans)

    def _initMapping(self):
        """
        Menginisialisasi pemetaan awal antara huruf dengan angka dari 1 sampai 9.

        """

        i = 0

        # Menentukan huruf mana yang akan ditempatkan di kiri
        if len(self.operand[0]) == len(self.answer[0]):
            allWords = self.operand + self.answer
        else:
            allWords = self.answer + self.operand

        # Mengasosiasikan tiap huruf dengan sebuah angka dari 1 sampai 9
        for word in allWords:
            for letter in word:
                if letter not in self.mapping.keys():
                    self.mapping[letter] = i
                    i += 1

    def _subtitute(self) -> [None, tuple]:
        """
        Menyubstitusikan tiap huruf dengan angka-angka yang bersesuaian pada
        pemetaan saat fungsi ini dipanggil.

        """

        # Mengganti huruf-huruf pada hasil dengan angka yang bersesuaian
        answerNum = ''
        for letter in self.answer[0]:
            answerNum += str(self.mapping[letter])

            # Mengembalikan None jika huruf pertama pada kata diawali angka 0
            if answerNum[0] == '0':
                return None
        self.numAns = int(answerNum)

        # Mengganti huruf-huruf pada operan dengan angka yang bersesuaian
        for i in range(len(self.operand)):
            word = self.operand[i]
            operandNum = ''
            for letter in word:
                operandNum += str(self.mapping[letter])

                # Mengembalikan None jika huruf pertama pada kata diawali angka 0
                if operandNum[0] == '0':
                    return None
            self.numOpr.append(int(operandNum))

        return (self.numOpr, self.numAns)

    def _incr(self):
        """
        Membuat komposisi pemetaan huruf-angka baru.

        """

        i = -1
        isFinish = False
        key = list(self.mapping.keys())

        while not isFinish and i >= -1 * len(key):
            currVal = self.mapping[key[i]]
            nextVal = currVal + 1

            # Menjadikan 0 dan menambahkan 1 pada huruf di kiri jika hasil inkremen adalah 10
            if nextVal == 10:
                nextVal = 0
                self.mapping[key[i]] = nextVal
                i -= 1

            # Menambahkan 1 sampai menjadi angka unik pertama setelah angka sebelumnya
            else:
                while self._checkIsContain(nextVal, self.mapping) and nextVal < 9:
                    nextVal += 1
                self.mapping[key[i]] = nextVal
                isFinish = True

    def _evaluate(self) -> bool:
        """
        Melakukan evaluasi pada operan dan hasil yang sudah diganti dengan angka.
        Evaluasi terdiri dari pengecekan agar tidak ada angka ganda dan juga
        pengecekan hasil operasi penjumlahan operannya apakah sesuai dengan hasil.

        """

        isUnique = True
        guessAns = sum(self.numOpr)

        # Mengecek apabila ada angka ganda
        for val in list(self.mapping.values()):
            if list(self.mapping.values()).count(val) > 1:
                isUnique = False
                break

        return (guessAns == self.numAns) and isUnique

    def _checkIsContain(self, val, mapping) -> bool:
        """
        Mengecek apakah suatu angka sudah terdapat pada pemetaan huruf-angka.

        """

        return val in mapping.values()


def readFile(file_name) -> tuple:
    """
    Membaca dan memeroses file yang bebrisi persoalan Cryptarithmetic.

    """

    operand = []
    answer = []

    BASE_DIR = Path(__file__).resolve().parent.parent
    FULL_PATH = Path(BASE_DIR).joinpath('test', file_name)

    with open(FULL_PATH) as f:

        # Membaca tiap baris pada file persoalan
        lines = [line.strip() for line in f.read().splitlines()]

        # Membuang baris yang tidak dibutuhkan
        lines.pop(-2)

        # Memasukkan operan dan hasil pada list masing-masing
        answer.append(lines.pop(-1))
        lines[-1] = lines[-1].strip('+')
        operand.extend(lines)

        f.close()

    return (operand, answer)


if __name__ == "__main__":
    problemList = [
        "problem01.txt", "problem02.txt", "problem03.txt", "problem04.txt",
        "problem05.txt", "problem06.txt", "problem07.txt", "problem08.txt",
        "problem09.txt", "problem10.txt"
    ]

    selectedProblem = int(
        input("\nChoose cryptarithmetic problem to solve (1-10): ")
    ) - 1

    operand, answer = readFile(problemList[selectedProblem])

    solver = CryptarithmeticSolver(operand, answer)
    solver.showProblem()

    print('\nSOLUTION', '========', sep='\n')
    initialTime = time.time()
    print("Calculating...", end='\r')
    solver.calculate()
    sys.stdout.flush()
    solver.showSolution()
    finalTime = time.time()

    print("\nEXECUTION TIME: ", end='')
    print(finalTime - initialTime, 's', end='')

    print("\nTOTAL TRIES: ", end='')
    print("{:,}".format(solver.triesCount))
