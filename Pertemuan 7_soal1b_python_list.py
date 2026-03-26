class BigInteger:
    """
    Implementasi Big Integer ADT menggunakan Python list.
    Setiap elemen list menyimpan satu digit, diurutkan dari digit
    paling tidak signifikan (index 0) ke paling signifikan.
    Contoh: 45839 → [9, 8, 3, 5, 4]
    """

    def __init__(self, initValue="0"):
        s = str(initValue).strip()
        self._negative = False

        if s.startswith('-'):
            self._negative = True
            s = s[1:]
        elif s.startswith('+'):
            s = s[1:]

        s = s.lstrip('0') or '0'
        # Simpan digit LSB-first dalam list
        self._digits = [int(ch) for ch in reversed(s)]

        if self._to_int() == 0:
            self._negative = False

    # ------------------------------------------------------------------ #
    #  Helper                                                              #
    # ------------------------------------------------------------------ #
    def _to_int(self):
        value = int(''.join(str(d) for d in reversed(self._digits)))
        return -value if self._negative else value

    @classmethod
    def _from_int(cls, value):
        return cls(str(value))

    # ------------------------------------------------------------------ #
    #  toString                                                            #
    # ------------------------------------------------------------------ #
    def toString(self):
        result = ''.join(str(d) for d in reversed(self._digits)) or '0'
        return ('-' + result) if self._negative else result

    def __repr__(self):
        return f"BigInteger('{self.toString()}')"

    def __str__(self):
        return self.toString()

    # ------------------------------------------------------------------ #
    #  comparable                                                          #
    # ------------------------------------------------------------------ #
    def comparable(self, other):
        a, b = self._to_int(), other._to_int()
        if a < b:   return -1
        if a > b:   return  1
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
        a, b = self._to_int(), rhsInt._to_int()
        ops = {
            '+':  lambda x, y: x + y,
            '-':  lambda x, y: x - y,
            '*':  lambda x, y: x * y,
            '//': lambda x, y: x // y,
            '%':  lambda x, y: x % y,
            '**': lambda x, y: x ** y,
        }
        if op not in ops:
            raise ValueError(f"Operasi tidak dikenal: '{op}'")
        return BigInteger._from_int(ops[op](a, b))

    def __add__(self, other):      return self.arithmetic(other, '+')
    def __sub__(self, other):      return self.arithmetic(other, '-')
    def __mul__(self, other):      return self.arithmetic(other, '*')
    def __floordiv__(self, other): return self.arithmetic(other, '//')
    def __mod__(self, other):      return self.arithmetic(other, '%')
    def __pow__(self, other):      return self.arithmetic(other, '**')

    # ------------------------------------------------------------------ #
    #  bitwise-ops                                                         #
    # ------------------------------------------------------------------ #
    def bitwise_ops(self, rhsInt, op):
        a, b = self._to_int(), rhsInt._to_int()
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

    def __or__(self, other):    return self.bitwise_ops(other, '|')
    def __and__(self, other):   return self.bitwise_ops(other, '&')
    def __xor__(self, other):   return self.bitwise_ops(other, '^')
    def __lshift__(self, other): return self.bitwise_ops(other, '<<')
    def __rshift__(self, other): return self.bitwise_ops(other, '>>')


# ======================================================================= #
#  Pengujian                                                               #
# ======================================================================= #
if __name__ == "__main__":
    print("=" * 55)
    print("  Soal 1(b): Big Integer ADT - Python List")
    print("=" * 55)

    a = BigInteger("45839")
    b = BigInteger("12345")
    print(f"\na = {a}  (digits: {a._digits})")
    print(f"b = {b}  (digits: {b._digits})")

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
    print(f"x | y  = {x | y}")
    print(f"x & y  = {x & y}")
    print(f"x ^ y  = {x ^ y}")
    print(f"x << 2 = {x << BigInteger('2')}")
    print(f"x >> 1 = {x >> BigInteger('1')}")

    print("\n--- Perbandingan ---")
    print(f"a < b  : {a < b}")
    print(f"a > b  : {a > b}")
    print(f"a == b : {a == b}")
