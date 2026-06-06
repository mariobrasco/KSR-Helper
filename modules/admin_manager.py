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

    print("\n--- PILIH DOSEN WALI ---")
    tampilkanDosenSingkat(csv_manager)

    nip_dosen_wali = input("Masukkan NIP dosen wali: ")

    if csv_manager.getDosen(nip_dosen_wali) is None:
        print("NIP dosen wali tidak ditemukan.")
        return

    semester = input("Masukkan semester mahasiswa contoh 1 sampai 8: ")

    if not semester.isdigit():
        print("Semester harus berupa angka.")
        return

    if int(semester) < 1 or int(semester) > 8:
        print("Semester hanya boleh dari 1 sampai 8.")
        return

    ip_terakhir = input("Masukkan IP terakhir contoh 3.50, untuk semester 1 isi 0.00: ")

    try:
        nilai_ip = float(ip_terakhir)

        if nilai_ip < 0 or nilai_ip > 4:
            print("IP harus berada di rentang 0.00 sampai 4.00.")
            return

    except ValueError:
        print("Format IP tidak valid. Gunakan titik, contoh 3.50.")
        return

    print("\nMasukkan kode mata kuliah yang sudah lulus.")
    print("Pisahkan dengan tanda ';'")
    print("Contoh: RL118;RL117;RL115")
    print("Isi '-' jika belum ada.")
    matkul_lulus = input("Mata kuliah lulus: ").upper()

    if matkul_lulus.strip() == "":
        matkul_lulus = "-"

    data_mahasiswa = {
        "nim": nim,
        "nama": nama,
        "password": password,
        "nip_dosen_wali": nip_dosen_wali,
        "matkul_lulus": matkul_lulus,
        "semester": semester,
        "ip_terakhir": str(nilai_ip)
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

    print("\n--- DAFTAR KELAS TERSEDIA ---")
    tampilkanKelasSingkat(csv_manager)

    print("\nMasukkan ID kelas yang diampu dosen.")
    print("Jika lebih dari satu, pisahkan dengan tanda ';'")
    print("Contoh: RL216-A;RL216-B")
    print("Isi '-' jika belum ada kelas yang diampu.")
    dosen_mk = input("ID kelas yang diampu: ").upper()

    if dosen_mk.strip() == "":
        dosen_mk = "-"

    if dosen_mk != "-":
        daftar_id_kelas = dosen_mk.split(";")

        for id_kelas in daftar_id_kelas:
            if csv_manager.getKelas(id_kelas) is None:
                print(f"ID kelas {id_kelas} tidak ditemukan.")
                return

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

    print(
        f"{'No':<4} | "
        f"{'NIM':<12} | "
        f"{'Nama':<35} | "
        f"{'Semester':<8} | "
        f"{'IP':<6} | "
        f"{'Dosen Wali':<15} | "
        f"{'Matkul Lulus':<50}"
    )
    print("-" * 150)

    nomor = 1

    for mahasiswa in semua_mahasiswa:
        print(
            f"{nomor:<4} | "
            f"{mahasiswa['nim']:<12} | "
            f"{mahasiswa['nama']:<35} | "
            f"{mahasiswa['semester']:<8} | "
            f"{mahasiswa['ip_terakhir']:<6} | "
            f"{mahasiswa['nip_dosen_wali']:<15} | "
            f"{mahasiswa['matkul_lulus']:<50}"
        )

        nomor += 1


def lihatDosen():
    csv_manager = CsvManager()
    semua_dosen = csv_manager.getSemuaDosen()

    print("\n=== DATA DOSEN ===")

    if len(semua_dosen) == 0:
        print("Belum ada data dosen.")
        return

    print(
        f"{'No':<4} | "
        f"{'NIP':<15} | "
        f"{'Nama':<35} | "
        f"{'Kelas Diampu':<80}"
    )
    print("-" * 145)

    nomor = 1

    for dosen in semua_dosen:
        print(
            f"{nomor:<4} | "
            f"{dosen['nip']:<15} | "
            f"{dosen['nama']:<35} | "
            f"{dosen['dosen_mk']:<80}"
        )

        nomor += 1


def lihatMataKuliah():
    csv_manager = CsvManager()
    semua_matkul = csv_manager.getSemuaMataKuliah()

    print("\n=== DATA MATA KULIAH ===")

    if len(semua_matkul) == 0:
        print("Belum ada data mata kuliah.")
        return

    print(
        f"{'No':<4} | "
        f"{'Kode':<8} | "
        f"{'Mata Kuliah':<45} | "
        f"{'SKS':<3} | "
        f"{'Smt':<3} | "
        f"{'Prasyarat':<28} | "
        f"{'Kelompok':<25} | "
        f"{'Min SKS':<7}"
    )
    print("-" * 150)

    nomor = 1

    for matkul in semua_matkul:
        print(
            f"{nomor:<4} | "
            f"{matkul['kode']:<8} | "
            f"{matkul['nama']:<45} | "
            f"{matkul['sks']:<3} | "
            f"{matkul['semester']:<3} | "
            f"{matkul['prasyarat']:<28} | "
            f"{matkul['kelompok_pilihan']:<25} | "
            f"{matkul['min_sks_lulus']:<7}"
        )

        nomor += 1


def lihatKelas():
    csv_manager = CsvManager()
    semua_kelas = csv_manager.getSemuaKelas()

    print("\n=== DATA KELAS ===")

    if len(semua_kelas) == 0:
        print("Belum ada data kelas.")
        return

    print(
        f"{'No':<4} | "
        f"{'ID Kelas':<10} | "
        f"{'Kode MK':<8} | "
        f"{'Mata Kuliah':<38} | "
        f"{'Kls':<3} | "
        f"{'Kuota':<5} | "
        f"{'Hari':<8} | "
        f"{'Jam':<12} | "
        f"{'Ruangan':<24} | "
        f"{'Dosen':<28}"
    )
    print("-" * 175)

    nomor = 1

    for kelas in semua_kelas:
        matkul = csv_manager.getMataKuliah(kelas["kode_matkul"])
        dosen = csv_manager.getDosen(kelas["nip_dosen"])

        nama_matkul = "-"
        nama_dosen = "-"

        if matkul is not None:
            nama_matkul = matkul["nama"]

        if dosen is not None:
            nama_dosen = dosen["nama"]

        print(
            f"{nomor:<4} | "
            f"{kelas['id_kelas']:<10} | "
            f"{kelas['kode_matkul']:<8} | "
            f"{nama_matkul:<38} | "
            f"{kelas['nama_kelas']:<3} | "
            f"{kelas['kuota']:<5} | "
            f"{kelas['hari']:<8} | "
            f"{kelas['jam']:<12} | "
            f"{kelas['ruangan']:<24} | "
            f"{nama_dosen:<28}"
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


def tampilkanDosenSingkat(csv_manager):
    semua_dosen = csv_manager.getSemuaDosen()

    if len(semua_dosen) == 0:
        print("Belum ada data dosen.")
        return

    print(f"{'NIP':<15} | {'Nama':<35}")
    print("-" * 55)

    for dosen in semua_dosen:
        print(f"{dosen['nip']:<15} | {dosen['nama']:<35}")


def tampilkanKelasSingkat(csv_manager):
    semua_kelas = csv_manager.getSemuaKelas()

    if len(semua_kelas) == 0:
        print("Belum ada data kelas.")
        return

    print(
        f"{'ID Kelas':<10} | "
        f"{'Kode MK':<8} | "
        f"{'Mata Kuliah':<35} | "
        f"{'Kls':<3} | "
        f"{'Hari':<8} | "
        f"{'Jam':<12} | "
        f"{'Dosen':<28}"
    )
    print("-" * 125)

    for kelas in semua_kelas:
        matkul = csv_manager.getMataKuliah(kelas["kode_matkul"])
        dosen = csv_manager.getDosen(kelas["nip_dosen"])

        nama_matkul = "-"
        nama_dosen = "-"

        if matkul is not None:
            nama_matkul = matkul["nama"]

        if dosen is not None:
            nama_dosen = dosen["nama"]

        print(
            f"{kelas['id_kelas']:<10} | "
            f"{kelas['kode_matkul']:<8} | "
            f"{nama_matkul:<35} | "
            f"{kelas['nama_kelas']:<3} | "
            f"{kelas['hari']:<8} | "
            f"{kelas['jam']:<12} | "
            f"{nama_dosen:<28}"
        )