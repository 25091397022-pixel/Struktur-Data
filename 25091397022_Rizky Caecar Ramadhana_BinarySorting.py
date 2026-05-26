"""
Implementasi AdvancedSorter dan ExprHeapSorter
Tugas: Analisis & Desain Algoritma - Sorting Lanjutan & Binary Tree
"""

import math
from typing import List, Optional
from collections import deque


# =============================================================================
# BAGIAN 1: ADVANCED SORTER (Sorting Lanjutan)
# =============================================================================

class ListNode:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def __repr__(self):
        return f"ListNode({self.data})"


class AdvancedSorter:
    def __init__(self):
        pass

    # =========================================================
    # 1. ARRAY MERGE SORT (Virtual Sublists + Single tmpArray)
    # =========================================================

    def sort_array(self, arr: List[int]) -> List[int]:
        """Mengurutkan array secara ascending menggunakan Merge Sort dengan satu tmpArray."""
        if len(arr) <= 1:
            return arr
        tmp_array = [0] * len(arr)  # Single temporary array - dialokasi SEKALI
        self._rec_merge_sort(arr, 0, len(arr) - 1, tmp_array)
        return arr

    def _rec_merge_sort(self, arr, first, last, tmp_array):
        """Rekursi Merge Sort menggunakan virtual sublists (indeks, bukan slice)."""
        if first >= last:
            return
        mid = (first + last) // 2
        self._rec_merge_sort(arr, first, mid, tmp_array)
        self._rec_merge_sort(arr, mid + 1, last, tmp_array)
        self._merge_virtual(arr, first, mid, last, tmp_array)

    def _merge_virtual(self, arr, left_start, mid, right_end, tmp_array):
        """
        Menggabungkan dua virtual sublist yang bersebelahan secara STABLE.
        Sublist kiri : arr[left_start..mid]
        Sublist kanan: arr[mid+1..right_end]
        Gunakan tmp_array sebagai buffer sementara, lalu salin kembali ke arr.
        """
        a = left_start       # pointer sublist kiri
        b = mid + 1          # pointer sublist kiri
        k = left_start       # pointer ke tmp_array

        # Gabungkan dua sublist ke tmp_array
        while a <= mid and b <= right_end:
            # STABLE: gunakan <= sehingga elemen kiri diambil duluan jika sama
            if arr[a] <= arr[b]:
                tmp_array[k] = arr[a]
                a += 1
            else:
                tmp_array[k] = arr[b]
                b += 1
            k += 1

        # Salin sisa elemen sublist kiri (jika ada)
        while a <= mid:
            tmp_array[k] = arr[a]
            a += 1
            k += 1

        # Salin sisa elemen sublist kanan (jika ada)
        while b <= right_end:
            tmp_array[k] = arr[b]
            b += 1
            k += 1

        # Salin kembali dari tmp_array ke arr
        for i in range(left_start, right_end + 1):
            arr[i] = tmp_array[i]

    # =========================================================
    # 2. LINKED LIST MERGE SORT (Fast-Slow + Dummy Merge)
    # =========================================================

    def sort_linked_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Mengurutkan singly linked list secara ascending menggunakan Merge Sort."""
        # Base case: list kosong atau hanya satu node
        if head is None or head.next is None:
            return head

        # Split list menjadi dua bagian
        right_head = self._split_linked_list(head)
        left_head = head

        # Rekursi sort kedua bagian
        left_sorted = self.sort_linked_list(left_head)
        right_sorted = self.sort_linked_list(right_head)

        # Merge dua list yang sudah terurut
        return self._merge_linked_lists(left_sorted, right_sorted)

    def _split_linked_list(self, head: ListNode) -> Optional[ListNode]:
        """
        Menemukan titik tengah list menggunakan teknik fast-slow pointer
        dalam SATU traversal tanpa menghitung panjang list.

        midPoint bergerak 1 langkah, curNode bergerak 2 langkah.
        Ketika curNode mencapai akhir, midPoint berada di tengah.
        Setelah loop: putus link di midPoint, kembalikan head kanan.
        """
        midPoint = head          # bergerak 1 langkah (slow pointer)
        curNode = head.next      # bergerak 2 langkah (fast pointer)

        while curNode is not None and curNode.next is not None:
            midPoint = midPoint.next       # maju 1
            curNode = curNode.next.next    # maju 2

        # midPoint sekarang ada di tengah list
        right_head = midPoint.next   # head sublist kanan
        midPoint.next = None         # putus link agar sublist kiri berakhir di midPoint

        return right_head

    def _merge_linked_lists(self, listA: Optional[ListNode], listB: Optional[ListNode]) -> Optional[ListNode]:
        """
        Menggabungkan dua linked list yang sudah terurut secara STABLE.
        Menggunakan dummy node & tail reference - TIDAK mengalokasi node baru.
        Hanya memodifikasi pointer .next.
        """
        # Dummy node sebagai sentinel (hanya 1, statis per merge)
        dummy = ListNode(0)
        tail = dummy  # tail selalu menunjuk ke node terakhir dalam hasil

        while listA is not None and listB is not None:
            # STABLE: ambil dari listA jika sama (pertahankan urutan relatif asli)
            if listA.data <= listB.data:
                tail.next = listA
                listA = listA.next
            else:
                tail.next = listB
                listB = listB.next
            tail = tail.next  # maju tail

        # Sambungkan sisa list yang belum habis (tidak perlu loop lagi)
        tail.next = listA if listA is not None else listB

        return dummy.next  # lewati dummy node

    # =========================================================
    # 3. QUICK SORT (Median-of-Three Pivot + Depth Limiter)
    # =========================================================

    def quick_sort(self, arr: List[int]) -> List[int]:
        """Entry point Quick Sort dengan fallback ke Merge Sort jika kedalaman > 2*log2(n)."""
        if len(arr) <= 1:
            return arr
        self._quick_sort_recursive(arr, 0, len(arr) - 1, depth=0)
        return arr

    def _quick_sort_recursive(self, arr, first, last, depth=0):
        """Rekursi Quick Sort dengan depth limiter sebagai safeguard worst-case."""
        if first >= last:
            return

        n = last - first + 1
        max_depth = int(2 * math.log2(len(arr))) if len(arr) > 1 else 1

        # FALLBACK: jika kedalaman rekursi melebihi 2*log2(n), gunakan Merge Sort
        if depth > max_depth:
            sub = arr[first:last + 1]
            self.sort_array(sub)
            arr[first:last + 1] = sub
            return

        pivot_pos = self.partition_quick(arr, first, last)
        self._quick_sort_recursive(arr, first, pivot_pos - 1, depth + 1)
        self._quick_sort_recursive(arr, pivot_pos + 1, last, depth + 1)

    def partition_quick(self, arr: List[int], first: int, last: int) -> int:
        """
        Partisi dengan strategi Median-of-Three untuk memilih pivot yang lebih robust.

        Langkah:
        1. Bandingkan arr[first], arr[mid], arr[last]
        2. Tukar sehingga median berada di arr[first] sebagai pivot
        3. Jalankan partisi standar in-place
        4. Kembalikan posisi akhir pivot

        Catatan stabilitas: Quick Sort secara inherent tidak stable karena swap
        jarak jauh. Median-of-three membantu performa rata-rata tapi tidak
        menjamin stabilitas urutan elemen yang sama.
        """
        mid = (first + last) // 2

        # Urutkan arr[first], arr[mid], arr[last] secara lokal untuk temukan median
        # Tujuan: arr[first] <= arr[mid] <= arr[last]
        if arr[first] > arr[mid]:
            arr[first], arr[mid] = arr[mid], arr[first]
        if arr[first] > arr[last]:
            arr[first], arr[last] = arr[last], arr[first]
        if arr[mid] > arr[last]:
            arr[mid], arr[last] = arr[last], arr[mid]
        # Sekarang arr[mid] = median → tukar ke posisi first sebagai pivot
        arr[first], arr[mid] = arr[mid], arr[first]

        pivot = arr[first]
        left = first + 1
        right = last

        # Partisi standar (Listing 12.5)
        while True:
            # Geser left ke kanan selama arr[left] <= pivot
            while left <= right and arr[left] <= pivot:
                left += 1
            # Geser right ke kiri selama arr[right] > pivot
            while right >= left and arr[right] > pivot:
                right -= 1

            if left > right:
                break  # penanda bersilang, selesai

            # Tukar elemen yang salah posisi
            arr[left], arr[right] = arr[right], arr[left]
            left += 1
            right -= 1

        # Tempatkan pivot di posisi akhirnya
        arr[first], arr[right] = arr[right], arr[first]
        return right  # posisi pivot


# =============================================================================
# BAGIAN 2: EXPR HEAP SORTER (Binary Tree & Heapsort)
# =============================================================================

class ExprHeapSorter:
    def __init__(self, expr_str: str):
        self.expr = expr_str
        self.values = []

    def parse_and_evaluate(self) -> List[int]:
        """Membangun pohon ekspresi dari string, mengevaluasi, mengembalikan list nilai integer."""
        # Hapus spasi dan jadikan deque token karakter
        tokens = deque(self.expr.replace(" ", ""))
        root = self._build_tree(tokens)
        if root is None:
            raise ValueError("Ekspresi kosong atau tidak valid")
        result = self._eval_tree(root)
        self.values = [result]
        return self.values

    def _build_tree(self, tokens: deque) -> Optional[dict]:
        """
        Membangun pohon ekspresi secara rekursif dari antrian token.
        Pola (sesuai Listing 13.9):
          '(' → buat node kiri → ambil operator → buat node kanan → abaikan ')'
          digit → buat node operand
        Gunakan dict: {'val': operator/operand, 'left': node, 'right': node}
        """
        if not tokens:
            return None

        token = tokens.popleft()

        if token == '(':
            # Ekspresi sub: ( left op right )
            left = self._build_tree(tokens)

            # Ambil operator
            if not tokens:
                raise ValueError("Token tidak valid: operator hilang setelah '('")
            operator = tokens.popleft()
            if operator not in ('+', '-', '*', '/'):
                raise ValueError(f"Token operator tidak valid: '{operator}'")

            right = self._build_tree(tokens)

            # Abaikan ')'
            if tokens and tokens[0] == ')':
                tokens.popleft()

            return {'val': operator, 'left': left, 'right': right}

        elif token.lstrip('-').isdigit():
            # Node operand (angka)
            # Tangani angka multi-digit
            num_str = token
            while tokens and tokens[0].isdigit():
                num_str += tokens.popleft()
            return {'val': int(num_str), 'left': None, 'right': None}

        else:
            raise ValueError(f"Token tidak dikenali: '{token}'")

    def _eval_tree(self, node: Optional[dict]) -> int:
        """
        Evaluasi pohon ekspresi secara postorder.
        Tangani pembagian nol → raise ValueError.
        """
        if node is None:
            raise ValueError("Node kosong tidak dapat dievaluasi")

        # Leaf node (operand)
        if node['left'] is None and node['right'] is None:
            return node['val']

        # Evaluasi subtree kiri dan kanan (postorder)
        left_val = self._eval_tree(node['left'])
        right_val = self._eval_tree(node['right'])

        op = node['val']
        if op == '+':
            return left_val + right_val
        elif op == '-':
            return left_val - right_val
        elif op == '*':
            return left_val * right_val
        elif op == '/':
            if right_val == 0:
                raise ValueError("Pembagian dengan nol tidak diizinkan")
            return left_val // right_val  # integer division
        else:
            raise ValueError(f"Operator tidak dikenal: '{op}'")

    def heapsort_inplace(self, arr: List[int]) -> List[int]:
        """Mengurutkan array secara ascending menggunakan in-place heapsort."""
        n = len(arr)
        if n <= 1:
            return arr

        # Fase 1: Bangun max-heap dari bawah ke atas (bottom-up heapify)
        # Mulai dari node non-leaf terakhir: indeks n//2 - 1
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(arr, n, i)

        # Fase 2: Ekstraksi elemen satu per satu
        # Tukar root (max) ke akhir, kurangi heap_size, sift-down untuk pulihkan heap
        for end in range(n - 1, 0, -1):
            arr[0], arr[end] = arr[end], arr[0]   # pindahkan max ke akhir
            self._sift_down(arr, end, 0)            # pulihkan heap property

        return arr

    def _sift_down(self, arr: List[int], heap_size: int, idx: int):
        """
        Memulihkan heap order property dari idx ke bawah.
        Menggunakan rumus indeks:
          left  = 2*idx + 1
          right = 2*idx + 2
        Loop hingga posisi idx tidak berubah (largest == idx).
        """
        while True:
            largest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            # Bandingkan dengan anak kiri
            if left < heap_size and arr[left] > arr[largest]:
                largest = left

            # Bandingkan dengan anak kanan
            if right < heap_size and arr[right] > arr[largest]:
                largest = right

            # Jika idx sudah merupakan yang terbesar, selesai
            if largest == idx:
                break

            # Tukar dan lanjutkan ke bawah
            arr[idx], arr[largest] = arr[largest], arr[idx]
            idx = largest

    def is_complete_tree(self, arr: List[int]) -> bool:
        """
        Memvalidasi apakah array memenuhi properti complete binary tree.

        Pada complete binary tree berbasis array:
        - Semua indeks 0..n-1 harus terisi (tidak ada "lubang")
        - Untuk setiap node i: anak kiri = 2*i+1, anak kanan = 2*i+2
        - Setelah menemukan node dengan anak yang hilang, semua node
          berikutnya harus berupa leaf (tidak punya anak)

        Array dengan panjang n SELALU membentuk complete binary tree
        karena indeks 0..n-1 terisi penuh secara level-order.
        """
        n = len(arr)
        if n == 0:
            return True

        found_gap = False  # penanda: sudah ditemukan node dengan anak hilang

        for i in range(n):
            left = 2 * i + 1
            right = 2 * i + 2

            if left < n:
                # Ada anak kiri
                if found_gap:
                    return False  # ada "lubang" sebelum node ini → bukan complete
            else:
                # Tidak ada anak kiri → semua node setelah ini harus leaf
                found_gap = True

            if right < n:
                # Ada anak kanan
                if found_gap:
                    return False
            else:
                # Tidak ada anak kanan
                found_gap = True

        return True


# =============================================================================
# DEMO & TESTING
# =============================================================================

def linked_list_from_list(data: list) -> Optional[ListNode]:
    """Helper: buat linked list dari Python list."""
    if not data:
        return None
    head = ListNode(data[0])
    cur = head
    for val in data[1:]:
        cur.next = ListNode(val)
        cur = cur.next
    return head

def linked_list_to_list(head: Optional[ListNode]) -> list:
    """Helper: konversi linked list ke Python list."""
    result = []
    while head:
        result.append(head.data)
        head = head.next
    return result


if __name__ == "__main__":
    print("=" * 60)
    print("DEMO AdvancedSorter")
    print("=" * 60)

    sorter = AdvancedSorter()

    # 1. Array Merge Sort
    arr = [38, 27, 43, 3, 9, 82, 10]
    print(f"\n[Array Merge Sort]")
    print(f"Input : {arr}")
    result = sorter.sort_array(arr[:])
    print(f"Output: {result}")

    # 2. Linked List Sort
    ll = linked_list_from_list([38, 27, 43, 3, 9, 82, 10])
    print(f"\n[Linked List Merge Sort]")
    print(f"Input : {linked_list_to_list(ll)}")
    sorted_ll = sorter.sort_linked_list(ll)
    print(f"Output: {linked_list_to_list(sorted_ll)}")

    # 3. Quick Sort (with depth fallback)
    arr2 = [64, 34, 25, 12, 22, 11, 90]
    print(f"\n[Quick Sort (Median-of-Three)]")
    print(f"Input : {arr2}")
    result2 = sorter.quick_sort(arr2[:])
    print(f"Output: {result2}")

    # Test worst-case (descending) → fallback ke Merge Sort jika perlu
    arr_desc = list(range(20, 0, -1))
    print(f"\n[Quick Sort - Descending input (worst-case test)]")
    print(f"Input : {arr_desc}")
    result_desc = sorter.quick_sort(arr_desc[:])
    print(f"Output: {result_desc}")

    print("\n" + "=" * 60)
    print("DEMO ExprHeapSorter")
    print("=" * 60)

    # Ekspresi: ((8 * 5) + (9 / (7 - 4)))
    expr = "((8*5)+(9/(7-4)))"
    print(f"\n[Expression Evaluation]")
    print(f"Ekspresi: {expr}")
    ehs = ExprHeapSorter(expr)
    try:
        val = ehs.parse_and_evaluate()
        print(f"Hasil   : {val[0]}")  # 8*5=40, 7-4=3, 9/3=3, 40+3=43
    except ValueError as e:
        print(f"Error: {e}")

    # Heapsort in-place
    data = [43, 15, 7, 22, 8, 30, 11, 5]
    print(f"\n[HeapSort In-Place]")
    print(f"Input : {data}")
    ehs2 = ExprHeapSorter("")
    sorted_data = ehs2.heapsort_inplace(data[:])
    print(f"Output: {sorted_data}")

    # Complete tree validation
    print(f"\n[Complete Tree Validation]")
    arr_complete = [1, 2, 3, 4, 5, 6, 7]
    print(f"Array {arr_complete}: complete = {ehs2.is_complete_tree(arr_complete)}")
    arr_any = [1, 2, 3, 4, 5]
    print(f"Array {arr_any}: complete = {ehs2.is_complete_tree(arr_any)}")

    # Test division by zero
    print(f"\n[Division by Zero Handling]")
    expr_div0 = "(5/(3-3))"
    ehs3 = ExprHeapSorter(expr_div0)
    try:
        ehs3.parse_and_evaluate()
    except ValueError as e:
        print(f"Tertangkap error: {e}")

    print("\nSelesai.")
