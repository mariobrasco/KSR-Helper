# modules/krs_manager.py


class KRSManager:
    def __init__(self, csv_manager, tree_prasyarat, queue_manager):
        self.csv = csv_manager
        self.tree = tree_prasyarat
        self.queue = queue_manager

    # =========================
    # HELPER UMUM
    # =========================

    def getUrutanHari(self, hari):
        daftar_hari = {
            "Senin": 1,
            "Selasa": 2,
            "Rabu": 3,
            "Kamis": 4,
            "Jumat": 5,
            "Sabtu": 6,
            "Minggu": 7
        }

        return daftar_hari.get(hari, 99)

    def konversiJamKeMenit(self, jam):
        bagian_jam = jam.split(":")
        jam_angka = int(bagian_jam[0])
        menit_angka = int(bagian_jam[1])

        return jam_angka * 60 + menit_angka

    def getRentangJam(self, jam_range):
        bagian = jam_range.split("-")

        if len(bagian) != 2:
            return 0, 0

        mulai = self.konversiJamKeMenit(bagian[0])
        selesai = self.konversiJamKeMenit(bagian[1])

        return mulai, selesai

    def isJadwalBentrok(self, jam_pertama, jam_kedua):
        mulai_pertama, selesai_pertama = self.getRentangJam(jam_pertama)
        mulai_kedua, selesai_kedua = self.getRentangJam(jam_kedua)

        if mulai_pertama < selesai_kedua and mulai_kedua < selesai_pertama:
            return True

        return False

    def getJatahSks(self, mahasiswa):
        semester = int(mahasiswa.get("semester", 1))
        ip_terakhir = float(mahasiswa.get("ip_terakhir", 0.0))

        if semester <= 2:
            return 20

        if ip_terakhir >= 3.50:
            return 24

        if ip_terakhir >= 3.00:
            return 22

        return 18

    def getSksTerpakai(self, nim):
        semua_krs = self.csv.getKrsByMahasiswa(nim)
        total_sks = 0

        for krs in semua_krs:
            if krs["status"] == "menunggu_validasi" or krs["status"] == "disetujui":
                matkul = self.csv.getMataKuliah(krs["kode_matkul"])

                if matkul is not None:
                    total_sks += int(matkul.get("sks", 0))

        return total_sks

    def getTotalSksLulus(self, mahasiswa):
        matkul_lulus = mahasiswa.get("matkul_lulus", "-")

        if matkul_lulus == "-":
            return 0

        daftar_lulus = matkul_lulus.split(";")
        total_sks = 0

        for kode_matkul in daftar_lulus:
            matkul = self.csv.getMataKuliah(kode_matkul)

            if matkul is not None:
                total_sks += int(matkul["sks"])

        return total_sks

    def getInfoKelasLengkap(self, kelas):
        matkul = self.csv.getMataKuliah(kelas["kode_matkul"])
        dosen = self.csv.getDosen(kelas["nip_dosen"])

        nama_matkul = "-"
        sks = "0"
        semester = "-"
        prasyarat = "-"
        kelompok_pilihan = "-"
        min_sks_lulus = "0"
        nama_dosen = "-"

        if matkul is not None:
            nama_matkul = matkul["nama"]
            sks = matkul["sks"]
            semester = matkul["semester"]
            prasyarat = matkul["prasyarat"]
            kelompok_pilihan = matkul["kelompok_pilihan"]
            min_sks_lulus = matkul["min_sks_lulus"]

        if dosen is not None:
            nama_dosen = dosen["nama"]

        peserta_terisi = self.csv.getJumlahPesertaKelas(kelas["id_kelas"])
        kuota = kelas["kuota"]
        jumlah_waiting = self.queue.getJumlahWaitingListKelas(kelas["id_kelas"])

        return {
            "id_kelas": kelas["id_kelas"],
            "kode_matkul": kelas["kode_matkul"],
            "nama": nama_matkul,
            "nama_kelas": kelas["nama_kelas"],
            "sks": sks,
            "semester": semester,
            "prasyarat": prasyarat,
            "kelompok_pilihan": kelompok_pilihan,
            "min_sks_lulus": min_sks_lulus,
            "kuota": kuota,
            "peserta": f"{peserta_terisi}/{kuota}",
            "waiting": str(jumlah_waiting),
            "ruangan": kelas["ruangan"],
            "hari": kelas["hari"],
            "jam": kelas["jam"],
            "nip_dosen": kelas["nip_dosen"],
            "nama_dosen": nama_dosen
        }

    # =========================
    # DAFTAR KELAS
    # =========================

    def getDaftarMataKuliah(self):
        return self.csv.getSemuaMataKuliah()

    def getDaftarKelasTersedia(self, nim):
        mahasiswa = self.csv.getMahasiswa(nim)

        if mahasiswa is None:
            return []

        semester_mahasiswa = int(mahasiswa["semester"])
        semua_kelas = self.csv.getSemuaKelas()
        hasil = []

        for kelas in semua_kelas:
            matkul = self.csv.getMataKuliah(kelas["kode_matkul"])

            if matkul is None:
                continue

            semester_matkul = int(matkul["semester"])

            if semester_matkul > semester_mahasiswa:
                continue

            if self.sudahLulusMatkul(mahasiswa, matkul["kode"]):
                continue

            if self.sudahAmbilMatkulAktif(mahasiswa["nim"], matkul["kode"]):
                continue

            prasyarat_ok, prasyarat_belum_lulus = self.cekPrasyarat(mahasiswa, matkul)

            if not prasyarat_ok:
                continue

            kelompok_ok = self.cekKelompokPilihan(mahasiswa, matkul)

            if not kelompok_ok:
                continue

            min_sks_ok = self.cekMinSksLulus(mahasiswa, matkul)

            if not min_sks_ok:
                continue

            hasil.append(self.getInfoKelasLengkap(kelas))

        hasil.sort(key=lambda data: (
            int(data["semester"]),
            data["kode_matkul"],
            data["nama_kelas"]
        ))

        return hasil

    def getDaftarKelasDosen(self, nip):
        semua_kelas = self.csv.getKelasDosen(nip)
        hasil = []

        for kelas in semua_kelas:
            hasil.append(self.getInfoKelasLengkap(kelas))

        hasil.sort(key=lambda data: (
            self.getUrutanHari(data["hari"]),
            data["jam"],
            data["kode_matkul"],
            data["nama_kelas"]
        ))

        return hasil

    # =========================
    # TREE PRASYARAT
    # =========================

    def tampilkanTreePrasyarat(self):
        self.tree.tampilkanTree("KA591")

    def tampilkanTreeSemester(self, semester):
        self.tree.tampilkanTreeSemester(semester)

    def tampilkanTreeSemesterMahasiswa(self, nim, mode):
        mahasiswa = self.csv.getMahasiswa(nim)

        if mahasiswa is None:
            print("Data mahasiswa tidak ditemukan.")
            return

        semester = int(mahasiswa["semester"])

        if mode == "sebelumnya":
            semester_target = semester - 1
        elif mode == "berikutnya":
            semester_target = semester + 1
        else:
            semester_target = semester

        if semester_target < 1:
            print("Tidak ada semester sebelumnya.")
            return

        if semester_target > 8:
            print("Tidak ada semester berikutnya.")
            return

        self.tampilkanTreeSemester(semester_target)

    # =========================
    # VALIDASI AKADEMIK
    # =========================

    def sudahLulusMatkul(self, mahasiswa, kode_matkul):
        matkul_lulus = mahasiswa.get("matkul_lulus", "-")

        if matkul_lulus == "-":
            return False

        daftar_lulus = matkul_lulus.split(";")

        return kode_matkul in daftar_lulus

    def sudahAmbilMatkulAktif(self, nim, kode_matkul):
        status_matkul = self.csv.getStatusKrsByMatkul(nim, kode_matkul)

        if status_matkul is None:
            return False

        if status_matkul["status"] == "ditolak":
            return False

        return True

    def cekPrasyarat(self, mahasiswa, matkul):
        prasyarat = matkul["prasyarat"]

        if prasyarat == "-":
            return True, []

        matkul_lulus = mahasiswa.get("matkul_lulus", "-").split(";")
        daftar_prasyarat = prasyarat.split(";")
        prasyarat_belum_lulus = []

        for kode_prasyarat in daftar_prasyarat:
            if kode_prasyarat not in matkul_lulus:
                prasyarat_belum_lulus.append(kode_prasyarat)

        if len(prasyarat_belum_lulus) > 0:
            return False, prasyarat_belum_lulus

        return True, []

    def cekKelompokPilihan(self, mahasiswa, matkul):
        kelompok_pilihan = matkul.get("kelompok_pilihan", "-")

        if kelompok_pilihan == "-":
            return True

        semua_matkul = self.csv.getSemuaMataKuliah()
        matkul_lulus = mahasiswa.get("matkul_lulus", "-").split(";")
        semua_krs = self.csv.getKrsByMahasiswa(mahasiswa["nim"])

        for data_matkul in semua_matkul:
            if data_matkul.get("kelompok_pilihan", "-") == kelompok_pilihan:
                if data_matkul["kode"] in matkul_lulus:
                    return False

                for krs in semua_krs:
                    if krs["kode_matkul"] == data_matkul["kode"]:
                        if krs["status"] != "ditolak":
                            return False

        return True

    def cekMinSksLulus(self, mahasiswa, matkul):
        min_sks_lulus = int(matkul.get("min_sks_lulus", 0))

        if min_sks_lulus == 0:
            return True

        total_sks_lulus = self.getTotalSksLulus(mahasiswa)

        if total_sks_lulus >= min_sks_lulus:
            return True

        return False

    def cekBatasSks(self, mahasiswa, matkul):
        nim = mahasiswa["nim"]
        jatah_sks = self.getJatahSks(mahasiswa)
        sks_terpakai = self.getSksTerpakai(nim)
        sks_matkul_baru = int(matkul.get("sks", 0))

        if sks_terpakai + sks_matkul_baru > jatah_sks:
            return False, sks_terpakai, jatah_sks

        return True, sks_terpakai, jatah_sks

    def cekBentrokJadwal(self, nim, id_kelas_baru):
        kelas_baru = self.csv.getKelas(id_kelas_baru)

        if kelas_baru is None:
            return False, None

        krs_mahasiswa = self.csv.getKrsByMahasiswa(nim)

        for krs in krs_mahasiswa:
            if krs["status"] == "ditolak" or krs["status"] == "waiting_list":
                continue

            kelas_lama = self.csv.getKelas(krs["id_kelas"])

            if kelas_lama is None:
                continue

            if kelas_lama["hari"] != kelas_baru["hari"]:
                continue

            if self.isJadwalBentrok(kelas_lama["jam"], kelas_baru["jam"]):
                matkul_lama = self.csv.getMataKuliah(kelas_lama["kode_matkul"])
                nama_matkul_lama = "-"

                if matkul_lama is not None:
                    nama_matkul_lama = matkul_lama["nama"]

                data_bentrok = {
                    "id_kelas": kelas_lama["id_kelas"],
                    "kode_matkul": kelas_lama["kode_matkul"],
                    "nama": nama_matkul_lama,
                    "hari": kelas_lama["hari"],
                    "jam": kelas_lama["jam"]
                }

                return True, data_bentrok

        return False, None

    # =========================
    # ROLE MAHASISWA
    # =========================

    def ambilMataKuliah(self, nim, id_kelas):
        mahasiswa = self.csv.getMahasiswa(nim)
        kelas = self.csv.getKelas(id_kelas)

        if mahasiswa is None:
            return "❌ Data mahasiswa tidak ditemukan."

        if kelas is None:
            return "❌ Kelas tidak ditemukan."

        kode_matkul = kelas["kode_matkul"]
        matkul = self.csv.getMataKuliah(kode_matkul)

        if matkul is None:
            return "❌ Data mata kuliah tidak ditemukan."

        semester_mahasiswa = int(mahasiswa["semester"])
        semester_matkul = int(matkul["semester"])

        if semester_matkul > semester_mahasiswa:
            return f"❌ Gagal: Mata kuliah ini baru tersedia di semester {matkul['semester']}."

        if self.sudahLulusMatkul(mahasiswa, kode_matkul):
            return "⚠️ Kamu sudah lulus mata kuliah ini."

        if self.sudahAmbilMatkulAktif(nim, kode_matkul):
            return "⚠️ Kamu sudah mengambil atau mengajukan mata kuliah ini di kelas lain."

        prasyarat_ok, prasyarat_belum_lulus = self.cekPrasyarat(mahasiswa, matkul)

        if not prasyarat_ok:
            return "❌ Gagal: Belum lulus prasyarat " + ";".join(prasyarat_belum_lulus)

        kelompok_ok = self.cekKelompokPilihan(mahasiswa, matkul)

        if not kelompok_ok:
            return "❌ Gagal: Mata kuliah ini berada dalam kelompok pilihan yang sudah kamu ambil."

        min_sks_ok = self.cekMinSksLulus(mahasiswa, matkul)

        if not min_sks_ok:
            total_sks_lulus = self.getTotalSksLulus(mahasiswa)
            return f"❌ Gagal: Minimal SKS lulus untuk mengambil mata kuliah ini adalah {matkul['min_sks_lulus']} SKS. SKS lulus kamu saat ini {total_sks_lulus}."

        sks_ok, sks_terpakai, jatah_sks = self.cekBatasSks(mahasiswa, matkul)

        if not sks_ok:
            return f"❌ Gagal: SKS melebihi batas. Jatah: {jatah_sks} SKS, terpakai: {sks_terpakai} SKS."

        bentrok, data_bentrok = self.cekBentrokJadwal(nim, id_kelas)

        if bentrok:
            return (
                "❌ Gagal: Jadwal bentrok dengan "
                + data_bentrok["nama"]
                + " kelas "
                + data_bentrok["id_kelas"]
                + f" pada {data_bentrok['hari']} jam {data_bentrok['jam']}."
            )

        peserta_terisi = self.csv.getJumlahPesertaKelas(id_kelas)
        kuota_maksimal = int(kelas["kuota"])

        if peserta_terisi < kuota_maksimal:
            self.csv.tambahKrs(nim, id_kelas, kode_matkul, "menunggu_validasi")

            return (
                f"✅ Berhasil mengajukan {matkul['nama']} kelas {kelas['nama_kelas']}.\n"
                f"Status: menunggu validasi dosen.\n"
                f"SKS: {sks_terpakai + int(matkul['sks'])}/{jatah_sks}\n"
                f"Kuota kelas: {peserta_terisi + 1}/{kuota_maksimal}"
            )

        self.queue.enqueue(id_kelas, nim)
        self.csv.tambahKrs(nim, id_kelas, kode_matkul, "waiting_list")

        urutan_waiting = self.queue.getUrutanMahasiswa(id_kelas, nim)

        return (
            f"⚠️ Kuota {matkul['nama']} kelas {kelas['nama_kelas']} penuh.\n"
            f"Kamu masuk waiting list kelas {id_kelas}.\n"
            f"Urutan waiting list: {urutan_waiting}"
        )

    def batalkanMataKuliah(self, nim, id_kelas):
        status_krs = self.csv.getStatusKrsByKelas(nim, id_kelas)

        if status_krs is None:
            return "❌ Kamu tidak mengambil kelas ini."

        kelas = self.csv.getKelas(id_kelas)

        if kelas is None:
            return "❌ Data kelas tidak ditemukan."

        matkul = self.csv.getMataKuliah(kelas["kode_matkul"])
        nama_matkul = kelas["kode_matkul"]

        if matkul is not None:
            nama_matkul = matkul["nama"]

        status_lama = status_krs["status"]

        self.csv.hapusKrs(nim, id_kelas)

        pesan = f"✅ {nama_matkul} kelas {kelas['nama_kelas']} berhasil dibatalkan."

        if status_lama == "waiting_list":
            self.queue.removeFromQueue(id_kelas, nim)
            return pesan

        if status_lama == "menunggu_validasi" or status_lama == "disetujui":
            nim_pengganti = self.queue.dequeue(id_kelas)

            if nim_pengganti is not None:
                self.csv.updateStatusKrs(nim_pengganti, id_kelas, "menunggu_validasi")
                pesan += f"\n🔄 Kursi kosong. NIM {nim_pengganti} masuk dari waiting list kelas {id_kelas}."

        return pesan

    def getKrsMahasiswa(self, nim):
        semua_krs = self.csv.getKrsByMahasiswa(nim)
        hasil = []

        for krs in semua_krs:
            kelas = self.csv.getKelas(krs["id_kelas"])

            if kelas is None:
                continue

            matkul = self.csv.getMataKuliah(krs["kode_matkul"])
            dosen = self.csv.getDosen(kelas["nip_dosen"])

            nama_matkul = "-"
            sks = "0"
            nama_dosen = "-"

            if matkul is not None:
                nama_matkul = matkul["nama"]
                sks = matkul["sks"]

            if dosen is not None:
                nama_dosen = dosen["nama"]

            hasil.append({
                "nim": krs["nim"],
                "id_kelas": krs["id_kelas"],
                "kode_matkul": krs["kode_matkul"],
                "nama": nama_matkul,
                "nama_kelas": kelas["nama_kelas"],
                "sks": sks,
                "hari": kelas["hari"],
                "jam": kelas["jam"],
                "ruangan": kelas["ruangan"],
                "nama_dosen": nama_dosen,
                "status": krs["status"]
            })

        hasil.sort(key=lambda data: (
            self.getUrutanHari(data["hari"]),
            data["jam"]
        ))

        return hasil

    def getWaitingListMahasiswa(self, nim):
        return self.queue.getQueueByMahasiswa(nim)

    # =========================
    # ROLE DOSEN
    # =========================

    def getDaftarValidasi(self, nip_dosen):
        kelas_diajar = self.csv.getKelasDosen(nip_dosen)
        daftar_id_kelas = []

        for kelas in kelas_diajar:
            daftar_id_kelas.append(kelas["id_kelas"])

        semua_krs = self.csv.getSemuaKrs()
        hasil = []

        for krs in semua_krs:
            if krs["status"] == "menunggu_validasi" and krs["id_kelas"] in daftar_id_kelas:
                kelas = self.csv.getKelas(krs["id_kelas"])

                if kelas is None:
                    continue

                matkul = self.csv.getMataKuliah(krs["kode_matkul"])
                mahasiswa = self.csv.getMahasiswa(krs["nim"])

                hasil.append({
                    "nim": krs["nim"],
                    "nama_mahasiswa": mahasiswa["nama"] if mahasiswa is not None else "-",
                    "id_kelas": krs["id_kelas"],
                    "kode_matkul": krs["kode_matkul"],
                    "nama": matkul["nama"] if matkul is not None else "-",
                    "nama_kelas": kelas["nama_kelas"],
                    "status": krs["status"]
                })

        return hasil

    def validasiKrs(self, nip_dosen, nim, id_kelas, setujui):
        kelas = self.csv.getKelas(id_kelas)

        if kelas is None:
            return "❌ Data kelas tidak ditemukan."

        if kelas["nip_dosen"] != nip_dosen:
            return "❌ Kamu tidak memiliki hak validasi kelas ini."

        status_krs = self.csv.getStatusKrsByKelas(nim, id_kelas)

        if status_krs is None:
            return "❌ Data KRS tidak ditemukan."

        if status_krs["status"] != "menunggu_validasi":
            return "⚠️ Data ini tidak sedang menunggu validasi."

        if setujui:
            self.csv.updateStatusKrs(nim, id_kelas, "disetujui")
            return f"✅ Pengajuan kelas {id_kelas} untuk NIM {nim} disetujui."

        self.csv.updateStatusKrs(nim, id_kelas, "ditolak")

        pesan = f"❌ Pengajuan kelas {id_kelas} untuk NIM {nim} ditolak."

        nim_pengganti = self.queue.dequeue(id_kelas)

        if nim_pengganti is not None:
            self.csv.updateStatusKrs(nim_pengganti, id_kelas, "menunggu_validasi")
            pesan += f"\n🔄 NIM {nim_pengganti} masuk dari waiting list kelas {id_kelas}."

        return pesan

    def getMahasiswaDisetujui(self, nip_dosen):
        kelas_diajar = self.csv.getKelasDosen(nip_dosen)
        daftar_id_kelas = []

        for kelas in kelas_diajar:
            daftar_id_kelas.append(kelas["id_kelas"])

        semua_krs = self.csv.getSemuaKrs()
        hasil = []

        for krs in semua_krs:
            if krs["status"] == "disetujui" and krs["id_kelas"] in daftar_id_kelas:
                mahasiswa = self.csv.getMahasiswa(krs["nim"])
                kelas = self.csv.getKelas(krs["id_kelas"])
                matkul = self.csv.getMataKuliah(krs["kode_matkul"])

                hasil.append({
                    "nim": krs["nim"],
                    "nama_mahasiswa": mahasiswa["nama"] if mahasiswa is not None else "-",
                    "id_kelas": krs["id_kelas"],
                    "kode_matkul": krs["kode_matkul"],
                    "nama": matkul["nama"] if matkul is not None else "-",
                    "nama_kelas": kelas["nama_kelas"] if kelas is not None else "-"
                })

        return hasil

    def getWaitingListDosen(self, nip_dosen):
        kelas_diajar = self.csv.getKelasDosen(nip_dosen)
        hasil = []

        for kelas in kelas_diajar:
            daftar_waiting = self.queue.getQueueByKelas(kelas["id_kelas"])

            for data in daftar_waiting:
                mahasiswa = self.csv.getMahasiswa(data["nim"])
                data["nama_mahasiswa"] = mahasiswa["nama"] if mahasiswa is not None else "-"
                hasil.append(data)

        return hasil


    # =========================
    # CETAK HASIL KRS
    # =========================

    def cetakHasilKrs(self, nim):
        mahasiswa = self.csv.getMahasiswa(nim)

        if mahasiswa is None:
            print("Data mahasiswa tidak ditemukan.")
            return

        daftar_krs = self.getKrsMahasiswa(nim)
        krs_disetujui = []

        for krs in daftar_krs:
            if krs["status"] == "disetujui":
                krs_disetujui.append(krs)

        if len(krs_disetujui) == 0:
            print("Belum ada mata kuliah yang disetujui untuk dicetak.")
            return

        krs_disetujui.sort(key=lambda data: (
            self.getUrutanHari(data["hari"]),
            data["jam"]
        ))

        print("\n=== HASIL KARTU RENCANA STUDI (KRS) ===")
        print("NIM      :", nim)
        print("Nama     :", mahasiswa["nama"])
        print("Semester :", mahasiswa["semester"])
        print("IP       :", mahasiswa["ip_terakhir"])
        print("-" * 150)

        total_sks = 0
        hari_sebelumnya = ""

        for krs in krs_disetujui:
            if krs["hari"] != hari_sebelumnya:
                print(f"\n{krs['hari'].upper()}")
                print("-" * 150)
                print(
                    f"{'Jam':<12} | "
                    f"{'ID Kelas':<10} | "
                    f"{'Kode MK':<8} | "
                    f"{'Mata Kuliah':<40} | "
                    f"{'SKS':<3} | "
                    f"{'Dosen':<28} | "
                    f"{'Ruang':<20} | "
                    f"{'Kelas':<6}"
                )
                print("-" * 150)
                hari_sebelumnya = krs["hari"]

            print(
                f"{krs['jam']:<12} | "
                f"{krs['id_kelas']:<10} | "
                f"{krs['kode_matkul']:<8} | "
                f"{krs['nama']:<40} | "
                f"{krs['sks']:<3} | "
                f"{krs['nama_dosen']:<28} | "
                f"{krs['ruangan']:<20} | "
                f"{krs['nama_kelas']:<6}"
            )

            total_sks += int(krs["sks"])

        print("-" * 150)
        print("Total SKS:", total_sks)