# main.py

from modules.csv_manager import CsvManager
from modules.tree_prasyarat import TreePrasyarat
from modules.queue_waiting_list import QueueManager
from modules.krs_manager import KRSManager
from modules.auth_manager import loginMahasiswa, loginDosen

from views.mahasiswa_menu import menuMahasiswa
from views.dosen_menu import menuDosen


def main():
    csv_manager = CsvManager()
    tree_prasyarat = TreePrasyarat(csv_manager)
    queue_manager = QueueManager(csv_manager)
    krs_logic = KRSManager(csv_manager, tree_prasyarat, queue_manager)

    while True:
        print("\n=== PORTAL KRS-HELPER ===")
        print("1. Login Mahasiswa")
        print("2. Login Dosen")
        print("3. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            mahasiswa = loginMahasiswa()

            if mahasiswa is not None:
                menuMahasiswa(mahasiswa, krs_logic)

        elif pilihan == "2":
            dosen = loginDosen()

            if dosen is not None:
                menuDosen(dosen, krs_logic)

        elif pilihan == "3":
            print("Terima kasih sudah menggunakan KRS-Helper.")
            break

        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()