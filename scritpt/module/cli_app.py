import engine
import os
import sys
import time

# =================== AUTENTIKASI CLI SAJA BUAT DEMO ===================

PASSWORD_SESI = "admin123" 

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_banner():
    
    print(r"""
  .----------------------.
  | ______     ______  _ |
  |/ ___\ \   / /  _ \/ ||
  |\___ \\ \ / /| |_) | ||
  | ___) |\ V / |  _ <| ||
  ||____/  \_/  |_| \_\_||
  '----------------------'
    -- SECURE VAULT CLI V1.0 --
    """)

def login_dulu():
    clear_screen()
    show_banner()
    print("[SECURITY CHECK] Sistem terkunci.")
    print("[HINT] Password Demo: admin123") 
    print("-" * 30)

    tries = 0
    while tries < 3:
        pwd = input("Masukkan Password Akses: ")
        if pwd == PASSWORD_SESI:
            print("Akses Diterima! Memuat sistem...")
            time.sleep(1) # Efek loading
            return True
        else:
            tries += 1
            print(f"[AKSES DITOLAK] Sisa percobaan: {3-tries}")
    
    print("Sistem menghentikan paksa koneksi...")
    sys.exit()

# =================== FUNGSI BUAT INPUT FILE DENGAN FITUR CLEAN PATH ===================
def get_file_path():
    print("\n[INPUT] Drag & Drop / Paste path file ke sini lalu tekan Enter:")
    path = input(">> ").strip()
    
    clean_path = path.replace('&', '').replace('"', '').replace("'", "").strip()
    
    return clean_path

# =================== KALAU JALAN DI TERMINAL ===================
def run_cli():
    login_dulu()

    while True:
        clear_screen()
        show_banner()
        print(f"Status Engine: {os.getcwd()}")
        print("-" * 40)
        print("[1] BUAT KUNCI BARU (Reset System)")
        print("[2] KUNCI FILE (Encrypt)")
        print("[3] BUKA FILE (Decrypt)")
        print("[0] KELUAR")
        print("-" * 40)
        
        # TES
        choice = input("root@secure-vault:~# ")

        if choice == '1':
            print("\n[WARNING] Membuat kunci baru akan membuat file lama TIDAK BISA DIBUKA selamanya.")
            confirm = input("Ketik 'SETUJU' untuk lanjut: ")
            if confirm == 'SETUJU':
                engine.buat_kunci()
            else:
                print("[BATAL] Operasi dibatalkan.")
            input("\n[Enter] untuk kembali...")

        elif choice == '2':
            print("\n--- PROTOKOL ENKRIPSI ---")
            target = get_file_path()
            
            if os.path.exists(target):
                if target.endswith(".exe") or target.endswith(".dll"):
                    print("[SYSTEM ERROR] File sistem (exe/dll) dilarang dienkripsi demi keamanan OS!")
                else:
                    sukses = engine.enkripsi_file(target)
                    if sukses:
                        print(f"Log: Enkripsi {target} selesai.")
            else:
                print(f"[ERROR 404] File tidak ditemukan di jalur tersebut.")
            
            input("\n[Enter] untuk kembali...")

        elif choice == '3':
            print("\n--- PROTOKOL DEKRIPSI ---")
            target = get_file_path()
            if os.path.exists(target):
                sukses = engine.dekripsi_file(target)
                if sukses:
                    print(f"Log: Dekripsi {target} selesai.")
            else:
                print(f"[ERROR 404] File tidak ditemukan.")
            input("\n[Enter] untuk kembali...")

        elif choice == '0':
            print("Menutup koneksi aman...")
            time.sleep(0.5)
            sys.exit()
        
        else:
            print("[COMMAND INVALID] Perintah tidak dikenali.")
            time.sleep(1)

if __name__ == "__main__":
    try:
        run_cli()
    except KeyboardInterrupt:
        # Menangani CTRL+C biar errornya gak jelek
        print("\n\n[FORCE QUIT] Program dihentikan paksa.")