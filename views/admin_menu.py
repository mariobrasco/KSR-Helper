# views/admin_menu.py

from modules.admin_manager import (
    tambahMahasiswa,
    tambahDosen,
    lihatMahasiswa,
    lihatDosen,
    hapusMahasiswa,
    hapusDosen
)


def menuAdmin(admin):
    while True:
        print("\n=== MENU ADMIN ===")
        print("Admin:", admin["nama"])
        print("------------------")
        print("1. Tambah akun mahasiswa")
        print("2. Tambah akun dosen")
        print("3. Lihat data mahasiswa")
        print("4. Lihat data dosen")
        print("5. Hapus akun mahasiswa")
        print("6. Hapus akun dosen")
        print("7. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tambahMahasiswa()

        elif pilihan == "2":
            tambahDosen()

        elif pilihan == "3":
            lihatMahasiswa()

        elif pilihan == "4":
            lihatDosen()

        elif pilihan == "5":
            hapusMahasiswa()

        elif pilihan == "6":
            hapusDosen()

        elif pilihan == "7":
            print("Logout admin berhasil.")
            break

        else:
            print("Pilihan tidak valid.")