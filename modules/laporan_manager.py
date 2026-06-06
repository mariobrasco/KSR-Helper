# modules/laporan_manager.py


class LaporanManager:
    def __init__(self, csv_manager):
        self.csv = csv_manager

    def tampilkanSemuaKrs(self):
        semua_krs = self.csv.getSemuaKrs()

        print("\n=== LAPORAN SEMUA KRS ===")

        if len(semua_krs) == 0:
            print("Belum ada data KRS.")
            return

        print(
            f"{'No':<4} | "
            f"{'NIM':<12} | "
            f"{'ID Kelas':<10} | "
            f"{'Kode MK':<8} | "
            f"{'Mata Kuliah':<35} | "
            f"{'Dosen':<28} | "
            f"{'Hari':<8} | "
            f"{'Jam':<12} | "
            f"{'Status':<18}"
        )
        print("-" * 155)

        nomor = 1

        for krs in semua_krs:
            kelas = self.csv.getKelas(krs["id_kelas"])
            matkul = self.csv.getMataKuliah(krs["kode_matkul"])

            nama_matkul = "-"
            nama_dosen = "-"
            hari = "-"
            jam = "-"

            if matkul is not None:
                nama_matkul = matkul["nama"]

            if kelas is not None:
                hari = kelas["hari"]
                jam = kelas["jam"]

                dosen = self.csv.getDosen(kelas["nip_dosen"])

                if dosen is not None:
                    nama_dosen = dosen["nama"]

            print(
                f"{nomor:<4} | "
                f"{krs['nim']:<12} | "
                f"{krs['id_kelas']:<10} | "
                f"{krs['kode_matkul']:<8} | "
                f"{nama_matkul:<35} | "
                f"{nama_dosen:<28} | "
                f"{hari:<8} | "
                f"{jam:<12} | "
                f"{krs['status']:<18}"
            )

            nomor += 1

    def tampilkanSemuaWaitingList(self):
        semua_waiting = self.csv.loadQueue()

        print("\n=== LAPORAN SEMUA WAITING LIST ===")

        if len(semua_waiting) == 0:
            print("Belum ada data waiting list.")
            return

        print(
            f"{'No':<4} | "
            f"{'ID Kelas':<10} | "
            f"{'Kode MK':<8} | "
            f"{'Mata Kuliah':<35} | "
            f"{'Dosen':<28} | "
            f"{'NIM':<12} | "
            f"{'Hari':<8} | "
            f"{'Jam':<12}"
        )
        print("-" * 145)

        nomor = 1

        for waiting in semua_waiting:
            kelas = self.csv.getKelas(waiting["id_kelas"])

            kode_matkul = "-"
            nama_matkul = "-"
            nama_dosen = "-"
            hari = "-"
            jam = "-"

            if kelas is not None:
                kode_matkul = kelas["kode_matkul"]
                hari = kelas["hari"]
                jam = kelas["jam"]

                matkul = self.csv.getMataKuliah(kode_matkul)
                dosen = self.csv.getDosen(kelas["nip_dosen"])

                if matkul is not None:
                    nama_matkul = matkul["nama"]

                if dosen is not None:
                    nama_dosen = dosen["nama"]

            print(
                f"{nomor:<4} | "
                f"{waiting['id_kelas']:<10} | "
                f"{kode_matkul:<8} | "
                f"{nama_matkul:<35} | "
                f"{nama_dosen:<28} | "
                f"{waiting['nim']:<12} | "
                f"{hari:<8} | "
                f"{jam:<12}"
            )

            nomor += 1

    def tampilkanLaporanKuotaKelas(self):
        semua_kelas = self.csv.getSemuaKelas()

        print("\n=== LAPORAN KUOTA KELAS ===")

        if len(semua_kelas) == 0:
            print("Belum ada data kelas.")
            return

        print(
            f"{'No':<4} | "
            f"{'ID Kelas':<10} | "
            f"{'Kode MK':<8} | "
            f"{'Mata Kuliah':<35} | "
            f"{'Dosen':<28} | "
            f"{'Hari':<8} | "
            f"{'Jam':<12} | "
            f"{'Peserta':<8} | "
            f"{'WL':<3}"
        )
        print("-" * 155)

        nomor = 1

        for kelas in semua_kelas:
            matkul = self.csv.getMataKuliah(kelas["kode_matkul"])
            dosen = self.csv.getDosen(kelas["nip_dosen"])

            nama_matkul = "-"
            nama_dosen = "-"

            if matkul is not None:
                nama_matkul = matkul["nama"]

            if dosen is not None:
                nama_dosen = dosen["nama"]

            peserta_terisi = self.csv.getJumlahPesertaKelas(kelas["id_kelas"])
            kuota = kelas["kuota"]
            waiting = len(self.csv.getWaitingListByKelas(kelas["id_kelas"]))

            print(
                f"{nomor:<4} | "
                f"{kelas['id_kelas']:<10} | "
                f"{kelas['kode_matkul']:<8} | "
                f"{nama_matkul:<35} | "
                f"{nama_dosen:<28} | "
                f"{kelas['hari']:<8} | "
                f"{kelas['jam']:<12} | "
                f"{str(peserta_terisi) + '/' + kuota:<8} | "
                f"{waiting:<3}"
            )

            nomor += 1