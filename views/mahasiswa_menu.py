# views/mahasiswa_menu.py


def menuMahasiswa(mahasiswa, krs_logic):
    while True:
        print("\n=== MENU MAHASISWA ===")
        print("Nama     :", mahasiswa["nama"])
        print("NIM      :", mahasiswa["nim"])
        print("Semester :", mahasiswa["semester"])
        print("IP       :", mahasiswa["ip_terakhir"])
        print("----------------------")
        print("1. Lihat kelas yang bisa diambil")
        print("2. Lihat tree prasyarat")
        print("3. Ambil kelas mata kuliah")
        print("4. Batalkan kelas mata kuliah")
        print("5. Lihat status KRS saya")
        print("6. Lihat waiting list saya")
        print("7. Lihat hasil KRS / jadwal mingguan")
        print("8. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkanDaftarKelas(mahasiswa, krs_logic)

        elif pilihan == "2":
            menuTreePrasyarat(mahasiswa, krs_logic)

        elif pilihan == "3":
            ambilMataKuliah(mahasiswa, krs_logic)

        elif pilihan == "4":
            batalkanMataKuliah(mahasiswa, krs_logic)

        elif pilihan == "5":
            tampilkanStatusKrs(mahasiswa, krs_logic)

        elif pilihan == "6":
            tampilkanWaitingListMahasiswa(mahasiswa, krs_logic)

        elif pilihan == "7":
            krs_logic.cetakHasilKrs(mahasiswa["nim"])

        elif pilihan == "8":
            print("Logout mahasiswa berhasil.")
            break

        else:
            print("Pilihan tidak valid.")


def tampilkanDaftarKelas(mahasiswa, krs_logic):
    daftar_kelas = krs_logic.getDaftarKelasTersedia(mahasiswa["nim"])

    print(f"\n--- DAFTAR KELAS YANG BISA DIAMBIL MAHASISWA SEMESTER {mahasiswa['semester']} ---")

    if len(daftar_kelas) == 0:
        print("Belum ada kelas yang tersedia untuk kamu.")
        print("Kemungkinan semua mata kuliah semester ini sudah lulus/diambil, atau prasyarat belum terpenuhi.")
        return

    print(
        f"{'ID Kelas':<10} | "
        f"{'Kode MK':<8} | "
        f"{'Mata Kuliah':<40} | "
        f"{'SKS':<3} | "
        f"{'Dosen Pengampu':<28} | "
        f"{'Kelas':<5} | "
        f"{'Hari':<8} | "
        f"{'Jam':<12} | "
        f"{'Ruangan':<22} | "
        f"{'Peserta':<8} | "
        f"{'WL':<3}"
    )
    print("-" * 170)

    for kelas in daftar_kelas:
        print(
            f"{kelas['id_kelas']:<10} | "
            f"{kelas['kode_matkul']:<8} | "
            f"{kelas['nama']:<40} | "
            f"{kelas['sks']:<3} | "
            f"{kelas['nama_dosen']:<28} | "
            f"{kelas['nama_kelas']:<5} | "
            f"{kelas['hari']:<8} | "
            f"{kelas['jam']:<12} | "
            f"{kelas['ruangan']:<22} | "
            f"{kelas['peserta']:<8} | "
            f"{kelas['waiting']:<3}"
        )

    print("-" * 170)
    print("Keterangan:")
    print("Peserta = jumlah mahasiswa masuk kelas / kuota kelas")
    print("WL      = jumlah mahasiswa di waiting list")
    print("Catatan : kelas yang tampil adalah kelas yang memenuhi semester, prasyarat, dan belum pernah kamu ambil/lulus.")


def menuTreePrasyarat(mahasiswa, krs_logic):
    while True:
        print("\n=== MENU TREE PRASYARAT ===")
        print("1. Lihat tree seluruh prasyarat menuju Skripsi")
        print("2. Lihat tree mata kuliah semester saya")
        print("3. Lihat tree mata kuliah semester sebelumnya")
        print("4. Lihat tree mata kuliah semester berikutnya")
        print("5. Kembali")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            print("\n--- TREE SELURUH PRASYARAT MENUJU SKRIPSI ---")
            krs_logic.tampilkanTreePrasyarat()

        elif pilihan == "2":
            krs_logic.tampilkanTreeSemesterMahasiswa(mahasiswa["nim"], "sekarang")

        elif pilihan == "3":
            krs_logic.tampilkanTreeSemesterMahasiswa(mahasiswa["nim"], "sebelumnya")

        elif pilihan == "4":
            krs_logic.tampilkanTreeSemesterMahasiswa(mahasiswa["nim"], "berikutnya")

        elif pilihan == "5":
            break

        else:
            print("Pilihan tidak valid.")


def ambilMataKuliah(mahasiswa, krs_logic):
    tampilkanDaftarKelas(mahasiswa, krs_logic)

    print("\nKetik 'batal' untuk kembali ke menu.")
    id_kelas = input("Masukkan ID kelas yang ingin diambil: ").upper()

    if id_kelas.lower() == "batal":
        return

    hasil = krs_logic.ambilMataKuliah(mahasiswa["nim"], id_kelas)
    print(hasil)


def batalkanMataKuliah(mahasiswa, krs_logic):
    tampilkanStatusKrs(mahasiswa, krs_logic)

    print("\nKetik 'batal' untuk kembali ke menu.")
    id_kelas = input("Masukkan ID kelas yang ingin dibatalkan: ").upper()

    if id_kelas.lower() == "batal":
        return

    hasil = krs_logic.batalkanMataKuliah(mahasiswa["nim"], id_kelas)
    print(hasil)


def tampilkanStatusKrs(mahasiswa, krs_logic):
    print("\n--- STATUS KRS SAYA ---")

    daftar_krs = krs_logic.getKrsMahasiswa(mahasiswa["nim"])

    if len(daftar_krs) == 0:
        print("Kamu belum mengambil kelas mata kuliah.")
        return

    print(
        f"{'No':<4} | "
        f"{'ID Kelas':<10} | "
        f"{'Kode MK':<8} | "
        f"{'Mata Kuliah':<38} | "
        f"{'SKS':<3} | "
        f"{'Dosen':<28} | "
        f"{'Hari':<8} | "
        f"{'Jam':<12} | "
        f"{'Ruang':<20} | "
        f"{'Status':<20}"
    )
    print("-" * 165)

    nomor = 1
    total_sks_aktif = 0

    for krs in daftar_krs:
        print(
            f"{nomor:<4} | "
            f"{krs['id_kelas']:<10} | "
            f"{krs['kode_matkul']:<8} | "
            f"{krs['nama']:<38} | "
            f"{krs['sks']:<3} | "
            f"{krs['nama_dosen']:<28} | "
            f"{krs['hari']:<8} | "
            f"{krs['jam']:<12} | "
            f"{krs['ruangan']:<20} | "
            f"{krs['status']:<20}"
        )

        if krs["status"] == "menunggu_validasi" or krs["status"] == "disetujui":
            total_sks_aktif += int(krs["sks"])

        nomor += 1

    jatah_sks = krs_logic.getJatahSks(mahasiswa)

    print("-" * 165)
    print(f"Total SKS aktif: {total_sks_aktif}/{jatah_sks}")


def tampilkanWaitingListMahasiswa(mahasiswa, krs_logic):
    print("\n--- WAITING LIST SAYA ---")

    daftar_waiting = krs_logic.getWaitingListMahasiswa(mahasiswa["nim"])

    if len(daftar_waiting) == 0:
        print("Kamu tidak sedang berada di waiting list.")
        return

    print(
        f"{'No':<4} | "
        f"{'ID Kelas':<10} | "
        f"{'Kode MK':<8} | "
        f"{'Mata Kuliah':<35} | "
        f"{'Dosen':<28} | "
        f"{'Kelas':<5} | "
        f"{'Hari':<8} | "
        f"{'Jam':<12} | "
        f"{'Ruangan':<22} | "
        f"{'Urutan':<8}"
    )
    print("-" * 175)

    nomor = 1

    for data in daftar_waiting:
        print(
            f"{nomor:<4} | "
            f"{data['id_kelas']:<10} | "
            f"{data['kode_matkul']:<8} | "
            f"{data['nama']:<35} | "
            f"{data['nama_dosen']:<28} | "
            f"{data['nama_kelas']:<5} | "
            f"{data['hari']:<8} | "
            f"{data['jam']:<12} | "
            f"{data['ruangan']:<22} | "
            f"{data['urutan']:<8}"
        )

        nomor += 1