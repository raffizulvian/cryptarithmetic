import sys
from pathlib import Path
from time import time


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

    num_opr : list
        Daftar integer yang merupakan hasil substitusi operan dengan angka yang bersesuaian.

    num_ans : int
        Integer yang merupakan hasil substitusi hasil dengan angka yang bersesuaian.

    tries_count : int
        Menyimpan jumlah uji coba/percobaan untuk mencari pemetaan huruf-angka yang tepat.

    """

    def __init__(self, operand, answer):
        self.operand = operand
        self.answer = answer
        self.mapping = {}
        self.num_opr = []
        self.num_ans = 0
        self.tries_count = 0

    def calculate(self) -> bool:
        """
        Bagian utama dari penerapan algoritma brute force. Melakukan iterasi dan
        langkah langkah untuk menyelesaikan persoalan cryptarithmetic.

        """

        is_found = False

        # Melakukan pemetaan awal pada huruf-angka
        self._init_mapping()
        total_letters = len(self.mapping.values())

        # Mengulagi proses sampai ditemukan solusi yang sesuai
        while not is_found and list(self.mapping.values()).count(9) < total_letters:

            # Menyubstitusikan huruf-huruf pada operan dan hasil serta
            # melakukan pengecekan apakah percobaan saat ini sesuai aturan
            guess = self._subtitute()
            if not guess:

                # Melakukan inkremen pada huruf paling kanan dalam pemetaan
                self._incr()
                self.tries_count += 1
                self.num_opr = []
                self.num_ans = 0
                continue

            # Mengecek hasil penjumlahan operan apakah sesuai dengan hasil
            is_found = self._evaluate()
            if not is_found:
                self.tries_count += 1
                self.num_opr = []
                self.num_ans = 0
                self._incr()

        return is_found

    def show_problem(self):
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

    def show_solution(self):
        """
        Mencetak solusi persoalan dengan format yang ditentukan.

        """

        opr = self.num_opr
        ans = self.num_ans

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

    def _init_mapping(self):
        """
        Menginisialisasi pemetaan awal antara huruf dengan angka dari 1 sampai 9.

        """

        initial_value = 0

        # Menentukan huruf mana yang akan ditempatkan di kiri
        if len(self.operand[0]) == len(self.answer[0]):
            all_words = self.operand + self.answer
        else:
            all_words = self.answer + self.operand

        # Mengasosiasikan tiap huruf dengan sebuah angka dari 1 sampai 9
        for word in all_words:
            for letter in word:
                if letter not in self.mapping.keys():
                    self.mapping[letter] = initial_value
                    initial_value += 1

    def _subtitute(self) -> [None, tuple]:
        """
        Menyubstitusikan tiap huruf dengan angka-angka yang bersesuaian pada
        pemetaan saat fungsi ini dipanggil.

        """

        # Mengganti huruf-huruf pada hasil dengan angka yang bersesuaian
        answer_num = ''
        for letter in self.answer[0]:
            answer_num += str(self.mapping[letter])

            # Mengembalikan None jika huruf pertama pada kata diawali angka 0
            if answer_num[0] == '0':
                return None
        self.num_ans = int(answer_num)

        # Mengganti huruf-huruf pada operan dengan angka yang bersesuaian
        for i in range(len(self.operand)):
            word = self.operand[i]
            operand_num = ''
            for letter in word:
                operand_num += str(self.mapping[letter])

                # Mengembalikan None jika huruf pertama pada kata diawali angka 0
                if operand_num[0] == '0':
                    return None
            self.num_opr.append(int(operand_num))

        return (self.num_opr, self.num_ans)

    def _incr(self):
        """
        Membuat komposisi pemetaan huruf-angka baru.

        """

        pos = -1
        is_finish = False
        key = list(self.mapping.keys())

        while not is_finish and pos >= -1 * len(key):
            curr_val = self.mapping[key[pos]]
            next_val = curr_val + 1

            # Menjadikan 0 dan menambahkan 1 pada huruf di kiri jika hasil inkremen adalah 10
            if next_val == 10:
                next_val = 0
                self.mapping[key[pos]] = next_val
                pos -= 1

            # Menambahkan 1 sampai menjadi angka unik pertama setelah angka sebelumnya
            else:
                while self._check_is_contain(next_val, self.mapping) and next_val < 9:
                    next_val += 1
                self.mapping[key[pos]] = next_val
                is_finish = True

    def _evaluate(self) -> bool:
        """
        Melakukan evaluasi pada operan dan hasil yang sudah diganti dengan angka.
        Evaluasi terdiri dari pengecekan agar tidak ada angka ganda dan juga
        pengecekan hasil operasi penjumlahan operannya apakah sesuai dengan hasil.

        """

        is_unique = True
        guess_answer = sum(self.num_opr)

        # Mengecek apabila ada angka ganda
        for val in list(self.mapping.values()):
            if list(self.mapping.values()).count(val) > 1:
                is_unique = False
                break

        return (guess_answer == self.num_ans) and is_unique

    def _check_is_contain(self, val, mapping) -> bool:
        """
        Mengecek apakah suatu angka sudah terdapat pada pemetaan huruf-angka.

        """

        return val in mapping.values()


def resource_path(relative_path) -> Path:
    """ 
    Mendapatkan absolute path file yang dituju, berfungsi untuk file .py
    dan untuk file .exe hasil PyInstaller.

    """

    try:
        # PyInstaller membuat folder sementara dan menyimpan di _MEIPASS
        base_path = sys._MEIPASS

    except Exception:
        base_path = Path('.').absolute()

    return Path(base_path).joinpath(relative_path)


def read_file(file_name) -> tuple:
    """
    Membaca dan memeroses file yang bebrisi persoalan Cryptarithmetic.

    """

    operand = []
    answer = []

    rel_path = Path("test").joinpath(file_name)
    full_path = resource_path(rel_path)

    try:
        with open(full_path) as f:

            # Membaca tiap baris pada file persoalan
            lines = [line.strip() for line in f.read().splitlines()]

            # Membuang baris yang tidak dibutuhkan
            lines.pop(-2)

            # Memasukkan operan dan hasil pada list masing-masing
            answer.append(lines.pop(-1))
            lines[-1] = lines[-1].strip('+')
            operand.extend(lines)

            f.close()
    
    except FileNotFoundError:
        print("**ERROR: File not found.**")

    return (operand, answer)


if __name__ == "__main__":
    problem_list = [
        "problem01.txt", "problem02.txt", "problem03.txt", "problem04.txt",
        "problem05.txt", "problem06.txt", "problem07.txt", "problem08.txt",
        "problem09.txt", "problem10.txt"
    ]

    num_prob = len(problem_list)

    selected_problem = int(
        input(f"\nChoose cryptarithmetic problem to solve (1-{num_prob}): ")
    ) - 1

    operand, answer = read_file(problem_list[selected_problem])

    solver = CryptarithmeticSolver(operand, answer)
    solver.show_problem()

    # Mencatat waktu awal program berjalan
    initial_time = time()

    print('\nSOLUTION', '========', sep='\n')
    print("Calculating...", end='\r')
    result = solver.calculate()
    sys.stdout.flush()
    if result:
        solver.show_solution()
    else:
        print("Sorry, no solutions found!")

    # Mencatat waktu akhir program berjalan
    final_time = time()

    print("\nEXECUTION TIME: ", end='')
    print(final_time - initial_time, 's', end='')

    print("\nTOTAL TRIES: ", end='')
    print("{:,}".format(solver.tries_count))
