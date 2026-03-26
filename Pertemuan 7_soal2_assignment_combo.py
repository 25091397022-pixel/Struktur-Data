class _Node:
    def __init__(self, digit):
        self.digit = digit
        self.next = None


class BigInteger:
    """
    Implementasi Big Integer ADT menggunakan Singly Linked List.
    Soal 2: Ditambah operator assignment combo:
      +=  -=  *=  //=  %=  **=
      <<=  >>=  |=  &=  ^=
    """

    def __init__(self, initValue="0"):
        self._head = None
        self._negative = False

        s = str(initValue).strip()
        if s.startswith('-'):
            self._negative = True
            s = s[1:]
        elif s.startswith('+'):
            s = s[1:]

        # Simpan digit LSB-first: untuk s='45839' → head→9→3→8→5→4
        tail = None
        for ch in s:
            node = _Node(int(ch))
            if self._head is None:
                self._head = node
                tail = node
            else:
                tail.next = node
                tail = node
        # Balik list agar LSB di head
        prev = None
        cur = self._head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self._head = prev

        if self._to_int() == 0:
            self._negative = False

    # ------------------------------------------------------------------ #
    #  Helper                                                              #
    # ------------------------------------------------------------------ #
    def _to_int(self):
        digits = []
        cur = self._head
        while cur:
            digits.append(str(cur.digit))
            cur = cur.next
        value = int(''.join(reversed(digits))) if digits else 0
        return -value if self._negative else value

    @classmethod
    def _from_int(cls, value):
        return cls(str(value))

    def _copy_from(self, other):
        """Salin state dari BigInteger lain ke self (untuk operator in-place)."""
        tmp = BigInteger(other.toString())
        self._head = tmp._head
        self._negative = tmp._negative

    # ------------------------------------------------------------------ #
    #  toString                                                            #
    # ------------------------------------------------------------------ #
    def toString(self):
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

    def __or__(self, other):     return self.bitwise_ops(other, '|')
    def __and__(self, other):    return self.bitwise_ops(other, '&')
    def __xor__(self, other):    return self.bitwise_ops(other, '^')
    def __lshift__(self, other): return self.bitwise_ops(other, '<<')
    def __rshift__(self, other): return self.bitwise_ops(other, '>>')

    # ------------------------------------------------------------------ #
    #  Soal 2: Operator Assignment Combo (in-place)                       #
    # ------------------------------------------------------------------ #

    # --- Aritmatika in-place ---
    def __iadd__(self, other):
        """+="""
        self._copy_from(self + other)
        return self

    def __isub__(self, other):
        """-="""
        self._copy_from(self - other)
        return self

    def __imul__(self, other):
        """*="""
        self._copy_from(self * other)
        return self

    def __ifloordiv__(self, other):
        """//="""
        self._copy_from(self // other)
        return self

    def __imod__(self, other):
        """%="""
        self._copy_from(self % other)
        return self

    def __ipow__(self, other):
        """**="""
        self._copy_from(self ** other)
        return self

    # --- Bitwise in-place ---
    def __ilshift__(self, other):
        """<<="""
        self._copy_from(self << other)
        return self

    def __irshift__(self, other):
        """>>="""
        self._copy_from(self >> other)
        return self

    def __ior__(self, other):
        """|="""
        self._copy_from(self | other)
        return self

    def __iand__(self, other):
        """&="""
        self._copy_from(self & other)
        return self

    def __ixor__(self, other):
        """^="""
        self._copy_from(self ^ other)
        return self


# ======================================================================= #
#  Pengujian                                                               #
# ======================================================================= #
if __name__ == "__main__":
    print("=" * 55)
    print("  Soal 2: Big Integer ADT - Operator Assignment Combo")
    print("=" * 55)

    print("\n--- Operator Assignment Aritmatika ---")

    a = BigInteger("100")
    b = BigInteger("25")
    print(f"a = {a}, b = {b}")

    a += b;  print(f"a += b   → a = {a}")   # 125
    a -= b;  print(f"a -= b   → a = {a}")   # 100
    a *= b;  print(f"a *= b   → a = {a}")   # 2500
    a //= b; print(f"a //= b  → a = {a}")   # 100
    a %= BigInteger("7"); print(f"a %%= 7   → a = {a}")  # 100 % 7 = 2
    a = BigInteger("3")
    a **= BigInteger("4"); print(f"3 **= 4  → a = {a}")  # 81

    print("\n--- Operator Assignment Bitwise ---")

    x = BigInteger("60")   # 0b111100
    y = BigInteger("13")   # 0b001101
    print(f"x = {x} (0b{int(str(x)):b}), y = {y} (0b{int(str(y)):b})")

    x |= y;  print(f"x |= y   → x = {x}")   # 61
    x &= BigInteger("15"); print(f"x &= 15  → x = {x}")  # 13
    x ^= BigInteger("10"); print(f"x ^= 10  → x = {x}")  # 7

    p = BigInteger("5")
    p <<= BigInteger("2"); print(f"5 <<= 2  → p = {p}")   # 20
    p >>= BigInteger("1"); print(f"p >>= 1  → p = {p}")   # 10

    print("\n--- Verifikasi Linked List masih benar ---")
    z = BigInteger("45839")
    z += BigInteger("161")
    print(f"45839 + 161 = {z}")   # 46000
