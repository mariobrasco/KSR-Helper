# modules/queue_waiting_list.py


class QueueManager:
    def __init__(self, csv_manager):
        self.csv = csv_manager

    def enqueue(self, kode_matkul, nim):
        antrian = self.csv.loadQueue()

        for data in antrian:
            if data["kode_matkul"] == kode_matkul and data["nim"] == nim:
                return

        data_baru = {
            "kode_matkul": kode_matkul,
            "nim": nim
        }

        antrian.append(data_baru)
        self.csv.saveQueue(antrian)

    def dequeue(self, kode_matkul):
        antrian = self.csv.loadQueue()

        for index in range(len(antrian)):
            data = antrian[index]

            if data["kode_matkul"] == kode_matkul:
                nim_terdepan = data["nim"]
                antrian.pop(index)
                self.csv.saveQueue(antrian)

                return nim_terdepan

        return None

    def removeFromQueue(self, kode_matkul, nim):
        antrian = self.csv.loadQueue()
        antrian_baru = []

        for data in antrian:
            if data["kode_matkul"] == kode_matkul and data["nim"] == nim:
                continue

            antrian_baru.append(data)

        self.csv.saveQueue(antrian_baru)

    def getQueueByMatkul(self, kode_matkul):
        antrian = self.csv.loadQueue()
        hasil = []
        urutan = 1

        for data in antrian:
            if data["kode_matkul"] == kode_matkul:
                data_baru = {
                    "kode_matkul": data["kode_matkul"],
                    "nim": data["nim"],
                    "urutan": str(urutan)
                }

                hasil.append(data_baru)
                urutan += 1

        return hasil

    def getQueueByMahasiswa(self, nim):
        antrian = self.csv.loadQueue()
        hasil = []
        semua_matkul = self.csv.getSemuaMataKuliah()

        for data in antrian:
            if data["nim"] == nim:
                urutan = self.getUrutanMahasiswa(data["kode_matkul"], nim)
                nama_matkul = "-"

                for matkul in semua_matkul:
                    if matkul["kode"] == data["kode_matkul"]:
                        nama_matkul = matkul["nama"]

                hasil.append({
                    "kode_matkul": data["kode_matkul"],
                    "nama": nama_matkul,
                    "nim": nim,
                    "urutan": str(urutan)
                })

        return hasil

    def getUrutanMahasiswa(self, kode_matkul, nim):
        antrian = self.csv.loadQueue()
        urutan = 1

        for data in antrian:
            if data["kode_matkul"] == kode_matkul:
                if data["nim"] == nim:
                    return urutan

                urutan += 1

        return "-"