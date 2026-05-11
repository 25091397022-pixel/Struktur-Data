"""
====================================================================
LATIHAN: Advanced Linked Lists
Materi   : Chapter 9 - Advanced Linked Lists (Struktur Data Lanjut)
====================================================================

Soal:
    "Rancang struktur data untuk aplikasi note-taking yang mendukung:
     1. Multiple tags per note  (multi-linked by tag)
     2. Chronological dan alphabetical views  (doubly linked sorted)
     3. Sync status tracking  (circular buffer for recent changes)"
====================================================================
"""

from datetime import datetime


# ─────────────────────────────────────────────────────────────────
# BAGIAN 1 ─ MULTI-LINKED LIST  (Multiple Tags per Note)
# ─────────────────────────────────────────────────────────────────
#
# Setiap NoteNode memiliki DUA chain pointer:
#   - nextByTime  : menyusun note secara kronologis (doubly linked)
#   - prevByTime
#   - nextByAlpha : menyusun note secara alfabetis berdasarkan judul
#   - prevByAlpha
#
# Selain itu, setiap note dapat memiliki banyak tag (multi-linked):
#   - tagHead     : linked list TagNode yang melekat pada note ini


class TagNode:
    """Node untuk linked list tag di dalam satu note."""
    def __init__(self, tag_name: str):
        self.tag_name = tag_name
        self.next_tag = None          # pointer ke tag berikutnya pada note yang sama

    def __repr__(self):
        return f"Tag({self.tag_name!r})"


class NoteNode:
    """
    Node utama yang mewakili satu catatan.
    Setiap node sekaligus menjadi anggota DUA chain doubly-linked list:
      - Chain kronologis  (diurutkan berdasarkan created_at)
      - Chain alfabetis   (diurutkan berdasarkan title)
    serta memiliki linked list internal berisi tag-tagnya.
    """
    def __init__(self, title: str, content: str):
        self.title      = title
        self.content    = content
        self.created_at = datetime.now()   # timestamp pencatatan

        # ── Pointer chain kronologis ──────────────────────────────
        self.next_by_time = None
        self.prev_by_time = None

        # ── Pointer chain alfabetis ───────────────────────────────
        self.next_by_alpha = None
        self.prev_by_alpha = None

        # ── Tag list internal (multi-linked) ──────────────────────
        self.tag_head = None          # kepala linked list tag note ini

    # ── Helpers tag ───────────────────────────────────────────────
    def add_tag(self, tag_name: str):
        """Tambahkan tag ke note ini (tidak duplikat)."""
        cur = self.tag_head
        while cur is not None:
            if cur.tag_name == tag_name:
                return                # sudah ada, abaikan
            cur = cur.next_tag
        new_tag = TagNode(tag_name)
        new_tag.next_tag = self.tag_head
        self.tag_head = new_tag

    def remove_tag(self, tag_name: str):
        """Hapus tag dari note ini jika ada."""
        prev, cur = None, self.tag_head
        while cur is not None:
            if cur.tag_name == tag_name:
                if prev is None:
                    self.tag_head = cur.next_tag
                else:
                    prev.next_tag = cur.next_tag
                return
            prev, cur = cur, cur.next_tag

    def get_tags(self) -> list:
        """Kembalikan semua tag sebagai list string."""
        tags, cur = [], self.tag_head
        while cur is not None:
            tags.append(cur.tag_name)
            cur = cur.next_tag
        return tags

    def has_tag(self, tag_name: str) -> bool:
        cur = self.tag_head
        while cur is not None:
            if cur.tag_name == tag_name:
                return True
            cur = cur.next_tag
        return False

    def __repr__(self):
        return (f"Note(title={self.title!r}, "
                f"tags={self.get_tags()}, "
                f"created={self.created_at.strftime('%Y-%m-%d %H:%M:%S')})")


# ─────────────────────────────────────────────────────────────────
# BAGIAN 2 ─ DOUBLY LINKED LIST  (Chronological & Alphabetical)
# ─────────────────────────────────────────────────────────────────

