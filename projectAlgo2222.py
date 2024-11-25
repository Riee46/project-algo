import os
import pandas as pd
from datetime import datetime
from tabulate import tabulate

DATA_OBAT_CSV = "data_obat.csv"

# Fungsi membaca data dari CSV
def baca_data_obat():
    if not os.path.exists(DATA_OBAT_CSV):
        # Buat file CSV kosong jika belum ada
        pd.DataFrame(columns=["Nama Obat", "Dosis", "Jumlah", "Tanggal Kadaluarsa"]).to_csv(DATA_OBAT_CSV, index=False)
    try:
        df = pd.read_csv(DATA_OBAT_CSV)
        return df.to_dict(orient="records")
    except pd.errors.EmptyDataError:
        return []

# Fungsi menulis data ke CSV
def tulis_data_obat(data):
    df = pd.DataFrame(data)
    df.to_csv(DATA_OBAT_CSV, index=False)

# Fungsi untuk menambah obat
def tambah_obat():
    print("=== Menambah Obat ===")
    nama_obat = input("Masukkan nama obat: ")
    dosis = input("Masukkan dosis obat: ")
    jumlah = input("Masukkan jumlah obat: ")
    if not jumlah.isdigit():
        print("Jumlah harus berupa angka!")
        return
    jumlah = int(jumlah)
    tanggal_kadaluarsa = input("Masukkan tanggal kadaluarsa (YYYY-MM-DD): ")

    # Validasi format tanggal
    try:
        datetime.strptime(tanggal_kadaluarsa, "%Y-%m-%d")
    except ValueError:
        print("Format tanggal salah! Gunakan format YYYY-MM-DD.")
        return

    data = baca_data_obat()
    data.append({
        "Nama Obat": nama_obat,
        "Dosis": dosis,
        "Jumlah": jumlah,
        "Tanggal Kadaluarsa": tanggal_kadaluarsa
    })
    tulis_data_obat(data)
    print("Obat berhasil ditambahkan.")

# Fungsi untuk menampilkan daftar obat
def tampilkan_daftar_obat():
    print("=== Daftar Obat ===")
    data = baca_data_obat()
    if not data:
        print("Tidak ada data obat.")
        return
    print(tabulate(data, headers="keys", tablefmt="grid"))

# Fungsi untuk menghapus obat
def hapus_obat():
    print("=== Menghapus Obat ===")
    nama_obat = input("Masukkan nama obat yang akan dihapus: ")
    data = baca_data_obat()
    data_baru = [obat for obat in data if obat["Nama Obat"].lower() != nama_obat.lower()]

    if len(data) == len(data_baru):
        print("Obat tidak ditemukan.")
    else:
        tulis_data_obat(data_baru)
        print(f"Obat '{nama_obat}' berhasil dihapus.")

# Fungsi untuk memperbarui stok otomatis
def pembaruan_stok_otomatis(nama_obat, jumlah_baru):
    data = baca_data_obat()
    for obat in data:
        if obat["Nama Obat"].lower() == nama_obat.lower():
            obat["Jumlah"] = jumlah_baru
            tulis_data_obat(data)
            print(f"Stok obat '{nama_obat}' berhasil diperbarui.")
            return
    print("Obat tidak ditemukan.")

# Fungsi untuk pemberitahuan stok habis
def cek_stok_habis():
    print("=== Pemberitahuan Stok Habis ===")
    data = baca_data_obat()
    habis = [obat for obat in data if int(obat["Jumlah"]) == 0]
    if not habis:
        print("Semua stok obat tersedia.")
    else:
        print("Obat yang stoknya habis:")
        print(tabulate(habis, headers="keys", tablefmt="grid"))

# Fungsi untuk menampilkan menu
def tampilan_menu_obat():
    print("\n=== Menu Kelola Data Obat ===")
    print(tabulate([
        ["1", "Tambah Obat"],
        ["2", "Hapus Obat"],
        ["3", "Tampilkan Daftar Obat"],
        ["4", "Pembaruan Stok Obat"],
        ["5", "Cek Stok Habis"],
        ["6", "Keluar"]
    ], headers=["No", "Submenu"], tablefmt="grid"))

# Fungsi utama untuk kelola data obat
def kelola_data_obat():
    while True:
        tampilan_menu_obat()
        pilihan = input("Pilih submenu (1-6): ")
        if pilihan == '1':
            tambah_obat()
        elif pilihan == '2':
            hapus_obat()
        elif pilihan == '3':
            tampilkan_daftar_obat()
        elif pilihan == '4':
            nama_obat = input("Masukkan nama obat: ")
            jumlah_baru = input("Masukkan jumlah stok baru: ")
            if not jumlah_baru.isdigit():
                print("Jumlah harus berupa angka!")
                continue
            pembaruan_stok_otomatis(nama_obat, int(jumlah_baru))
        elif pilihan == '5':
            cek_stok_habis()
        elif pilihan == '6':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid!")

# Menjalankan program
if __name__ == "__main__":
    kelola_data_obat()
