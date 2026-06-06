# modules/csv_manager.py

import os


class CsvManager:
    def __init__(self):
        self.folder_data = "data"
        self.pastikanFolderDataAda()

    def pastikanFolderDataAda(self):
        if not os.path.exists(self.folder_data):
            os.makedirs(self.folder_data)

    def bacaCsv(self, file_path):
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            isi_file = file.read().strip()

        if isi_file == "":
            return []

        baris_teks = isi_file.split("\n")

        if len(baris_teks) <= 1:
            return []

        header = baris_teks[0].split(",")
        hasil = []

        for i in range(1, len(baris_teks)):
            isi_baris = baris_teks[i].split(",")

            if len(isi_baris) == len(header):
                data_baris = {}

                for j in range(len(header)):
                    data_baris[header[j]] = isi_baris[j]

                hasil.append(data_baris)

        return hasil

    def tulisCsv(self, file_path, header, data):
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(",".join(header) + "\n")

            for baris in data:
                nilai_per_kolom = []

                for kolom in header:
                    nilai = str(baris.get(kolom, ""))
                    nilai_per_kolom.append(nilai)

                file.write(",".join(nilai_per_kolom) + "\n")

    # =========================
    # ADMIN
    # =========================

    def getAdmin(self, id_admin):
        semua_admin = self.bacaCsv("data/admin.csv")

        for admin in semua_admin:
            if admin["id_admin"] == id_admin:
                return admin

        return None

    # =========================
    # MAHASISWA
    # =========================

    def getMahasiswa(self, nim):
        semua_mahasiswa = self.bacaCsv("data/mahasiswa.csv")

        for mahasiswa in semua_mahasiswa:
            if mahasiswa["nim"] == nim:
                return mahasiswa

        return None

    def getSemuaMahasiswa(self):
        return self.bacaCsv("data/mahasiswa.csv")

    def tambahMahasiswa(self, data_mahasiswa):
        semua_mahasiswa = self.bacaCsv("data/mahasiswa.csv")
        semua_mahasiswa.append(data_mahasiswa)

        header = [
            "nim",
            "nama",
            "password",
            "nip_dosen_wali",
            "matkul_lulus",
            "semester",
            "ip_terakhir"
        ]

        self.tulisCsv("data/mahasiswa.csv", header, semua_mahasiswa)

    def hapusMahasiswa(self, nim):
        semua_mahasiswa = self.bacaCsv("data/mahasiswa.csv")
        data_baru = []
        ditemukan = False

        for mahasiswa in semua_mahasiswa:
            if mahasiswa["nim"] == nim:
                ditemukan = True
            else:
                data_baru.append(mahasiswa)

        header = [
            "nim",
            "nama",
            "password",
            "nip_dosen_wali",
            "matkul_lulus",
            "semester",
            "ip_terakhir"
        ]

        self.tulisCsv("data/mahasiswa.csv", header, data_baru)

        return ditemukan


    # =========================
    # DOSEN
    # =========================

    def getDosen(self, nip):
        semua_dosen = self.bacaCsv("data/dosen.csv")

        for dosen in semua_dosen:
            if dosen["nip"] == nip:
                return dosen

        return None

    def getSemuaDosen(self):
        return self.bacaCsv("data/dosen.csv")

    def getDosenByKelas(self, id_kelas):
        kelas = self.getKelas(id_kelas)

        if kelas is not None:
            dosen = self.getDosen(kelas["nip_dosen"])

            if dosen is not None:
                return dosen

        semua_dosen = self.getSemuaDosen()

        for dosen in semua_dosen:
            daftar_kelas = dosen["dosen_mk"].split(";")

            if id_kelas in daftar_kelas:
                return dosen

        return None

    def tambahDosen(self, data_dosen):
        semua_dosen = self.bacaCsv("data/dosen.csv")
        semua_dosen.append(data_dosen)

        header = ["nip", "nama", "password", "dosen_mk"]
        self.tulisCsv("data/dosen.csv", header, semua_dosen)

    def hapusDosen(self, nip):
        semua_dosen = self.bacaCsv("data/dosen.csv")
        data_baru = []
        ditemukan = False

        for dosen in semua_dosen:
            if dosen["nip"] == nip:
                ditemukan = True
            else:
                data_baru.append(dosen)

        header = ["nip", "nama", "password", "dosen_mk"]
        self.tulisCsv("data/dosen.csv", header, data_baru)

        return ditemukan

    # =========================
    # MATA KULIAH
    # =========================

    def getSemuaMataKuliah(self):
        return self.bacaCsv("data/mata_kuliah.csv")

    def getMataKuliah(self, kode_matkul):
        semua_matkul = self.bacaCsv("data/mata_kuliah.csv")

        for matkul in semua_matkul:
            if matkul["kode"] == kode_matkul:
                return matkul

        return None

    def getMataKuliahBySemester(self, semester):
        semua_matkul = self.bacaCsv("data/mata_kuliah.csv")
        hasil = []

        for matkul in semua_matkul:
            if matkul["semester"] == str(semester):
                hasil.append(matkul)

        return hasil

    # =========================
    # KELAS
    # =========================

    def getSemuaKelas(self):
        return self.bacaCsv("data/kelas.csv")

    def getKelas(self, id_kelas):
        semua_kelas = self.bacaCsv("data/kelas.csv")

        for kelas in semua_kelas:
            if kelas["id_kelas"] == id_kelas:
                return kelas

        return None

    def getKelasByMatkul(self, kode_matkul):
        semua_kelas = self.bacaCsv("data/kelas.csv")
        hasil = []

        for kelas in semua_kelas:
            if kelas["kode_matkul"] == kode_matkul:
                hasil.append(kelas)

        return hasil

    def getKelasBySemester(self, semester):
        semua_kelas = self.bacaCsv("data/kelas.csv")
        hasil = []

        for kelas in semua_kelas:
            matkul = self.getMataKuliah(kelas["kode_matkul"])

            if matkul is not None and matkul["semester"] == str(semester):
                hasil.append(kelas)

        return hasil

    def getKelasDosen(self, nip):
        semua_kelas = self.bacaCsv("data/kelas.csv")
        hasil = []

        for kelas in semua_kelas:
            if kelas["nip_dosen"] == nip:
                hasil.append(kelas)

        if len(hasil) > 0:
            return hasil

        dosen = self.getDosen(nip)

        if dosen is None:
            return []

        if dosen["dosen_mk"] == "-":
            return []

        daftar_id_kelas = dosen["dosen_mk"].split(";")

        for id_kelas in daftar_id_kelas:
            kelas = self.getKelas(id_kelas)

            if kelas is not None:
                hasil.append(kelas)

        return hasil

    # =========================
    # KRS
    # =========================

    def getSemuaKrs(self):
        return self.bacaCsv("data/krs.csv")

    def getKrsByMahasiswa(self, nim):
        semua_krs = self.bacaCsv("data/krs.csv")
        hasil = []

        for krs in semua_krs:
            if krs["nim"] == nim:
                hasil.append(krs)

        return hasil

    def getKrsByKelas(self, id_kelas):
        semua_krs = self.bacaCsv("data/krs.csv")
        hasil = []

        for krs in semua_krs:
            if krs["id_kelas"] == id_kelas:
                hasil.append(krs)

        return hasil

    def getKrsByMatkul(self, kode_matkul):
        semua_krs = self.bacaCsv("data/krs.csv")
        hasil = []

        for krs in semua_krs:
            if krs["kode_matkul"] == kode_matkul:
                hasil.append(krs)

        return hasil

    def getStatusKrsByKelas(self, nim, id_kelas):
        semua_krs = self.bacaCsv("data/krs.csv")

        for krs in semua_krs:
            if krs["nim"] == nim and krs["id_kelas"] == id_kelas:
                return krs

        return None

    def getStatusKrsByMatkul(self, nim, kode_matkul):
        semua_krs = self.bacaCsv("data/krs.csv")

        for krs in semua_krs:
            if krs["nim"] == nim and krs["kode_matkul"] == kode_matkul:
                return krs

        return None

    def tambahKrs(self, nim, id_kelas, kode_matkul, status):
        semua_krs = self.bacaCsv("data/krs.csv")

        data_baru = {
            "nim": nim,
            "id_kelas": id_kelas,
            "kode_matkul": kode_matkul,
            "status": status
        }

        semua_krs.append(data_baru)

        header = ["nim", "id_kelas", "kode_matkul", "status"]
        self.tulisCsv("data/krs.csv", header, semua_krs)

    def updateStatusKrs(self, nim, id_kelas, status_baru):
        semua_krs = self.bacaCsv("data/krs.csv")
        ditemukan = False

        for krs in semua_krs:
            if krs["nim"] == nim and krs["id_kelas"] == id_kelas:
                krs["status"] = status_baru
                ditemukan = True

        header = ["nim", "id_kelas", "kode_matkul", "status"]
        self.tulisCsv("data/krs.csv", header, semua_krs)

        return ditemukan

    def hapusKrs(self, nim, id_kelas):
        semua_krs = self.bacaCsv("data/krs.csv")
        data_baru = []
        ditemukan = False

        for krs in semua_krs:
            if krs["nim"] == nim and krs["id_kelas"] == id_kelas:
                ditemukan = True
                continue

            data_baru.append(krs)

        header = ["nim", "id_kelas", "kode_matkul", "status"]
        self.tulisCsv("data/krs.csv", header, data_baru)

        return ditemukan

    def getJumlahPesertaKelas(self, id_kelas):
        semua_krs = self.bacaCsv("data/krs.csv")
        jumlah = 0

        for krs in semua_krs:
            if krs["id_kelas"] == id_kelas:
                if krs["status"] == "menunggu_validasi" or krs["status"] == "disetujui":
                    jumlah += 1

        return jumlah

    # =========================
    # WAITING LIST
    # =========================

    def loadQueue(self):
        return self.bacaCsv("data/waiting_list.csv")

    def saveQueue(self, data_queue):
        header = ["id_kelas", "nim"]
        self.tulisCsv("data/waiting_list.csv", header, data_queue)

    def getWaitingListByKelas(self, id_kelas):
        semua_waiting = self.bacaCsv("data/waiting_list.csv")
        hasil = []

        for waiting in semua_waiting:
            if waiting["id_kelas"] == id_kelas:
                hasil.append(waiting)

        return hasil

    def getWaitingListByMahasiswa(self, nim):
        semua_waiting = self.bacaCsv("data/waiting_list.csv")
        hasil = []

        for waiting in semua_waiting:
            if waiting["nim"] == nim:
                hasil.append(waiting)

        return hasil