class NoteCollection:
    """
    Mengelola dua doubly linked list yang berbagi node NoteNode yang sama:
      - chrono_head / chrono_tail : urutan kronologis (ascending created_at)
      - alpha_head  / alpha_tail  : urutan alfabetis  (ascending title)
    Insert dilakukan SORTED agar kedua chain selalu terurut.
    """

    def __init__(self):
        # Chain kronologis
        self.chrono_head = None
        self.chrono_tail = None
        # Chain alfabetis
        self.alpha_head  = None
        self.alpha_tail  = None

        self._count = 0

    # ── Insert sorted ke chain kronologis ─────────────────────────
    def _insert_chrono(self, node: NoteNode):
        """Sisipkan node ke dalam chain kronologis (ascending created_at)."""
        if self.chrono_head is None:                          # list kosong
            self.chrono_head = self.chrono_tail = node
            node.next_by_time = node.prev_by_time = None
            return

        if node.created_at <= self.chrono_head.created_at:   # depan
            node.next_by_time = self.chrono_head
            self.chrono_head.prev_by_time = node
            self.chrono_head = node
            return

        if node.created_at >= self.chrono_tail.created_at:   # belakang
            node.prev_by_time = self.chrono_tail
            self.chrono_tail.next_by_time = node
            self.chrono_tail = node
            return

        cur = self.chrono_head                                # tengah
        while cur is not None and cur.created_at < node.created_at:
            cur = cur.next_by_time
        # sisipkan sebelum cur
        node.next_by_time = cur
        node.prev_by_time = cur.prev_by_time
        cur.prev_by_time.next_by_time = node
        cur.prev_by_time = node

    # ── Insert sorted ke chain alfabetis ──────────────────────────
    def _insert_alpha(self, node: NoteNode):
        """Sisipkan node ke dalam chain alfabetis (ascending title)."""
        if self.alpha_head is None:                           # list kosong
            self.alpha_head = self.alpha_tail = node
            node.next_by_alpha = node.prev_by_alpha = None
            return

        if node.title.lower() <= self.alpha_head.title.lower():  # depan
            node.next_by_alpha = self.alpha_head
            self.alpha_head.prev_by_alpha = node
            self.alpha_head = node
            return

        if node.title.lower() >= self.alpha_tail.title.lower():  # belakang
            node.prev_by_alpha = self.alpha_tail
            self.alpha_tail.next_by_alpha = node
            self.alpha_tail = node
            return

        cur = self.alpha_head                                 # tengah
        while cur is not None and cur.title.lower() < node.title.lower():
            cur = cur.next_by_alpha
        node.next_by_alpha = cur
        node.prev_by_alpha = cur.prev_by_alpha
        cur.prev_by_alpha.next_by_alpha = node
        cur.prev_by_alpha = node

    # ── Hapus dari chain kronologis ───────────────────────────────
    def _remove_chrono(self, node: NoteNode):
        if node.prev_by_time:
            node.prev_by_time.next_by_time = node.next_by_time
        else:
            self.chrono_head = node.next_by_time
        if node.next_by_time:
            node.next_by_time.prev_by_time = node.prev_by_time
        else:
            self.chrono_tail = node.prev_by_time
        node.next_by_time = node.prev_by_time = None

    # ── Hapus dari chain alfabetis ────────────────────────────────
    def _remove_alpha(self, node: NoteNode):
        if node.prev_by_alpha:
            node.prev_by_alpha.next_by_alpha = node.next_by_alpha
        else:
            self.alpha_head = node.next_by_alpha
        if node.next_by_alpha:
            node.next_by_alpha.prev_by_alpha = node.prev_by_alpha
        else:
            self.alpha_tail = node.prev_by_alpha
        node.next_by_alpha = node.prev_by_alpha = None

    # ── API Publik ─────────────────────────────────────────────────
    def add_note(self, title: str, content: str,
                 tags: list = None) -> NoteNode:
        """
        Buat note baru, sisipkan ke KEDUA chain secara sorted,
        dan daftarkan semua tag-nya.
        Kompleksitas: O(n) untuk pencarian posisi insert di tiap chain.
        """
        node = NoteNode(title, content)
        if tags:
            for t in tags:
                node.add_tag(t)
        self._insert_chrono(node)
        self._insert_alpha(node)
        self._count += 1
        return node

    def delete_note(self, node: NoteNode):
        """
        Hapus note dari KEDUA chain.
        Kompleksitas: O(1) karena doubly linked list.
        """
        self._remove_chrono(node)
        self._remove_alpha(node)
        self._count -= 1

    def find_by_tag(self, tag_name: str) -> list:
        """
        Telusuri chain kronologis dan kembalikan semua note
        yang memiliki tag tertentu.
        Kompleksitas: O(n)
        """
        result, cur = [], self.chrono_head
        while cur is not None:
            if cur.has_tag(tag_name):
                result.append(cur)
            cur = cur.next_by_time
        return result

    def traverse_chronological(self, reverse: bool = False) -> list:
        """Tampilkan semua note sesuai urutan waktu."""
        result = []
        if not reverse:
            cur = self.chrono_head
            while cur is not None:
                result.append(cur)
                cur = cur.next_by_time
        else:
            cur = self.chrono_tail
            while cur is not None:
                result.append(cur)
                cur = cur.prev_by_time
        return result

    def traverse_alphabetical(self, reverse: bool = False) -> list:
        """Tampilkan semua note sesuai urutan abjad."""
        result = []
        if not reverse:
            cur = self.alpha_head
            while cur is not None:
                result.append(cur)
                cur = cur.next_by_alpha
        else:
            cur = self.alpha_tail
            while cur is not None:
                result.append(cur)
                cur = cur.prev_by_alpha
        return result

    def __len__(self):
        return self._count


