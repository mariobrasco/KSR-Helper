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

    def getAdmin(self, id_admin):
        semua_data = self.bacaCsv("data/admin.csv")

        for admin in semua_data:
            if admin["id_admin"] == id_admin:
                return admin

        return None

    def getMahasiswa(self, nim):
        semua_data = self.bacaCsv("data/mahasiswa.csv")

        for mahasiswa in semua_data:
            if mahasiswa["nim"] == nim:
                return mahasiswa

        return None

    def getDosen(self, nip):
        semua_data = self.bacaCsv("data/dosen.csv")

        for dosen in semua_data:
            if dosen["nip"] == nip:
                return dosen

        return None

    def getSemuaMahasiswa(self):
        return self.bacaCsv("data/mahasiswa.csv")

    def getSemuaDosen(self):
        return self.bacaCsv("data/dosen.csv")

    def getSemuaMataKuliah(self):
        return self.bacaCsv("data/mata_kuliah.csv")

    def getMataKuliah(self, kode_matkul):
        semua_data = self.bacaCsv("data/mata_kuliah.csv")

        for matkul in semua_data:
            if matkul["kode"] == kode_matkul:
                return matkul

        return None

    def getSemuaKrs(self):
        return self.bacaCsv("data/krs.csv")

    def getKrsByMatkul(self, kode_matkul):
        semua_krs = self.bacaCsv("data/krs.csv")
        hasil = []

        for krs in semua_krs:
            if krs["kode_matkul"] == kode_matkul:
                hasil.append(krs)

        return hasil

    def getKrsByMahasiswa(self, nim):
        semua_krs = self.bacaCsv("data/krs.csv")
        hasil = []

        for krs in semua_krs:
            if krs["nim"] == nim:
                hasil.append(krs)

        return hasil

    def getStatusKrs(self, nim, kode_matkul):
        semua_krs = self.bacaCsv("data/krs.csv")

        for krs in semua_krs:
            if krs["nim"] == nim and krs["kode_matkul"] == kode_matkul:
                return krs

        return None

    def tambahKrs(self, nim, kode_matkul, status):
        semua_krs = self.bacaCsv("data/krs.csv")

        data_baru = {
            "nim": nim,
            "kode_matkul": kode_matkul,
            "status": status
        }

        semua_krs.append(data_baru)

        header = ["nim", "kode_matkul", "status"]
        self.tulisCsv("data/krs.csv", header, semua_krs)

    def updateStatusKrs(self, nim, kode_matkul, status_baru):
        semua_krs = self.bacaCsv("data/krs.csv")

        for krs in semua_krs:
            if krs["nim"] == nim and krs["kode_matkul"] == kode_matkul:
                krs["status"] = status_baru

        header = ["nim", "kode_matkul", "status"]
        self.tulisCsv("data/krs.csv", header, semua_krs)

    def hapusKrs(self, nim, kode_matkul):
        semua_krs = self.bacaCsv("data/krs.csv")
        data_baru = []

        for krs in semua_krs:
            if krs["nim"] == nim and krs["kode_matkul"] == kode_matkul:
                continue

            data_baru.append(krs)

        header = ["nim", "kode_matkul", "status"]
        self.tulisCsv("data/krs.csv", header, data_baru)

    def loadQueue(self):
        return self.bacaCsv("data/waiting_list.csv")

    def saveQueue(self, data_queue):
        header = ["kode_matkul", "nim"]
        self.tulisCsv("data/waiting_list.csv", header, data_queue)

    def tambahMahasiswa(self, data_mahasiswa):
        semua_mahasiswa = self.bacaCsv("data/mahasiswa.csv")
        semua_mahasiswa.append(data_mahasiswa)
        # Update header dengan semester dan ip_terakhir
        header = ["nim", "nama", "password", "nip_dosen_wali", "matkul_lulus", "semester", "ip_terakhir"]
        self.tulisCsv("data/mahasiswa.csv", header, semua_mahasiswa)

    def tambahDosen(self, data_dosen):
        semua_dosen = self.bacaCsv("data/dosen.csv")
        semua_dosen.append(data_dosen)

        header = ["nip", "nama", "password", "dosen_mk"]
        self.tulisCsv("data/dosen.csv", header, semua_dosen)

    def hapusMahasiswa(self, nim):
        semua_mahasiswa = self.bacaCsv("data/mahasiswa.csv")
        data_baru = []
        ditemukan = False

        for mahasiswa in semua_mahasiswa:
            if mahasiswa["nim"] == nim:
                ditemukan = True
            else:
                data_baru.append(mahasiswa)

        header = ["nim", "nama", "password", "nip_dosen_wali", "matkul_lulus", "semester", "ip_terakhir"]
        self.tulisCsv("data/mahasiswa.csv", header, data_baru)
        return ditemukan
    
    def updateIpMahasiswa(self, nim, ip_baru):
        semua_mahasiswa = self.bacaCsv("data/mahasiswa.csv")
        for mahasiswa in semua_mahasiswa:
            if mahasiswa["nim"] == nim:
                mahasiswa["ip_terakhir"] = str(ip_baru)
        
        header = ["nim", "nama", "password", "nip_dosen_wali", "matkul_lulus", "semester", "ip_terakhir"]
        self.tulisCsv("data/mahasiswa.csv", header, semua_mahasiswa)

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