# modules/tree_prasyarat.py


class Node:
    def __init__(self, kode, nama):
        self.kode = kode
        self.nama = nama
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

    def buatNode(self, kode_matkul):
        matkul = self.csv.getMataKuliah(kode_matkul)

        if matkul is None:
            return None

        node = Node(matkul["kode"], matkul["nama"])
        prasyarat = matkul["prasyarat"]

        if prasyarat != "-":
            daftar_prasyarat = prasyarat.split(";")

            for kode_prasyarat in daftar_prasyarat:
                child = self.buatNode(kode_prasyarat)

                if child is not None:
                    node.tambahChild(child)

        return node

    def tampilkanTree(self, kode_root="KA591"):
        root = self.buatNode(kode_root)

        if root is None:
            print("Data root tree tidak ditemukan.")
            return

        self.cetakTree(root)

    def cetakTree(self, node, level=0, visited=None):
        if visited is None:
            visited = []

        indent = "    " * level

        if node.kode in visited:
            print(indent + f"↳ {node.kode} - {node.nama} (sudah ditampilkan)")
            return

        visited.append(node.kode)

        if level == 0:
            print(f"{node.kode} - {node.nama}")
        else:
            print(indent + f"└── {node.kode} - {node.nama}")

        for child in node.children:
            self.cetakTree(child, level + 1, visited)

    def tampilkanUrutanPrasyarat(self, kode_matkul):
        root = self.buatNode(kode_matkul)

        if root is None:
            print("Mata kuliah tidak ditemukan.")
            return

        hasil = []
        self.postOrder(root, hasil)

        print("\nUrutan mata kuliah dari dasar:")
        for data in hasil:
            print(f"- {data['kode']} - {data['nama']}")

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
            "nama": node.nama
        })