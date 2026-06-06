# views/dosen_menu.py


def menuDosen(dosen, krs_logic):
    while True:
        print("\n=== MENU DOSEN ===")
        print("Nama:", dosen["nama"])
        print("NIP :", dosen["nip"])
        print("------------------")
        print("1. Lihat & validasi pengajuan KRS")
        print("2. Lihat mahasiswa yang sudah disetujui")
        print("3. Lihat waiting list mata kuliah")
        print("4. Input nilai IP Mahasiswa Wali")
        print("5. Logout")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            validasiPengajuanKrs(dosen, krs_logic)

        elif pilihan == "2":
            tampilkanMahasiswaDisetujui(dosen, krs_logic)

        elif pilihan == "3":
            tampilkanWaitingListDosen(dosen, krs_logic)

        elif pilihan == "4":
            print("\n--- DAFTAR MAHASISWA ---")
            semua_mahasiswa = krs_logic.csv.bacaCsv("data/mahasiswa.csv")
            
            if len(semua_mahasiswa) == 0:
                print("Belum ada data mahasiswa di sistem.")
            else:
                print(f"{'No':<4} | {'NIM':<10} | {'Nama Mahasiswa':<30} | {'Semester':<8} | {'IP Terakhir':<11} | {'NIP Wali':<10}")
                print("-" * 85)
                
                nomor = 1
                for mhs in semua_mahasiswa:
                    nim_mhs = mhs.get("nim", "-")
                    nama_mhs = mhs.get("nama", "-")
                    smt_mhs = mhs.get("semester", "-")
                    ip_mhs = mhs.get("ip_terakhir", "-")
                    wali_mhs = mhs.get("nip_dosen_wali", "-")

                    status_wali = wali_mhs
                    if wali_mhs == dosen["nip"]:
                        status_wali = f"{wali_mhs} (Mhs Kamu)"
                        
                    print(f"{nomor:<4} | {nim_mhs:<10} | {nama_mhs:<30} | {smt_mhs:<8} | {ip_mhs:<11} | {status_wali}")
                    nomor += 1
                print("-" * 85)

            print("\n*Ketik 'batal' pada kolom NIM untuk kembali ke menu")
            nim_input = input("Masukkan NIM Mahasiswa Perwalian: ")
            
            if nim_input.lower() == 'batal':
                continue
                
            ip_input = input("Masukkan Nilai IP (Format angka, misal: 3.80): ")

            try:
                ip_float = float(ip_input)
                hasil = krs_logic.inputNilaiIp(dosen["nip"], nim_input, ip_float)
                print(hasil)
            except ValueError:
                print("❌ Gagal: Format IP salah! Pastikan kamu menggunakan angka dan titik (bukan koma).")

        elif pilihan == "5":
            print("Logout dosen berhasil.")
            break

        elif pilihan == "5":
            print("Logout dosen berhasil.")
            break

        else:
            print("Pilihan tidak valid.")


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
        print(f"{'No':<4} | {'NIM':<12} | {'Kode MK':<10} | {'Nama Mata Kuliah':<35} | {'Status':<20}")
        print("-" * 95)

        if len(data_di_halaman_ini) == 0:
            print("Tidak ada pengajuan KRS yang perlu divalidasi.")
        else:
            nomor_urut = index_awal + 1

            for data in data_di_halaman_ini:
                nim = data["nim"]
                kode_matkul = data["kode_matkul"]
                nama_matkul = data.get("nama", "-")
                status = data["status"]

                print(f"{nomor_urut:<4} | {nim:<12} | {kode_matkul:<10} | {nama_matkul:<35} | {status:<20}")
                nomor_urut += 1

        print("-" * 95)
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
                kode_matkul = data_terpilih["kode_matkul"]

                print("\nData yang dipilih:")
                print("NIM      :", nim_target)
                print("Kode MK  :", kode_matkul)
                print("Status   :", data_terpilih["status"])

                keputusan = input("Ketik 'acc' untuk setujui atau 'tolak' untuk menolak: ").lower()

                if keputusan == "acc":
                    hasil = krs_logic.validasiKrs(dosen["nip"], nim_target, kode_matkul, True)
                    print(hasil)

                elif keputusan == "tolak":
                    hasil = krs_logic.validasiKrs(dosen["nip"], nim_target, kode_matkul, False)
                    print(hasil)

                else:
                    print("Input keputusan tidak valid.")

            else:
                print("Nomor urut tidak ditemukan.")

        else:
            print("Input tidak valid.")


def tampilkanMahasiswaDisetujui(dosen, krs_logic):
    print("\n--- MAHASISWA YANG SUDAH DISETUJUI ---")

    try:
        daftar_mahasiswa = krs_logic.getMahasiswaDisetujui(dosen["nip"])
    except AttributeError:
        print("Fitur mahasiswa disetujui belum tersedia di krs_manager.")
        return

    if len(daftar_mahasiswa) == 0:
        print("Belum ada mahasiswa yang disetujui.")
        return

    print(f"{'No':<4} | {'NIM':<12} | {'Nama Mahasiswa':<35} | {'Kode MK':<10} | {'Nama Mata Kuliah':<35}")
    print("-" * 110)

    nomor = 1
    for data in daftar_mahasiswa:
        nim = data["nim"]
        nama_mahasiswa = data.get("nama_mahasiswa", "-")
        kode_matkul = data["kode_matkul"]
        nama_matkul = data.get("nama", "-")

        print(f"{nomor:<4} | {nim:<12} | {nama_mahasiswa:<35} | {kode_matkul:<10} | {nama_matkul:<35}")
        nomor += 1


def tampilkanWaitingListDosen(dosen, krs_logic):
    print("\n--- WAITING LIST MATA KULIAH DOSEN ---")

    try:
        daftar_waiting = krs_logic.getWaitingListDosen(dosen["nip"])
    except AttributeError:
        print("Fitur waiting list dosen belum tersedia di krs_manager.")
        return

    if len(daftar_waiting) == 0:
        print("Tidak ada mahasiswa dalam waiting list untuk mata kuliah yang kamu ampu.")
        return

    print(f"{'No':<4} | {'Kode MK':<10} | {'Nama Mata Kuliah':<35} | {'NIM':<12} | {'Nama Mahasiswa':<35} | {'Urutan':<8}")
    print("-" * 120)

    nomor = 1
    for data in daftar_waiting:
        kode_matkul = data["kode_matkul"]
        nama_matkul = data.get("nama", "-")
        nim = data["nim"]
        nama_mahasiswa = data.get("nama_mahasiswa", "-")
        urutan = data.get("urutan", "-")

        print(f"{nomor:<4} | {kode_matkul:<10} | {nama_matkul:<35} | {nim:<12} | {nama_mahasiswa:<35} | {urutan:<8}")
        nomor += 1