# ─────────────────────────────────────────────────────────────────
# BAGIAN 3 ─ CIRCULAR BUFFER  (Sync Status Tracking)
# ─────────────────────────────────────────────────────────────────
#
# Circular linked list dengan kapasitas tetap digunakan untuk
# melacak N perubahan terakhir (recent sync changes).
# Ketika buffer penuh, entri terlama otomatis ditimpa.
#
# Struktur:
#   listRef → node terakhir yang diisi (konvensi Slide 19)
#   listRef.next → node terlama (node pertama dalam urutan logis)

class SyncRecord:
    """Satu record perubahan (change event)."""
    def __init__(self, note_title: str, action: str):
        self.note_title = note_title
        self.action     = action           # 'CREATE', 'UPDATE', 'DELETE'
        self.timestamp  = datetime.now()

    def __repr__(self):
        return (f"SyncRecord(action={self.action!r}, "
                f"note={self.note_title!r}, "
                f"time={self.timestamp.strftime('%H:%M:%S')})")


class CircularBufferNode:
    """Node dalam circular linked list untuk sync buffer."""
    def __init__(self):
        self.record = None        # SyncRecord atau None (slot kosong)
        self.next   = None


class SyncCircularBuffer:
    """
    Circular linked list berkapasitas tetap (capacity).
    Digunakan sebagai ring buffer untuk mencatat perubahan terbaru.

    Ilustrasi (capacity=4):
        [slot0] → [slot1] → [slot2] → [slot3] ─┐
           ↑___________________________________|
    listRef selalu menunjuk ke slot yang BARU SAJA ditulis.
    """

    def __init__(self, capacity: int = 10):
        if capacity < 1:
            raise ValueError("Kapasitas minimal 1")
        self._capacity = capacity
        self._size     = 0        # jumlah record yang tersimpan (<= capacity)

        # Bangun circular linked list dengan 'capacity' slot kosong
        first = CircularBufferNode()
        cur   = first
        for _ in range(capacity - 1):
            nxt      = CircularBufferNode()
            cur.next = nxt
            cur      = nxt
        cur.next = first          # tutup lingkaran

        # listRef menunjuk ke node SEBELUM first (= node terakhir saat ini)
        # agar add() pertama kali menulis ke 'first'
        self._listRef = cur       # cur adalah node terakhir = "tail"

    def add(self, note_title: str, action: str):
        """
        Tambahkan sync record baru.
        Jika penuh, node terlama ditimpa (ring buffer overwrite).
        Kompleksitas: O(1)
        """
        self._listRef = self._listRef.next   # maju ke slot berikutnya
        self._listRef.record = SyncRecord(note_title, action)
        if self._size < self._capacity:
            self._size += 1

    def get_recent(self, n: int = None) -> list:
        """
        Kembalikan hingga n record terbaru (default: semua).
        Urutan: terbaru → terlama.
        Kompleksitas: O(min(n, capacity))
        """
        if n is None or n > self._size:
            n = self._size
        result = []
        cur = self._listRef
        for _ in range(n):
            if cur.record is not None:
                result.append(cur.record)
            cur = cur.next        # tapi kita perlu mundur... gunakan cara lain
            # Koreksi: traversal mundur tidak tersedia pada singly circular,
            # maka kita kumpulkan semua lalu slice dari belakang.
            # Lihat implementasi _collect() di bawah.
        # Gunakan helper:
        return self._collect()[:n]

    def _collect(self) -> list:
        """Kumpulkan semua record dari terbaru ke terlama."""
        if self._size == 0:
            return []
        result = []
        # listRef = node paling baru; putar mundur via full traversal
        # Kita kumpulkan semua slot dalam urutan maju lalu reverse
        all_nodes = []
        cur  = self._listRef
        done = False
        seen = 0
        while not done:
            if cur.record is not None:
                all_nodes.append(cur.record)
                seen += 1
            cur  = cur.next
            done = (cur is self._listRef) or (seen >= self._capacity)
        # all_nodes[0] = listRef = terbaru, tapi kita maju sehingga
        # sebenarnya urutan sudah dari terbaru → memutar kembali ke terbaru.
        # Karena kita mulai dari listRef dan maju, all_nodes pertama = terbaru.
        return all_nodes

    def get_recent_n(self, n: int) -> list:
        """Kembalikan n record terbaru."""
        return self._collect()[:n]

    def is_full(self) -> bool:
        return self._size == self._capacity

    def __len__(self):
        return self._size

    def __repr__(self):
        return (f"SyncCircularBuffer(capacity={self._capacity}, "
                f"size={self._size})")


