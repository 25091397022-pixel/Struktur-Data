class _Node:
    """Node untuk menyimpan satu digit dari bilangan bulat besar."""
    def __init__(self, digit):
        self.digit = digit
        self.next = None


class BigInteger:
    """
    Implementasi Big Integer ADT menggunakan Singly Linked List.
    Setiap digit disimpan dalam node terpisah, diurutkan dari digit
    paling tidak signifikan (least significant) ke paling signifikan.
    Contoh: 45839 → head -> 9 -> 8 -> 3 -> 5 -> 4 -> None
    """

    def __init__(self, initValue="0"):
        self._head = None
        self._negative = False

        # Tangani tanda negatif
        s = str(initValue).strip()
        if s.startswith('-'):
            self._negative = True
            s = s[1:]
        elif s.startswith('+'):
            s = s[1:]

        # Hapus leading zeros, tapi pastikan minimal ada "0"
        s = s.lstrip('0') or '0'

        # Simpan digit dari paling tidak signifikan ke paling signifikan
        # s = '45839' → simpan 9 di head, kemudian 3, 8, 5, 4 di belakang
        # Hasil: head→9→3→8→5→4 (LSB first)
        tail = None
        for ch in s:              # iterasi dari MSB ke LSB
            node = _Node(int(ch))
            if self._head is None:
                self._head = node
                tail = node
            else:
                tail.next = node  # tambah di belakang → MSB terakhir
                tail = node
        # Sekarang linked list: head→4→5→8→3→9 (MSB first)
        # Balik list agar menjadi LSB first: head→9→3→8→5→4
        prev = None
        cur = self._head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self._head = prev

        # Nilai nol tidak negatif
        if self._to_int() == 0:
            self._negative = False

    # ------------------------------------------------------------------ #
    #  Helper: konversi internal ke int Python                            #
    # ------------------------------------------------------------------ #
    def _to_int(self):
        """Konversi linked list ke int Python (untuk operasi internal)."""
        digits = []
        cur = self._head
        while cur:
            digits.append(str(cur.digit))
            cur = cur.next
        # digits disimpan LSB-first, balik untuk mendapat angka
        value = int(''.join(reversed(digits))) if digits else 0
        return -value if self._negative else value

    @classmethod
    def _from_int(cls, value):
        """Buat BigInteger baru dari int Python."""
        return cls(str(value))

    # ------------------------------------------------------------------ #
    #  toString                                                            #
    # ------------------------------------------------------------------ #
    def toString(self):
        """Mengembalikan representasi string dari bilangan bulat besar."""
        digits = []
        cur = self._head
        while cur:
            digits.append(str(cur.digit))
            cur = cur.next
        result = ''.join(reversed(digits)) if digits else '0'
        return ('-' + result) if self._negative else result

    def __repr__(self):
        return f"BigInteger('{self.toString()}')"

    def __str__(self):
        return self.toString()

    # ------------------------------------------------------------------ #
    #  comparable                                                          #
    # ------------------------------------------------------------------ #
    def comparable(self, other):
        """
        Membandingkan big integer ini dengan other untuk menentukan urutan logisnya.
        Mengembalikan: -1 jika self < other, 0 jika sama, 1 jika self > other
        """
        a = self._to_int()
        b = other._to_int()
        if a < b:
            return -1
        elif a > b:
            return 1
        return 0

    def __lt__(self, other):  return self.comparable(other) == -1
    def __le__(self, other):  return self.comparable(other) <= 0
    def __gt__(self, other):  return self.comparable(other) == 1
    def __ge__(self, other):  return self.comparable(other) >= 0
    def __eq__(self, other):  return self.comparable(other) == 0
    def __ne__(self, other):  return self.comparable(other) != 0

    # ------------------------------------------------------------------ #
    #  arithmetic                                                          #
    # ------------------------------------------------------------------ #
    def arithmetic(self, rhsInt, op):
        """
        Mengembalikan BigInteger baru hasil operasi aritmatika antara
        self dan rhsInt. Operasi yang didukung: +, -, *, //, %, **
        """
        a = self._to_int()
        b = rhsInt._to_int()
        ops = {
            '+':  lambda x, y: x + y,
            '-':  lambda x, y: x - y,
            '*':  lambda x, y: x * y,
            '//': lambda x, y: x // y,
            '%':  lambda x, y: x % y,
            '**': lambda x, y: x ** y,
        }
        if op not in ops:
            raise ValueError(f"Operasi aritmatika tidak dikenal: '{op}'")
        return BigInteger._from_int(ops[op](a, b))

    def __add__(self, other):  return self.arithmetic(other, '+')
    def __sub__(self, other):  return self.arithmetic(other, '-')
    def __mul__(self, other):  return self.arithmetic(other, '*')
    def __floordiv__(self, other): return self.arithmetic(other, '//')
    def __mod__(self, other):  return self.arithmetic(other, '%')
    def __pow__(self, other):  return self.arithmetic(other, '**')

    # ------------------------------------------------------------------ #
    #  bitwise-ops                                                         #
    # ------------------------------------------------------------------ #
    def bitwise_ops(self, rhsInt, op):
        """
        Mengembalikan BigInteger baru hasil operasi bitwise antara
        self dan rhsInt. Operasi yang didukung: |, &, ^, <<, >>
        """
        a = self._to_int()
        b = rhsInt._to_int()
        ops = {
            '|':  lambda x, y: x | y,
            '&':  lambda x, y: x & y,
            '^':  lambda x, y: x ^ y,
            '<<': lambda x, y: x << y,
            '>>': lambda x, y: x >> y,
        }
        if op not in ops:
            raise ValueError(f"Operasi bitwise tidak dikenal: '{op}'")
        return BigInteger._from_int(ops[op](a, b))

    def __or__(self, other):   return self.bitwise_ops(other, '|')
    def __and__(self, other):  return self.bitwise_ops(other, '&')
    def __xor__(self, other):  return self.bitwise_ops(other, '^')
    def __lshift__(self, other): return self.bitwise_ops(other, '<<')
    def __rshift__(self, other): return self.bitwise_ops(other, '>>')


# ======================================================================= #
#  Pengujian                                                               #
# ======================================================================= #
if __name__ == "__main__":
    print("=" * 55)
    print("  Soal 1(a): Big Integer ADT - Singly Linked List")
    print("=" * 55)

    a = BigInteger("45839")
    b = BigInteger("12345")
    print(f"\na = {a}")
    print(f"b = {b}")

    print("\n--- Aritmatika ---")
    print(f"a + b  = {a + b}")
    print(f"a - b  = {a - b}")
    print(f"a * b  = {a * b}")
    print(f"a // b = {a // b}")
    print(f"a % b  = {a % b}")
    print(f"a ** 2 = {a ** BigInteger('2')}")

    print("\n--- Bitwise ---")
    x = BigInteger("60")
    y = BigInteger("13")
    print(f"x = {x}, y = {y}")
    print(f"x | y  = {x | y}")
    print(f"x & y  = {x & y}")
    print(f"x ^ y  = {x ^ y}")
    print(f"x << 2 = {x << BigInteger('2')}")
    print(f"x >> 1 = {x >> BigInteger('1')}")

    print("\n--- Perbandingan ---")
    print(f"a < b  : {a < b}")
    print(f"a > b  : {a > b}")
    print(f"a == b : {a == b}")
    print(f"a != b : {a != b}")
