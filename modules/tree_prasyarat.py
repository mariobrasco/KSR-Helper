# modules/tree_prasyarat.py


class Node:
    def __init__(self, kode, nama, sks="-", semester="-"):
        self.kode = kode
        self.nama = nama
        self.sks = sks
        self.semester = semester
        self.children = []

    def tambahChild(self, child):
        self.children.append(child)


class TreePrasyarat:
    def __init__(self, csv_manager):
        self.csv = csv_manager

    def getPrasyarat(self, kode_matkul):
        matkul = self.csv.getMataKuliah(kode_matkul)

        if matkul is None:
            return "-"

        return matkul["prasyarat"]

    def getNamaMataKuliah(self, kode_matkul):
        matkul = self.csv.getMataKuliah(kode_matkul)

        if matkul is None:
            return "-"

        return matkul["nama"]

    def buatNode(self, kode_matkul, visited=None):
        if visited is None:
            visited = []

        matkul = self.csv.getMataKuliah(kode_matkul)

        if matkul is None:
            return None

        node = Node(
            matkul["kode"],
            matkul["nama"],
            matkul["sks"],
            matkul["semester"]
        )

        if kode_matkul in visited:
            return node

        visited.append(kode_matkul)

        prasyarat = matkul["prasyarat"]

        if prasyarat != "-":
            daftar_prasyarat = prasyarat.split(";")

            for kode_prasyarat in daftar_prasyarat:
                child = self.buatNode(kode_prasyarat, visited.copy())

                if child is not None:
                    node.tambahChild(child)

        return node

    def tampilkanTree(self, kode_root="KA591"):
        root = self.buatNode(kode_root)

        if root is None:
            print("Data mata kuliah tidak ditemukan.")
            return

        self.cetakTree(root)

    def cetakTree(self, node, prefix="", is_last=True, visited=None, is_root=True):
        if visited is None:
            visited = []

        label = f"{node.kode} - {node.nama} ({node.sks} SKS, Smt {node.semester})"

        if node.kode in visited:
            if node.semester != "1":
                label += " (prasyarat sama, sudah muncul sebelumnya)"

            if is_root:
                print(label)
            else:
                connector = "└── " if is_last else "├── "
                print(prefix + connector + label)

            return

        visited.append(node.kode)

        if is_root:
            print(label)
        else:
            connector = "└── " if is_last else "├── "
            print(prefix + connector + label)

        if is_root:
            child_prefix = ""
        else:
            if is_last:
                child_prefix = prefix + "    "
            else:
                child_prefix = prefix + "│   "

        jumlah_child = len(node.children)

        for index in range(jumlah_child):
            child = node.children[index]
            child_is_last = index == jumlah_child - 1
            self.cetakTree(child, child_prefix, child_is_last, visited, False)

    def tampilkanTreeSemester(self, semester):
        semua_matkul = self.csv.getMataKuliahBySemester(semester)

        if len(semua_matkul) == 0:
            print(f"Tidak ada mata kuliah untuk semester {semester}.")
            return

        print(f"\n=== TREE PRASYARAT MATA KULIAH SEMESTER {semester} ===")

        for matkul in semua_matkul:
            print("\n" + "=" * 90)
            print(f"{matkul['kode']} - {matkul['nama']} ({matkul['sks']} SKS)")
            print("=" * 90)

            if matkul["prasyarat"] == "-":
                print(f"{matkul['kode']} - {matkul['nama']} ({matkul['sks']} SKS, Smt {matkul['semester']})")
                print("└── Tidak memiliki prasyarat")
            else:
                self.tampilkanTree(matkul["kode"])

    def tampilkanUrutanPrasyarat(self, kode_matkul):
        root = self.buatNode(kode_matkul)

        if root is None:
            print("Mata kuliah tidak ditemukan.")
            return

        hasil = []
        self.postOrder(root, hasil)

        print("\nUrutan pengambilan dari prasyarat paling dasar:")
        print("-" * 80)

        nomor = 1

        for data in hasil:
            print(
                f"{nomor}. {data['kode']} - {data['nama']} "
                f"({data['sks']} SKS, Semester {data['semester']})"
            )
            nomor += 1

    def postOrder(self, node, hasil, visited=None):
        if visited is None:
            visited = []

        if node.kode in visited:
            return

        visited.append(node.kode)

        for child in node.children:
            self.postOrder(child, hasil, visited)

        hasil.append({
            "kode": node.kode,
            "nama": node.nama,
            "sks": node.sks,
            "semester": node.semester
        })

    def getDaftarPrasyaratLengkap(self, kode_matkul):
        root = self.buatNode(kode_matkul)

        if root is None:
            return []

        hasil = []
        self.postOrder(root, hasil)

        daftar_prasyarat = []

        for data in hasil:
            if data["kode"] != kode_matkul:
                daftar_prasyarat.append(data)

        return daftar_prasyarat