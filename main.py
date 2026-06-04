from queue_waiting_list import Queue

queue = Queue()

while True:
    print("\n=== KRS HELPER ===")
    print("1. Tambah Antrian")
    print("2. Proses (Keluar Antrian Terdepan)")
    print("3. Lihat Waiting List")
    print("0. Keluar")

    pilihan = input("Pilih: ")

    if pilihan == "1":
        nim = input("Masukkan NIM: ")
        queue.enqueue(nim)
        print("Masuk waiting list")

    elif pilihan == "2":
        hasil = queue.dequeue()
        if hasil:
            print(f"{hasil} masuk kelas")
        else:
            print("Antrian kosong")

    elif pilihan == "3":
        queue.display()

    elif pilihan == "0":
        break