# modules/krs_manager.py


class KRSManager:
    def __init__(self, csv_manager, tree_prasyarat, queue_manager):
        self.csv = csv_manager
        self.tree = tree_prasyarat
        self.queue = queue_manager

    def getDaftarMataKuliah(self):
        return self.csv.getSemuaMataKuliah()

    def tampilkanTreePrasyarat(self):
        self.tree.tampilkanTree("KA591")

    def ambilMataKuliah(self, nim, kode_matkul):
        mahasiswa = self.csv.getMahasiswa(nim)
        matkul = self.csv.getMataKuliah(kode_matkul)

        if mahasiswa is None: return "❌ Data mahasiswa tidak ditemukan."
        if matkul is None: return "❌ Mata kuliah tidak ditemukan."

        status_krs = self.csv.getStatusKrs(nim, kode_matkul)
        if status_krs is not None:
            return "⚠️ Kamu sudah mengambil atau mengajukan mata kuliah ini."

        prasyarat = self.tree.getPrasyarat(kode_matkul)
        matkul_lulus = mahasiswa.get("matkul_lulus", "").split(";")

        if prasyarat != "-":
            daftar_prasyarat = prasyarat.split(";")
            for req in daftar_prasyarat:
                if req not in matkul_lulus:
                    return f"❌ Gagal: Kamu belum lulus prasyarat ({req})."

        # ==========================================
        # VALIDASI SKS BERDASARKAN SEMESTER DAN IP
        # ==========================================
        semester = int(mahasiswa.get("semester", 1))
        ip_terakhir = float(mahasiswa.get("ip_terakhir", 0.0))

        jatah_sks = 20 # Default untuk Maba (Semester 1)
        if semester > 1:
            if ip_terakhir >= 3.50:
                jatah_sks = 24
            elif ip_terakhir >= 3.00:
                jatah_sks = 22
            else:
                jatah_sks = 18

        # Hitung SKS yang sudah diambil di sistem
        semua_krs = self.csv.getSemuaKrs()
        sks_terpakai = 0
        for krs in semua_krs:
            if krs["nim"] == nim and krs["status"] in ["menunggu_validasi", "disetujui"]:
                mk_diambil = self.csv.getMataKuliah(krs["kode_matkul"])
                if mk_diambil:
                    sks_terpakai += int(mk_diambil.get("sks", 0))

        sks_matkul_baru = int(matkul.get("sks", 0))
        if (sks_terpakai + sks_matkul_baru) > jatah_sks:
            return f"❌ Gagal: SKS melebihi batas. Jatah kamu: {jatah_sks} SKS, Terpakai: {sks_terpakai} SKS."

        # VALIDASI KUOTA DAN QUEUE
        semua_krs_matkul = [k for k in semua_krs if k["kode_matkul"] == kode_matkul]
        kursi_terisi = sum(1 for k in semua_krs_matkul if k["status"] in ["menunggu_validasi", "disetujui"])
        kuota_maksimal = int(matkul["kuota"])

        if kursi_terisi < kuota_maksimal:
            self.csv.tambahKrs(nim, kode_matkul, "menunggu_validasi")
            return f"✅ Sukses: {matkul['nama']} diajukan. (SKS Terpakai: {sks_terpakai + sks_matkul_baru}/{jatah_sks})."
        else:
            self.queue.enqueue(kode_matkul, nim)
            self.csv.tambahKrs(nim, kode_matkul, "waiting_list")
            return f"⏳ Kelas penuh: Kamu masuk antrian (Waiting List) untuk {matkul['nama']}."

    def batalkanMataKuliah(self, nim, kode_matkul):
        status_krs = self.csv.getStatusKrs(nim, kode_matkul)

        if status_krs is None:
            return "❌ Kamu tidak mengambil mata kuliah ini."

        status_lama = status_krs["status"]

        self.csv.hapusKrs(nim, kode_matkul)

        pesan = f"✅ Mata kuliah {kode_matkul} berhasil dibatalkan."

        if status_lama == "waiting_list":
            self.queue.removeFromQueue(kode_matkul, nim)
            return pesan

        if status_lama == "menunggu_validasi" or status_lama == "disetujui":
            nim_pengganti = self.queue.dequeue(kode_matkul)

            if nim_pengganti is not None:
                self.csv.updateStatusKrs(nim_pengganti, kode_matkul, "menunggu_validasi")
                pesan += f"\n🔄 Kursi kosong. NIM {nim_pengganti} masuk dari waiting list."

        return pesan

    def getKrsMahasiswa(self, nim):
        semua_krs = self.csv.getKrsByMahasiswa(nim)
        hasil = []

        for krs in semua_krs:
            matkul = self.csv.getMataKuliah(krs["kode_matkul"])
            nama_matkul = "-"

            if matkul is not None:
                nama_matkul = matkul["nama"]

            hasil.append({
                "nim": krs["nim"],
                "kode_matkul": krs["kode_matkul"],
                "nama": nama_matkul,
                "status": krs["status"]
            })

        return hasil

    def getWaitingListMahasiswa(self, nim):
        return self.queue.getQueueByMahasiswa(nim)

    def getDaftarValidasi(self, nip_dosen):
        dosen = self.csv.getDosen(nip_dosen)

        if dosen is None:
            return []

        matkul_diajar = dosen["dosen_mk"].split(";")
        semua_krs = self.csv.getSemuaKrs()
        hasil = []

        for krs in semua_krs:
            if krs["status"] == "menunggu_validasi" and krs["kode_matkul"] in matkul_diajar:
                matkul = self.csv.getMataKuliah(krs["kode_matkul"])
                nama_matkul = "-"

                if matkul is not None:
                    nama_matkul = matkul["nama"]

                hasil.append({
                    "nim": krs["nim"],
                    "kode_matkul": krs["kode_matkul"],
                    "nama": nama_matkul,
                    "status": krs["status"]
                })

        return hasil

    def validasiKrs(self, nip_dosen, nim, kode_matkul, setujui):
        dosen = self.csv.getDosen(nip_dosen)

        if dosen is None:
            return "❌ Data dosen tidak ditemukan."

        matkul_diajar = dosen["dosen_mk"].split(";")

        if kode_matkul not in matkul_diajar:
            return "❌ Kamu tidak memiliki hak validasi mata kuliah ini."

        status_krs = self.csv.getStatusKrs(nim, kode_matkul)

        if status_krs is None:
            return "❌ Data KRS tidak ditemukan."

        if status_krs["status"] != "menunggu_validasi":
            return "⚠️ Data ini tidak sedang menunggu validasi."

        if setujui:
            self.csv.updateStatusKrs(nim, kode_matkul, "disetujui")
            return f"✅ Pengajuan {kode_matkul} untuk NIM {nim} disetujui."

        self.csv.updateStatusKrs(nim, kode_matkul, "ditolak")

        pesan = f"❌ Pengajuan {kode_matkul} untuk NIM {nim} ditolak."

        nim_pengganti = self.queue.dequeue(kode_matkul)

        if nim_pengganti is not None:
            self.csv.updateStatusKrs(nim_pengganti, kode_matkul, "menunggu_validasi")
            pesan += f"\n🔄 NIM {nim_pengganti} masuk dari waiting list."

        return pesan

    def getMahasiswaDisetujui(self, nip_dosen):
        dosen = self.csv.getDosen(nip_dosen)

        if dosen is None:
            return []

        matkul_diajar = dosen["dosen_mk"].split(";")
        semua_krs = self.csv.getSemuaKrs()
        hasil = []

        for krs in semua_krs:
            if krs["status"] == "disetujui" and krs["kode_matkul"] in matkul_diajar:
                mahasiswa = self.csv.getMahasiswa(krs["nim"])
                matkul = self.csv.getMataKuliah(krs["kode_matkul"])

                nama_mahasiswa = "-"
                nama_matkul = "-"

                if mahasiswa is not None:
                    nama_mahasiswa = mahasiswa["nama"]

                if matkul is not None:
                    nama_matkul = matkul["nama"]

                hasil.append({
                    "nim": krs["nim"],
                    "nama_mahasiswa": nama_mahasiswa,
                    "kode_matkul": krs["kode_matkul"],
                    "nama": nama_matkul
                })

        return hasil

    def getWaitingListDosen(self, nip_dosen):
        dosen = self.csv.getDosen(nip_dosen)

        if dosen is None:
            return []

        matkul_diajar = dosen["dosen_mk"].split(";")
        semua_waiting = self.csv.loadQueue()
        hasil = []

        for kode_matkul in matkul_diajar:
            urutan = 1

            for waiting in semua_waiting:
                if waiting["kode_matkul"] == kode_matkul:
                    mahasiswa = self.csv.getMahasiswa(waiting["nim"])
                    matkul = self.csv.getMataKuliah(kode_matkul)

                    nama_mahasiswa = "-"
                    nama_matkul = "-"

                    if mahasiswa is not None:
                        nama_mahasiswa = mahasiswa["nama"]

                    if matkul is not None:
                        nama_matkul = matkul["nama"]

                    hasil.append({
                        "kode_matkul": kode_matkul,
                        "nama": nama_matkul,
                        "nim": waiting["nim"],
                        "nama_mahasiswa": nama_mahasiswa,
                        "urutan": str(urutan)
                    })

                    urutan += 1

        return hasil
    
    def inputNilaiIp(self, nip_dosen, nim, nilai_ip):
        mahasiswa = self.csv.getMahasiswa(nim)
        if mahasiswa is None:
            return "❌ Mahasiswa tidak ditemukan."
        if mahasiswa["nip_dosen_wali"] != nip_dosen:
            return "❌ Otoritas ditolak: Kamu bukan Dosen Wali mahasiswa ini."
            
        self.csv.updateIpMahasiswa(nim, nilai_ip)
        return f"✅ Berhasil mengupdate IP Mahasiswa {nim} menjadi {nilai_ip}."
    
    def cetakHasilKrs(self, nim):
        semua_krs = self.csv.getSemuaKrs()
        krs_disetujui = [k for k in semua_krs if k["nim"] == nim and k["status"] == "disetujui"]
        
        if not krs_disetujui:
            print("Belum ada mata kuliah yang disetujui untuk dicetak.")
            return

        semua_kelas = self.csv.bacaCsv("data/kelas.csv")
        semua_dosen = self.csv.bacaCsv("data/dosen.csv")
        mahasiswa = self.csv.getMahasiswa(nim)

        print(f"\n=== HASIL KARTU RENCANA STUDI (KRS) ===")
        print(f"NIM      : {nim}")
        print(f"Nama     : {mahasiswa['nama']}")
        print(f"Semester : {mahasiswa.get('semester', '-')}")
        print("-" * 125)
        print(f"{'No':<3} | {'Hari':<8} | {'Jam':<11} | {'Ruang':<15} | {'Kode':<7} | {'Mata Kuliah':<30} | {'SKS':<3} | {'Kelas':<6} | {'Dosen Pengampu':<20}")
        print("-" * 125)

        total_sks = 0
        nomor = 1

        for krs in krs_disetujui:
            kode_mk = krs["kode_matkul"]
            mk = self.csv.getMataKuliah(kode_mk)
            
            # Cari Jadwal Kelas
            jadwal = next((c for c in semua_kelas if c["kode_matkul"] == kode_mk), None)
            hari = jadwal["hari"] if jadwal else "-"
            jam = jadwal["jam"] if jadwal else "-"
            ruang = jadwal["ruangan"] if jadwal else "-"
            id_kelas = jadwal["id_kelas"] if jadwal else "-"

            nama_dosen = "-"
            for d in semua_dosen:
                if kode_mk in d.get("dosen_mk", "").split(";"):
                    nama_dosen = d["nama"]
                    break

            sks = int(mk.get("sks", 0)) if mk else 0
            total_sks += sks
            nama_mk = mk["nama"] if mk else "-"

            print(f"{nomor:<3} | {hari:<8} | {jam:<11} | {ruang:<15} | {kode_mk:<7} | {nama_mk:<30} | {sks:<3} | {id_kelas:<6} | {nama_dosen:<20}")
            nomor += 1

        print("-" * 125)
        print(f"Total SKS Diambil: {total_sks}")