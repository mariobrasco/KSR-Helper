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

        print(f"{'No':<4} | {'NIM':<12} | {'Kode MK':<10} | {'Status':<20}")
        print("-" * 55)

        nomor = 1

        for krs in semua_krs:
            print(
                f"{nomor:<4} | "
                f"{krs['nim']:<12} | "
                f"{krs['kode_matkul']:<10} | "
                f"{krs['status']:<20}"
            )
            nomor += 1

    def tampilkanSemuaWaitingList(self):
        semua_waiting = self.csv.loadQueue()

        print("\n=== LAPORAN SEMUA WAITING LIST ===")

        if len(semua_waiting) == 0:
            print("Belum ada data waiting list.")
            return

        print(f"{'No':<4} | {'Kode MK':<10} | {'NIM':<12}")
        print("-" * 35)

        nomor = 1

        for waiting in semua_waiting:
            print(
                f"{nomor:<4} | "
                f"{waiting['kode_matkul']:<10} | "
                f"{waiting['nim']:<12}"
            )
            nomor += 1