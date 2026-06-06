# views/dosen_menu.py


def menuDosen(dosen, krs_logic):
    while True:
        print("\n=== MENU DOSEN ===")
        print("Nama:", dosen["nama"])
        print("NIP :", dosen["nip"])
        print("------------------")
        print("1. Lihat kelas yang saya ampu")
        print("2. Lihat & validasi pengajuan KRS")
        print("3. Lihat mahasiswa yang sudah disetujui")
        print("4. Lihat waiting list kelas")
        print("5. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            tampilkanKelasDosen(dosen, krs_logic)

        elif pilihan == "2":
            validasiPengajuanKrs(dosen, krs_logic)

        elif pilihan == "3":
            tampilkanMahasiswaDisetujui(dosen, krs_logic)

        elif pilihan == "4":
            tampilkanWaitingListDosen(dosen, krs_logic)

        elif pilihan == "5":
            print("Logout dosen berhasil.")
            break

        else:
            print("Pilihan tidak valid.")


def tampilkanKelasDosen(dosen, krs_logic):
    daftar_kelas = krs_logic.getDaftarKelasDosen(dosen["nip"])

    print("\n--- KELAS YANG SAYA AMPU ---")

    if len(daftar_kelas) == 0:
        print("Belum ada kelas yang diampu.")
        return

    print(
        f"{'No':<4} | "
        f"{'ID Kelas':<10} | "
        f"{'Kode MK':<8} | "
        f"{'Mata Kuliah':<40} | "
        f"{'Kelas':<5} | "
        f"{'Hari':<8} | "
        f"{'Jam':<12} | "
        f"{'Ruangan':<22} | "
        f"{'Peserta':<8} | "
        f"{'WL':<3}"
    )
    print("-" * 155)

    nomor = 1

    for kelas in daftar_kelas:
        print(
            f"{nomor:<4} | "
            f"{kelas['id_kelas']:<10} | "
            f"{kelas['kode_matkul']:<8} | "
            f"{kelas['nama']:<40} | "
            f"{kelas['nama_kelas']:<5} | "
            f"{kelas['hari']:<8} | "
            f"{kelas['jam']:<12} | "
            f"{kelas['ruangan']:<22} | "
            f"{kelas['peserta']:<8} | "
            f"{kelas['waiting']:<3}"
        )
        nomor += 1


def validasiPengajuanKrs(dosen, krs_logic):
    halaman_saat_ini = 1
    batas_per_halaman = 5

    while True:
        daftar_pengajuan = krs_logic.getDaftarValidasi(dosen["nip"])
        total_data = len(daftar_pengajuan)

        total_halaman = total_data // batas_per_halaman

        if total_data % batas_per_halaman > 0:
            total_halaman += 1

        if total_halaman == 0:
            total_halaman = 1

        if halaman_saat_ini > total_halaman:
            halaman_saat_ini = total_halaman

        if halaman_saat_ini < 1:
            halaman_saat_ini = 1

        index_awal = (halaman_saat_ini - 1) * batas_per_halaman
        index_akhir = index_awal + batas_per_halaman

        data_di_halaman_ini = daftar_pengajuan[index_awal:index_akhir]

        print(f"\n--- DAFTAR PENGAJUAN KRS HALAMAN {halaman_saat_ini}/{total_halaman} ---")
        print(
            f"{'No':<4} | "
            f"{'NIM':<12} | "
            f"{'Nama Mahasiswa':<30} | "
            f"{'ID Kelas':<10} | "
            f"{'Kode MK':<8} | "
            f"{'Mata Kuliah':<35} | "
            f"{'Kelas':<5} | "
            f"{'Status':<18}"
        )
        print("-" * 140)

        if len(data_di_halaman_ini) == 0:
            print("Tidak ada pengajuan KRS yang perlu divalidasi.")
        else:
            nomor_urut = index_awal + 1

            for data in data_di_halaman_ini:
                print(
                    f"{nomor_urut:<4} | "
                    f"{data['nim']:<12} | "
                    f"{data['nama_mahasiswa']:<30} | "
                    f"{data['id_kelas']:<10} | "
                    f"{data['kode_matkul']:<8} | "
                    f"{data['nama']:<35} | "
                    f"{data['nama_kelas']:<5} | "
                    f"{data['status']:<18}"
                )

                nomor_urut += 1

        print("-" * 140)
        print("\nOpsi:")
        print("- Ketik nomor urut untuk ACC/Tolak")
        print("- Ketik 'n' untuk halaman berikutnya")
        print("- Ketik 'p' untuk halaman sebelumnya")
        print("- Ketik 'q' untuk kembali")

        aksi = input("Masukkan opsi: ").lower()

        if aksi == "q":
            break

        elif aksi == "n":
            if halaman_saat_ini < total_halaman:
                halaman_saat_ini += 1
            else:
                print("Kamu sudah berada di halaman terakhir.")

        elif aksi == "p":
            if halaman_saat_ini > 1:
                halaman_saat_ini -= 1
            else:
                print("Kamu sudah berada di halaman pertama.")

        elif aksi.isdigit():
            index_pilihan = int(aksi) - 1

            if index_pilihan >= 0 and index_pilihan < total_data:
                data_terpilih = daftar_pengajuan[index_pilihan]

                nim_target = data_terpilih["nim"]
                id_kelas = data_terpilih["id_kelas"]

                print("\nData yang dipilih:")
                print("NIM        :", nim_target)
                print("Nama       :", data_terpilih["nama_mahasiswa"])
                print("ID Kelas   :", id_kelas)
                print("Kode MK    :", data_terpilih["kode_matkul"])
                print("Mata Kuliah:", data_terpilih["nama"])
                print("Kelas      :", data_terpilih["nama_kelas"])
                print("Status     :", data_terpilih["status"])

                keputusan = input("Ketik 'acc' untuk setujui atau 'tolak' untuk menolak: ").lower()

                if keputusan == "acc":
                    hasil = krs_logic.validasiKrs(dosen["nip"], nim_target, id_kelas, True)
                    print(hasil)

                elif keputusan == "tolak":
                    hasil = krs_logic.validasiKrs(dosen["nip"], nim_target, id_kelas, False)
                    print(hasil)

                else:
                    print("Input keputusan tidak valid.")

            else:
                print("Nomor urut tidak ditemukan.")

        else:
            print("Input tidak valid.")


def tampilkanMahasiswaDisetujui(dosen, krs_logic):
    print("\n--- MAHASISWA YANG SUDAH DISETUJUI ---")

    daftar_mahasiswa = krs_logic.getMahasiswaDisetujui(dosen["nip"])

    if len(daftar_mahasiswa) == 0:
        print("Belum ada mahasiswa yang disetujui.")
        return

    print(
        f"{'No':<4} | "
        f"{'NIM':<12} | "
        f"{'Nama Mahasiswa':<30} | "
        f"{'ID Kelas':<10} | "
        f"{'Kode MK':<8} | "
        f"{'Mata Kuliah':<35} | "
        f"{'Kelas':<5}"
    )
    print("-" * 125)

    nomor = 1

    for data in daftar_mahasiswa:
        print(
            f"{nomor:<4} | "
            f"{data['nim']:<12} | "
            f"{data['nama_mahasiswa']:<30} | "
            f"{data['id_kelas']:<10} | "
            f"{data['kode_matkul']:<8} | "
            f"{data['nama']:<35} | "
            f"{data['nama_kelas']:<5}"
        )
        nomor += 1


def tampilkanWaitingListDosen(dosen, krs_logic):
    print("\n--- WAITING LIST KELAS SAYA ---")

    daftar_waiting = krs_logic.getWaitingListDosen(dosen["nip"])

    if len(daftar_waiting) == 0:
        print("Tidak ada mahasiswa dalam waiting list untuk kelas yang kamu ampu.")
        return

    print(
        f"{'No':<4} | "
        f"{'ID Kelas':<10} | "
        f"{'Kode MK':<8} | "
        f"{'Mata Kuliah':<32} | "
        f"{'Kelas':<5} | "
        f"{'Hari':<8} | "
        f"{'Jam':<12} | "
        f"{'NIM':<12} | "
        f"{'Nama Mahasiswa':<30} | "
        f"{'Urutan':<8}"
    )
    print("-" * 155)

    nomor = 1

    for data in daftar_waiting:
        print(
            f"{nomor:<4} | "
            f"{data['id_kelas']:<10} | "
            f"{data['kode_matkul']:<8} | "
            f"{data['nama']:<32} | "
            f"{data['nama_kelas']:<5} | "
            f"{data['hari']:<8} | "
            f"{data['jam']:<12} | "
            f"{data['nim']:<12} | "
            f"{data['nama_mahasiswa']:<30} | "
            f"{data['urutan']:<8}"
        )

        nomor += 1