# ─────────────────────────────────────────────────────────────────
# DEMO & PENGUJIAN
# ─────────────────────────────────────────────────────────────────

def separator(title: str):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")


def demo():
    import time

    # ── 1. Buat koleksi note ───────────────────────────────────────
    separator("1. Membuat NoteCollection & Menambah Note")
    collection = NoteCollection()
    sync_buf   = SyncCircularBuffer(capacity=5)

    notes_data = [
        ("Zebrafish Study",  "Penelitian ikan zebra.",        ["biology", "research"]),
        ("Python Tips",      "Tips seputar Python.",          ["python", "programming"]),
        ("Algorithm Notes",  "Catatan algoritma dasar.",      ["cs", "algorithm"]),
        ("Mango Recipe",     "Resep es mangga.",              ["food", "recipe"]),
        ("Biology Basics",   "Pengenalan biologi sel.",       ["biology", "education"]),
        ("Data Structures",  "Linked list, tree, graph.",     ["cs", "programming"]),
    ]

    node_refs = []
    for title, content, tags in notes_data:
        n = collection.add_note(title, content, tags)
        node_refs.append(n)
        sync_buf.add(title, "CREATE")
        time.sleep(0.01)   # pastikan timestamp berbeda-beda

    print(f"Total note ditambahkan : {len(collection)}")

    # ── 2. Tampilkan view kronologis ───────────────────────────────
    separator("2. Chronological View (terlama → terbaru)")
    for i, n in enumerate(collection.traverse_chronological(), 1):
        print(f"  {i}. [{n.created_at.strftime('%H:%M:%S.%f')[:-3]}] "
              f"{n.title}  tags={n.get_tags()}")

    separator("2b. Reverse Chronological (terbaru → terlama)")
    for i, n in enumerate(collection.traverse_chronological(reverse=True), 1):
        print(f"  {i}. {n.title}")

    # ── 3. Tampilkan view alfabetis ────────────────────────────────
    separator("3. Alphabetical View (A → Z)")
    for i, n in enumerate(collection.traverse_alphabetical(), 1):
        print(f"  {i}. {n.title}")

    separator("3b. Reverse Alphabetical (Z → A)")
    for i, n in enumerate(collection.traverse_alphabetical(reverse=True), 1):
        print(f"  {i}. {n.title}")

    # ── 4. Multi-linked: cari note berdasarkan tag ─────────────────
    separator("4. Cari Note berdasarkan Tag")
    for tag in ["biology", "cs", "programming", "recipe"]:
        found = collection.find_by_tag(tag)
        print(f"  Tag '{tag}' ({len(found)} note): "
              f"{[n.title for n in found]}")

    # ── 5. Tambah & hapus tag secara dinamis ──────────────────────
    separator("5. Manipulasi Tag Secara Dinamis")
    target = node_refs[0]   # Zebrafish Study
    print(f"  Sebelum : {target.title} → tags={target.get_tags()}")
    target.add_tag("genetics")
    target.add_tag("biology")    # duplikat, diabaikan
    print(f"  Sesudah tambah 'genetics' : tags={target.get_tags()}")
    target.remove_tag("research")
    print(f"  Sesudah hapus 'research'  : tags={target.get_tags()}")

    # ── 6. Hapus note ─────────────────────────────────────────────
    separator("6. Hapus Note dari Kedua Chain")
    del_note = node_refs[3]   # Mango Recipe
    print(f"  Menghapus: {del_note.title}")
    collection.delete_note(del_note)
    sync_buf.add(del_note.title, "DELETE")
    print(f"  Sisa note (kronologis) : "
          f"{[n.title for n in collection.traverse_chronological()]}")
    print(f"  Sisa note (alfabetis)  : "
          f"{[n.title for n in collection.traverse_alphabetical()]}")

    # ── 7. Sync buffer tracking ───────────────────────────────────
    separator("7. Sync Circular Buffer (Recent Changes)")
    # Tambah lebih banyak event untuk uji overwrite
    sync_buf.add("Python Tips", "UPDATE")
    sync_buf.add("Biology Basics", "UPDATE")

    print(f"  Buffer: {sync_buf}")
    print(f"  Semua record (terbaru dulu):")
    for i, rec in enumerate(sync_buf._collect(), 1):
        print(f"    {i}. [{rec.timestamp.strftime('%H:%M:%S')}] "
              f"{rec.action:6s} → {rec.note_title!r}")

    print(f"\n  3 perubahan terbaru saja:")
    for rec in sync_buf.get_recent_n(3):
        print(f"    • {rec.action} → {rec.note_title!r}")

    # Uji overwrite (tambahkan melebihi kapasitas=5)
    separator("8. Uji Overwrite Buffer (capacity=5)")
    extra_events = [("Note X", "CREATE"), ("Note Y", "CREATE"),
                    ("Note Z", "UPDATE")]
    for title, action in extra_events:
        sync_buf.add(title, action)
        print(f"  Tambah [{action}] {title!r}  → buffer size={len(sync_buf)}")

    print(f"\n  Isi buffer setelah overwrite (kapasitas={sync_buf._capacity}):")
    for i, rec in enumerate(sync_buf._collect(), 1):
        print(f"    {i}. {rec.action:6s} → {rec.note_title!r}")

    separator("SELESAI")
    print("  Semua fitur berjalan dengan benar.")
    print()


if __name__ == "__main__":
    demo()
