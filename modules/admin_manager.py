# modules/admin_manager.py

from modules.csv_manager import CsvManager


def tambahMahasiswa():
    csv_manager = CsvManager()

    print("\n=== TAMBAH AKUN MAHASISWA ===")

    nim = input("Masukkan NIM: ")

    if csv_manager.getMahasiswa(nim) is not None:
        print("NIM sudah terdaftar.")
        return

    nama = input("Masukkan nama mahasiswa: ")
    password = input("Masukkan password awal: ")
    nip_dosen_wali = input("Masukkan NIP dosen wali: ")

    if csv_manager.getDosen(nip_dosen_wali) is None:
        print("NIP dosen wali tidak ditemukan.")
        return

    data_mahasiswa = {
        "nim": nim,
        "nama": nama,
        "password": password,
        "nip_dosen_wali": nip_dosen_wali,
        "matkul_lulus": "-"
    }

    csv_manager.tambahMahasiswa(data_mahasiswa)

    print("Akun mahasiswa berhasil ditambahkan.")


def tambahDosen():
    csv_manager = CsvManager()

    print("\n=== TAMBAH AKUN DOSEN ===")

    nip = input("Masukkan NIP: ")

    if csv_manager.getDosen(nip) is not None:
        print("NIP sudah terdaftar.")
        return

    nama = input("Masukkan nama dosen: ")
    password = input("Masukkan password awal: ")

    print("\nMasukkan kode mata kuliah yang diampu.")
    print("Jika lebih dari satu, pisahkan dengan tanda ';'")
    print("Contoh: RL117;RL216")
    dosen_mk = input("Kode mata kuliah yang diampu: ")

    data_dosen = {
        "nip": nip,
        "nama": nama,
        "password": password,
        "dosen_mk": dosen_mk
    }

    csv_manager.tambahDosen(data_dosen)

    print("Akun dosen berhasil ditambahkan.")


def lihatMahasiswa():
    csv_manager = CsvManager()
    semua_mahasiswa = csv_manager.getSemuaMahasiswa()

    print("\n=== DATA MAHASISWA ===")

    if len(semua_mahasiswa) == 0:
        print("Belum ada data mahasiswa.")
        return

    print(f"{'No':<4} | {'NIM':<12} | {'Nama':<35} | {'Dosen Wali':<15} | {'Matkul Lulus':<30}")
    print("-" * 105)

    nomor = 1

    for mahasiswa in semua_mahasiswa:
        print(
            f"{nomor:<4} | "
            f"{mahasiswa['nim']:<12} | "
            f"{mahasiswa['nama']:<35} | "
            f"{mahasiswa['nip_dosen_wali']:<15} | "
            f"{mahasiswa['matkul_lulus']:<30}"
        )
        nomor += 1


def lihatDosen():
    csv_manager = CsvManager()
    semua_dosen = csv_manager.getSemuaDosen()

    print("\n=== DATA DOSEN ===")

    if len(semua_dosen) == 0:
        print("Belum ada data dosen.")
        return

    print(f"{'No':<4} | {'NIP':<15} | {'Nama':<35} | {'Mata Kuliah Diampu':<30}")
    print("-" * 95)

    nomor = 1

    for dosen in semua_dosen:
        print(
            f"{nomor:<4} | "
            f"{dosen['nip']:<15} | "
            f"{dosen['nama']:<35} | "
            f"{dosen['dosen_mk']:<30}"
        )
        nomor += 1


def hapusMahasiswa():
    csv_manager = CsvManager()

    print("\n=== HAPUS AKUN MAHASISWA ===")

    nim = input("Masukkan NIM mahasiswa yang akan dihapus: ")

    berhasil = csv_manager.hapusMahasiswa(nim)

    if berhasil:
        print("Akun mahasiswa berhasil dihapus.")
    else:
        print("NIM tidak ditemukan.")


def hapusDosen():
    csv_manager = CsvManager()

    print("\n=== HAPUS AKUN DOSEN ===")

    nip = input("Masukkan NIP dosen yang akan dihapus: ")

    berhasil = csv_manager.hapusDosen(nip)

    if berhasil:
        print("Akun dosen berhasil dihapus.")
    else:
        print("NIP tidak ditemukan.")