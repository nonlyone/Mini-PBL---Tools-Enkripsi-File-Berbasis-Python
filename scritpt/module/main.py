import platform
import os
import sys
import time

def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("--- SECURE VAULT SYSTEM BOOTLOADER ---")
    print("[INIT] Memeriksa kompatibilitas sistem...")
    time.sleep(1)

    # =================== Deteksi Sistem Operasi User ===================
    os_type = platform.system()
    print(f"[INFO] Sistem Operasi Terdeteksi: {os_type}")

    # =================== Logika Pemilihan InterfaceS ===================
    # Prioritas: GUI (Windows) -> CLI (Linux/Mac atau jika GUI Error)


    # =================== JIKA OS USER ITU WINDOWS ===================
    if os_type == "Windows":
        print("[INFO] Memuat tampilan...")
        try:
            
            import gui_app 
            app = gui_app.AplikasiVault()
            app.mainloop()

          # =================== KALAU ERROR KARENA TIDAK ADA LIBRARY CUSTOMTINKER ===================   
        except ImportError as e:
            
            print(f"\n[WARNING] Library GUI kurang lengkap ({e}).")
            print("[ACTION] Mengalihkan ke Mode CLI (Mode Terminal).")
            time.sleep(2)
            masuk_mode_cli()

         # =================== FALLBACK KE TERMINAL KALAU GUINYA ERROR  ===================    
        except Exception as e:
            print(f"\n[CRITICAL ERROR] GUI Gagal: {e}")
            print("[ACTION] Fallback ke CLI.")
            masuk_mode_cli()
            
# =================== JIKA KEDETECT SEBAGAI USER OS NON WINDOWS  ===================   
    else:
        # Linux / MacOS / Server
        print("[INFO] Non-Windows Environment. Masuk ke Mode Terminal.")
        masuk_mode_cli()

# =================== UNTUK MASUK KE TERMINAL ATAU MEMANGGIL cli_app.py  =================== 
def masuk_mode_cli():
    try:
        import cli_app
        cli_app.run_cli()
    except ImportError:
        print("\n[FATAL] File 'cli_app.py' atau 'engine.py' hilang!")
        input("Tekan Enter untuk keluar...")
    except KeyboardInterrupt:
        print("\n[EXIT] Program dimatikan user.")
        sys.exit()

if __name__ == "__main__":
    main()