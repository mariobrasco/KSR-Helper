# modules/auth_manager.py

from modules.csv_manager import CsvManager


def loginAdmin():
    csv_manager = CsvManager()

    id_admin = input("Masukkan ID Admin: ")
    password = input("Masukkan password: ")

    admin = csv_manager.getAdmin(id_admin)

    if admin is not None and admin["password"] == password:
        print("\nLogin admin berhasil.")
        return admin

    print("\nLogin gagal. ID admin atau password salah.")
    return None


def loginMahasiswa():
    csv_manager = CsvManager()

    nim = input("Masukkan NIM: ")
    password = input("Masukkan password: ")

    mahasiswa = csv_manager.getMahasiswa(nim)

    if mahasiswa is not None and mahasiswa["password"] == password:
        print("\nLogin mahasiswa berhasil.")
        return mahasiswa

    print("\nLogin gagal. NIM atau password salah.")
    return None


def loginDosen():
    csv_manager = CsvManager()

    nip = input("Masukkan NIP: ")
    password = input("Masukkan password: ")

    dosen = csv_manager.getDosen(nip)

    if dosen is not None and dosen["password"] == password:
        print("\nLogin dosen berhasil.")
        return dosen

    print("\nLogin gagal. NIP atau password salah.")
    return None