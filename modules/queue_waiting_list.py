# modules/queue_waiting_list.py


class QueueManager:
    def __init__(self, csv_manager):
        self.csv = csv_manager

    def enqueue(self, id_kelas, nim):
        antrian = self.csv.loadQueue()

        for data in antrian:
            if data["id_kelas"] == id_kelas and data["nim"] == nim:
                return False

        data_baru = {
            "id_kelas": id_kelas,
            "nim": nim
        }

        antrian.append(data_baru)
        self.csv.saveQueue(antrian)

        return True

    def dequeue(self, id_kelas):
        antrian = self.csv.loadQueue()

        for index in range(len(antrian)):
            data = antrian[index]

            if data["id_kelas"] == id_kelas:
                nim_terdepan = data["nim"]

                antrian.pop(index)
                self.csv.saveQueue(antrian)

                return nim_terdepan

        return None

    def removeFromQueue(self, id_kelas, nim):
        antrian = self.csv.loadQueue()
        antrian_baru = []
        ditemukan = False

        for data in antrian:
            if data["id_kelas"] == id_kelas and data["nim"] == nim:
                ditemukan = True
                continue

            antrian_baru.append(data)

        self.csv.saveQueue(antrian_baru)

        return ditemukan

    def getQueueByKelas(self, id_kelas):
        antrian = self.csv.loadQueue()
        hasil = []
        urutan = 1

        for data in antrian:
            if data["id_kelas"] == id_kelas:
                kelas = self.csv.getKelas(id_kelas)

                kode_matkul = "-"
                nama_matkul = "-"
                nama_kelas = "-"
                hari = "-"
                jam = "-"
                ruangan = "-"
                nip_dosen = "-"
                nama_dosen = "-"

                if kelas is not None:
                    kode_matkul = kelas["kode_matkul"]
                    nama_kelas = kelas["nama_kelas"]
                    hari = kelas["hari"]
                    jam = kelas["jam"]
                    ruangan = kelas["ruangan"]
                    nip_dosen = kelas["nip_dosen"]

                    matkul = self.csv.getMataKuliah(kode_matkul)
                    dosen = self.csv.getDosen(nip_dosen)

                    if matkul is not None:
                        nama_matkul = matkul["nama"]

                    if dosen is not None:
                        nama_dosen = dosen["nama"]

                hasil.append({
                    "id_kelas": id_kelas,
                    "kode_matkul": kode_matkul,
                    "nama": nama_matkul,
                    "nama_kelas": nama_kelas,
                    "hari": hari,
                    "jam": jam,
                    "ruangan": ruangan,
                    "nip_dosen": nip_dosen,
                    "nama_dosen": nama_dosen,
                    "nim": data["nim"],
                    "urutan": str(urutan)
                })

                urutan += 1

        return hasil

    def getQueueByMahasiswa(self, nim):
        antrian = self.csv.loadQueue()
        hasil = []

        for data in antrian:
            if data["nim"] == nim:
                id_kelas = data["id_kelas"]
                kelas = self.csv.getKelas(id_kelas)

                kode_matkul = "-"
                nama_matkul = "-"
                nama_kelas = "-"
                hari = "-"
                jam = "-"
                ruangan = "-"
                nip_dosen = "-"
                nama_dosen = "-"

                if kelas is not None:
                    kode_matkul = kelas["kode_matkul"]
                    nama_kelas = kelas["nama_kelas"]
                    hari = kelas["hari"]
                    jam = kelas["jam"]
                    ruangan = kelas["ruangan"]
                    nip_dosen = kelas["nip_dosen"]

                    matkul = self.csv.getMataKuliah(kode_matkul)
                    dosen = self.csv.getDosen(nip_dosen)

                    if matkul is not None:
                        nama_matkul = matkul["nama"]

                    if dosen is not None:
                        nama_dosen = dosen["nama"]

                urutan = self.getUrutanMahasiswa(id_kelas, nim)

                hasil.append({
                    "id_kelas": id_kelas,
                    "kode_matkul": kode_matkul,
                    "nama": nama_matkul,
                    "nama_kelas": nama_kelas,
                    "hari": hari,
                    "jam": jam,
                    "ruangan": ruangan,
                    "nip_dosen": nip_dosen,
                    "nama_dosen": nama_dosen,
                    "nim": nim,
                    "urutan": str(urutan)
                })

        return hasil

    def getUrutanMahasiswa(self, id_kelas, nim):
        antrian = self.csv.loadQueue()
        urutan = 1

        for data in antrian:
            if data["id_kelas"] == id_kelas:
                if data["nim"] == nim:
                    return urutan

                urutan += 1

        return "-"

    def getJumlahWaitingListKelas(self, id_kelas):
        antrian = self.csv.loadQueue()
        jumlah = 0

        for data in antrian:
            if data["id_kelas"] == id_kelas:
                jumlah += 1

        return jumlah

    def tampilkanQueueKelas(self, id_kelas):
        daftar_antrian = self.getQueueByKelas(id_kelas)

        if len(daftar_antrian) == 0:
            print("Waiting list kelas ini kosong.")
            return

        print(f"\n=== WAITING LIST KELAS {id_kelas} ===")
        print(
            f"{'Urutan':<8} | "
            f"{'NIM':<12} | "
            f"{'Mata Kuliah':<38} | "
            f"{'Dosen':<28} | "
            f"{'Hari':<8} | "
            f"{'Jam':<12} | "
            f"{'Ruang':<22}"
        )
        print("-" * 135)

        for data in daftar_antrian:
            print(
                f"{data['urutan']:<8} | "
                f"{data['nim']:<12} | "
                f"{data['nama']:<38} | "
                f"{data['nama_dosen']:<28} | "
                f"{data['hari']:<8} | "
                f"{data['jam']:<12} | "
                f"{data['ruangan']:<22}"
            )