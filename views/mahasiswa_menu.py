# views/mahasiswa_menu.py


def menuMahasiswa(mahasiswa, krs_logic):
    while True:
        print("\n=== MENU MAHASISWA ===")
        print("Nama:", mahasiswa["nama"])
        print("NIM :", mahasiswa["nim"])
        print(f"Semester : {mahasiswa['semester']}")
        print(f"IP       : {mahasiswa['ip_terakhir']}")
        print("----------------------")
        print("1. Lihat daftar mata kuliah")
        print("2. Lihat tree prasyarat")
        print("3. Ambil mata kuliah")
        print("4. Batalkan mata kuliah")
        print("5. Lihat status KRS saya")
        print("6. Lihat waiting list saya")
        print("7. Lihat hasil KRS (Cetak Jadwal)")
        print("8. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkanDaftarMataKuliah(krs_logic)

        elif pilihan == "2":
            tampilkanTreePrasyarat(krs_logic)

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


def tampilkanDaftarMataKuliah(krs_logic):
    daftar_matkul = krs_logic.getDaftarMataKuliah()

    print("\n--- DAFTAR MATA KULIAH ---")
    print(f"{'Kode':<8} | {'Nama Mata Kuliah':<40} | {'Kuota':<5} | {'Prasyarat':<20}")
    print("-" * 85)

    if len(daftar_matkul) == 0:
        print("Belum ada data mata kuliah.")
        return

    for matkul in daftar_matkul:
        kode_matkul = matkul["kode"]
        nama_matkul = matkul["nama"]
        kuota = matkul["kuota"]
        prasyarat = matkul["prasyarat"]

        print(f"{kode_matkul:<8} | {nama_matkul:<40} | {kuota:<5} | {prasyarat:<20}")


def tampilkanTreePrasyarat(krs_logic):
    print("\n--- TREE PRASYARAT MATA KULIAH ---")

    try:
        krs_logic.tampilkanTreePrasyarat()
    except AttributeError:
        print("Fitur tree prasyarat belum tersedia di krs_manager.")


def ambilMataKuliah(mahasiswa, krs_logic):
    tampilkanDaftarMataKuliah(krs_logic)

    print("\nKetik 'batal' untuk kembali ke menu.")
    kode_matkul = input("Masukkan kode mata kuliah yang ingin diambil: ").upper()

    if kode_matkul.lower() == "batal":
        return

    hasil = krs_logic.ambilMataKuliah(mahasiswa["nim"], kode_matkul)
    print(hasil)


def batalkanMataKuliah(mahasiswa, krs_logic):
    tampilkanStatusKrs(mahasiswa, krs_logic)

    print("\nKetik 'batal' untuk kembali ke menu.")
    kode_matkul = input("Masukkan kode mata kuliah yang ingin dibatalkan: ").upper()

    if kode_matkul.lower() == "batal":
        return

    hasil = krs_logic.batalkanMataKuliah(mahasiswa["nim"], kode_matkul)
    print(hasil)


def tampilkanStatusKrs(mahasiswa, krs_logic):
    print("\n--- STATUS KRS SAYA ---")

    try:
        daftar_krs = krs_logic.getKrsMahasiswa(mahasiswa["nim"])
    except AttributeError:
        print("Fitur status KRS belum tersedia di krs_manager.")
        return

    if len(daftar_krs) == 0:
        print("Kamu belum mengambil mata kuliah.")
        return

    print(f"{'No':<4} | {'Kode MK':<10} | {'Nama Mata Kuliah':<40} | {'Status':<20}")
    print("-" * 85)

    nomor = 1
    for krs in daftar_krs:
        kode_matkul = krs["kode_matkul"]
        nama_matkul = krs.get("nama", "-")
        status = krs["status"]

        print(f"{nomor:<4} | {kode_matkul:<10} | {nama_matkul:<40} | {status:<20}")
        nomor += 1


def tampilkanWaitingListMahasiswa(mahasiswa, krs_logic):
    print("\n--- WAITING LIST SAYA ---")

    try:
        daftar_waiting = krs_logic.getWaitingListMahasiswa(mahasiswa["nim"])
    except AttributeError:
        print("Fitur waiting list mahasiswa belum tersedia di krs_manager.")
        return

    if len(daftar_waiting) == 0:
        print("Kamu tidak sedang berada di waiting list.")
        return

    print(f"{'No':<4} | {'Kode MK':<10} | {'Nama Mata Kuliah':<40} | {'Urutan':<8}")
    print("-" * 75)

    nomor = 1
    for data in daftar_waiting:
        kode_matkul = data["kode_matkul"]
        nama_matkul = data.get("nama", "-")
        urutan = data.get("urutan", "-")

        print(f"{nomor:<4} | {kode_matkul:<10} | {nama_matkul:<40} | {urutan:<8}")
        nomor += 1