# CryptarithmeticSolver

Cryptarithmetic merupakan sebuah program yang mampu untuk menyelesaikan persoalan cryptarithmetic sederhana dengan mengunakan algoritma brute force.

## Requirement

Agar dapat menjalankan program langsung dari `cryptarithmetic.py`, pastikan komputer Anda memiliki:

- **Python** (>= 3.8.2)

Namun jika ingin menjalankan program dari `crytarithmetic.exe` tidak diperlukan Python.

## Installation

Buat salinan dari program ini ke komputer lokal Anda dari GitHub

    $ git clone https://github.com/raffizulvian/cryptarithmetic.git
    
atau dapat mendownload file zip baik dari GitHub maupun Google Drive pengumpulan tugas.

## How to Use

Tersedia dua pilihan untuk dapat menggunakan dan menjalankan program ini. Anda bisa menjalankan file `executable` atau file `python`.
Untuk menjalankan program ini dari file `executable` pada top-level directory buka terminal atau command prompt dan tuliskan perintah:

    $ cd bin
    $ cryptarithmetic.exe

atau jika ingin menjalankan file `python`:

    $ cd src
    $ py cryptarithmetic.py

Setelah program berjalan, silakan masukkan nomor persoalan yang ingin diselesaikan. Maka program akan segera mencari kemungkinan solusi dan menampilkannya di layar.

### Add Custom Problem

Untuk menambahkan persoalan baru silakan tuliskan persoalan tersebut dengan format yang sesuai ketentuan pada sebuah file `.txt`.
Penamaan file dibebaskan namun baiknya mengikuti penamaan file soal yang telah ada yaitu `problemXX.txt` dengan `XX` adalah nomor soal.

Pada `cryptarithmetic.py`, setelah inisialisasi list `problem_list` tambahkan daftar soal baru dengan kode berikut:

```python
problem_list = [...]

problem_list += ["problemXX.txt", "problemYY.txt"]
```

**WARNING**: Jika menambahkan soal baru, soal tersebut hanya bisa dibaca jika menjalankan program langsung dari `crytarithmetic.py`. Untuk membuat file `executable` baru dengan soal tambahan silakan merujuk pada
[dokumentasi PyInstaller](https://pyinstaller.readthedocs.io/en/stable/).

## Author

13519003 - Raffi Zulvian Muzhaffar 😎
