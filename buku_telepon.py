import os

def bersihkan_layar():
    os.system('cls' if os.name == 'nt' else 'clear')

class BukuTelepon:
    def __init__(self):
        # Menggunakan dictionary untuk menyimpan Nama sebagai Key dan Nomor sebagai Value
        self.kontak = {}

    def tambah_kontak(self, nama, nomor):
        if nama in self.kontak:
            print(f"\n[!] Kontak dengan nama {nama} sudah ada.")
        else:
            self.kontak[nama] = nomor
            print(f"\n[✓] Kontak {nama} berhasil ditambahkan.")

    def cari_kontak(self, nama):
        if nama in self.kontak:
            print(f"\n--- Hasil Pencarian ---")
            print(f"Nama  : {nama}")
            print(f"Nomor : {self.kontak[nama]}")
        else:
            print(f"\n[!] Kontak {nama} tidak ditemukan.")

    def hapus_kontak(self, nama):
        if nama in self.kontak:
            del self.kontak[nama]
            print(f"\n[✓] Kontak {nama} berhasil dihapus.")
        else:
            print(f"\n[!] Gagal menghapus. Kontak {nama} tidak ditemukan.")

    def tampilkan_semua(self):
        if not self.kontak:
            print("\n[i] Buku telepon masih kosong.")
        else:
            print(f"\n{'='*30}")
            print(f"{'NAMA':<15} | {'NOMOR TELEPON'}")
            print(f"{'-'*30}")
            for nama, nomor in sorted(self.kontak.items()):
                print(f"{nama:<15} | {nomor}")
            print(f"{'='*30}")

def main():
    buku = BukuTelepon()
    
    while True:
        print("\n=== SIMULASI BUKU TELEPON ===")
        print("1. Tambah Kontak")
        print("2. Cari Kontak")
        print("3. Hapus Kontak")
        print("4. Tampilkan Semua Kontak")
        print("5. Keluar")
        
        pilihan = input("\nPilih menu (1-5): ")

        if pilihan == '1':
            nama = input("Masukkan Nama : ")
            nomor = input("Masukkan Nomor: ")
            buku.tambah_kontak(nama, nomor)
        
        elif pilihan == '2':
            nama = input("Cari Nama: ")
            buku.cari_kontak(nama)
            
        elif pilihan == '3':
            nama = input("Hapus Nama: ")
            buku.hapus_kontak(nama)
            
        elif pilihan == '4':
            buku.tampilkan_semua()
            
        elif pilihan == '5':
            print("Terima kasih! Keluar...")
            break
        
        else:
            print("[!] Pilihan tidak valid.")

        input("\nTekan Enter untuk lanjut...")
        bersihkan_layar()

if __name__ == "__main__":
    main()
