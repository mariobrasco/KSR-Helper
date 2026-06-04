# admin_main.py

from modules.auth_manager import loginAdmin
from views.admin_menu import menuAdmin


def main():
    while True:
        print("\n=== PORTAL ADMIN KRS-HELPER ===")
        print("1. Login Admin")
        print("2. Keluar")

        pilihan = input("Pilih menu: ")

        if pilihan == "1":
            admin = loginAdmin()

            if admin is not None:
                menuAdmin(admin)

        elif pilihan == "2":
            print("Keluar dari portal admin.")
            break

        else:
            print("Pilihan tidak valid.")


if __name__ == "__main__":
    main()