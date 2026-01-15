import os
import time
from cryptography.fernet import Fernet


FILE_SIGNATURE = b'RKS1' 

# =================== GENERATE KUNCI FERNET ==================
def buat_kunci():
    print("Sedang generate kunci rahasia...", end="")
    time.sleep(1) 
    
    kunci = Fernet.generate_key()
     
    # =================== SIMPAN FILE KUNCI FERNET ===================
    with open("kunci_rahasia.key", "wb") as f:
        f.write(kunci)
    
    print(" [BERHASIL DIBUAT]")
    print("WARNING: Jangan hapus file 'kunci_rahasia.key' atau datamu hilang selamanya!")

# =================== CEK KUNCI ADA ATAU ENGGA ===================
def ambil_kunci():
    if not os.path.exists("kunci_rahasia.key"):
        print("[!] Gawat, file 'kunci_rahasia.key' gak ketemu!")
        return None
    
    return open("kunci_rahasia.key", "rb").read()

def delay(pesan):

    print(f"{pesan} ", end="")
    for i in range(5):
        print(".", end="", flush=True)
        time.sleep(0.5)
    print(" OK")

# =================== PROSES ENKRIPSI FILE ===================
def enkripsi_file(file_asli):
    kunci = ambil_kunci()
    if not kunci:
        return False
        
    cipher = Fernet(kunci)
    
    try:
        # Baca file asli
        with open(file_asli, "rb") as f:
            data_asli = f.read()
            
        delay("Lagi Mengenkripsi File Kamu")      
        data_acak = cipher.encrypt(data_asli)
        data_enkripsi = FILE_SIGNATURE + data_acak
        
        # Simpan file enkripsi (.enc)
        file_enkripsi = file_asli + ".enc"
        with open(file_enkripsi, "wb") as f:
            f.write(data_enkripsi)
            
        print(f"[INFO] File aman! Disimpan sebagai: {file_enkripsi}")
        
        # Hapus file asli (Opsional)
        os.remove(file_asli) 
        return True
        
    except FileNotFoundError:
        print("[ERROR] File yang mau dienkripsi gak ada bray!.")
        return False
    except Exception as e:
        print(f"[ERROR] Waduh error: {e}")
        return False
    
    # =================== PROSES DESKRIPSI FILE ENKRIPSI ===================

def dekripsi_file(file_asli):
    kunci = ambil_kunci()
    if not kunci:
        return False
        
    cipher = Fernet(kunci)
    
    try:
        with open(file_asli, "rb") as f:
            isi_file = f.read()
            
        # =================== MENGECEK / VALIDASI MAGIC BYTES =================== 
        if not isi_file.startswith(FILE_SIGNATURE):
            print("[ALERT] Ini bukan file hasil enkripsi RKS1 / Tools ini!.")
            return False
            
        data_murni_acak = isi_file[len(FILE_SIGNATURE):]
        
        delay("Sedang memulihkan file kamu")
        data_asli = cipher.decrypt(data_murni_acak)
        
        # Balikin ke file aseli
        if file_asli.endswith(".enc"):
            file_deskipsi = file_asli[:-4]
        else:
            file_deskipsi = "hasil_buka_" + file_asli         
        with open(file_deskipsi, "wb") as f:
            f.write(data_asli)
            
        print(f"[INFO] Berhasil dibuka! Kembali menjadi: {file_deskipsi}")
        return True
        
    except Exception as e:
        print(f"[ERROR] Gagal buka kunci. Kuncinya salah atau file rusak.")
        # print(e)
        return False

# =================== TEMPAT TES KODINGAN ===================
if __name__ == "__main__":
    print("--- DEBUG MODE: ENGINE ---")
    
    # Coba bikin kunci
    # buat_kunci() 
    
    # Tes Enkripsi
    # enkripsi_file("target.txt")
    
    # Tes Dekripsi
    # dekripsi_file("target.txt.enc")