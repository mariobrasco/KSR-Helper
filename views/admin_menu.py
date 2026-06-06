# views/admin_menu.py

from modules.admin_manager import (
    tambahMahasiswa,
    tambahDosen,
    lihatMahasiswa,
    lihatDosen,
    lihatMataKuliah,
    lihatKelas,
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
        print("5. Lihat data mata kuliah")
        print("6. Lihat data kelas")
        print("7. Hapus akun mahasiswa")
        print("8. Hapus akun dosen")
        print("9. Logout")

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
            lihatMataKuliah()

        elif pilihan == "6":
            lihatKelas()

        elif pilihan == "7":
            hapusMahasiswa()

        elif pilihan == "8":
            hapusDosen()

        elif pilihan == "9":
            print("Logout admin berhasil.")
            break

        else:
            print("Pilihan tidak valid.")