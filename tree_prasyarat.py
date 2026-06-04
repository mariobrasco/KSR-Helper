class Node:
    def __init__(self, kode, nama):
        self.kode = kode
        self.nama = nama
        self.children = []

    def add_child(self, child):
        self.children.append(child)


# =========================
# BUILD TREE
# =========================

def build_tree():

    daspro = Node("RL117", "Dasar Pemrograman")
    mtk_dasar = Node("RL118", "Matematika Dasar")
    mtk_diskrit = Node("RL120", "Matematika Diskrit")

    struktur_data = Node("RL216", "Struktur Data & Algoritma")
    basis_data = Node("RL315", "Basis Data")
    oop = Node("RL322", "OOP")
    os = Node("RL316", "Sistem Operasi")
    rkpl = Node("RL215", "Rekayasa Kebutuhan Perangkat Lunak")
    pengantar_rpl = Node("RL116", "Pengantar RPL")
    skripsi = Node("KA591", "Skripsi")

    # =========================
    # RELASI
    # =========================

    mtk_diskrit.add_child(mtk_dasar)

    struktur_data.add_child(daspro)

    basis_data.add_child(daspro)
    basis_data.add_child(mtk_diskrit)

    oop.add_child(daspro)

    os.add_child(daspro)

    rkpl.add_child(pengantar_rpl)

    skripsi.add_child(struktur_data)
    skripsi.add_child(basis_data)
    skripsi.add_child(oop)
    skripsi.add_child(os)
    skripsi.add_child(rkpl)

    return skripsi


# =========================
# PRINT DIAGRAM PANAH
# =========================

def print_arrow_tree(node, indent=0, visited=None):
    if visited is None:
        visited = set()

    if node.kode in visited:
        return
    visited.add(node.kode)

    # root tampil
    if indent == 0:
        print(f"{node.kode} - {node.nama}")

    for child in node.children:
        print("   " * indent + f"↓ {child.kode} - {child.nama}")
        print_arrow_tree(child, indent + 1, visited)


# =========================
# MAIN
# =========================

if __name__ == "__main__":
    root = build_tree()

    print("\n=== KRS-HELPER - DIAGRAM PRASYARAT ===\n")
    print_arrow_tree(root)