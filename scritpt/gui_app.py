import customtkinter as ctk
from tkinter import filedialog, messagebox
import engine  
import os
import time

# =================== KONFIGURASI TAMPILAN ===================
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("green") 

class AplikasiVault(ctk.CTk):
    def __init__(self):
        super().__init__()

        # =================== SETUP JENDELA ===================
        self.title("PROJECT Mini - PBL S-VAULT // ENKRIPSI DATA")
        self.geometry("650x450")
        self.resizable(False, False)

        self.path_file_terpilih = None

        # =================== LAYOUTING ===================
        self.grid_columnconfigure(0, weight=1)

        # 1. Header Judul 
        self.lbl_judul = ctk.CTkLabel(self, text="SECURE VAULT SYSTEM v1.0", font=("Consolas", 26, "bold"))
        self.lbl_judul.grid(row=0, column=0, pady=(30, 10))
        
        self.lbl_subjudul = ctk.CTkLabel(self, text="Algoritma: Fernet (AES-128) + Custom Header SVR1", font=("Consolas", 12))
        self.lbl_subjudul.grid(row=1, column=0, pady=(0, 20))

        # 2. Frame Pilih File
        self.frame_file = ctk.CTkFrame(self)
        self.frame_file.grid(row=2, column=0, pady=10, padx=20, sticky="ew")
        
        self.btn_cari = ctk.CTkButton(self.frame_file, text="[1] CARI FILE", command=self.cari_file, font=("Consolas", 14))
        self.btn_cari.grid(row=0, column=0, padx=20, pady=20)
        
        self.lbl_info_file = ctk.CTkLabel(self.frame_file, text="Status: Belum ada file...", text_color="gray", font=("Consolas", 12))
        self.lbl_info_file.grid(row=0, column=1, padx=10)

        # 3. Frame Tombol Eksekusi
        self.frame_aksi = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_aksi.grid(row=3, column=0, pady=20)

        self.btn_enkripsi = ctk.CTkButton(self.frame_aksi, text="[2] KUNCI (ENCRYPT)", 
                                          fg_color="#b30000", hover_color="#800000", # Merah Gelap
                                          width=180, height=40,
                                          font=("Consolas", 14, "bold"),
                                          command=self.aksi_enkripsi)
        self.btn_enkripsi.grid(row=0, column=0, padx=10)

        self.btn_dekripsi = ctk.CTkButton(self.frame_aksi, text="[3] BUKA (DECRYPT)", 
                                          fg_color="#006600", hover_color="#004d00", # Hijau Gelap
                                          width=180, height=40,
                                          font=("Consolas", 14, "bold"),
                                          command=self.aksi_dekripsi)
        self.btn_dekripsi.grid(row=0, column=1, padx=10)

        # 4. Status proses
        self.lbl_status = ctk.CTkLabel(self, text="JALANKAN PROGRAM", font=("Consolas", 16), text_color="#00ff00")
        self.lbl_status.grid(row=4, column=0, pady=20)

        # 5. Footer / Tombol Bahaya
        self.btn_reset = ctk.CTkButton(self, text="⚠ RESET KEY SYSTEM ⚠", 
                                       fg_color="transparent", border_width=1, border_color="gray", text_color="gray",
                                       hover_color="#333333",
                                       command=self.aksi_reset_key)
        self.btn_reset.grid(row=5, column=0, pady=30)

    # =================== LOGIKA PROGRAM ===================
    
    def cari_file(self):
        filename = filedialog.askopenfilename()
        if filename:
            self.path_file_terpilih = filename
            nama_singkat = os.path.basename(filename)
            self.lbl_info_file.configure(text=f"Target: {nama_singkat}", text_color="white")
            self.lbl_status.configure(text="FILE TERDETEKSI", text_color="cyan")

    def aksi_enkripsi(self):
        if not self.path_file_terpilih:
            messagebox.showwarning("Peringatan", "Pilih file kamu dulu!")
            return
        
        self.lbl_status.configure(text="ENCRYPTING... (Tunggu)", text_color="yellow")
        self.update()
        
        # =================== Panggil Engine ===================
        hasil = engine.enkripsi_file(self.path_file_terpilih)
        
        if hasil:
            self.lbl_status.configure(text="ENKRIPSI SUKSES!", text_color="#00ff00")
            self.path_file_terpilih = None # Reset
            self.lbl_info_file.configure(text="Target: -", text_color="gray")
            messagebox.showinfo("Berhasil", "File aman! Cek file berekstensi .enc")
        else:
            self.lbl_status.configure(text="GAGAL! Cek Terminal.", text_color="red")

    def aksi_dekripsi(self):
        if not self.path_file_terpilih:
            messagebox.showwarning("Peringatan", "Pilih file kamu dulu!")
            return
            
        self.lbl_status.configure(text="DECRYPTING... (Tunggu)", text_color="yellow")
        self.update() 
        
        hasil = engine.dekripsi_file(self.path_file_terpilih)
        
        if hasil:
            self.lbl_status.configure(text="DEKRIPSI SUKSES!", text_color="#00ff00")
            self.path_file_terpilih = None
            self.lbl_info_file.configure(text="Target: -", text_color="gray")
            messagebox.showinfo("Berhasil", "File kembali normal!")
        else:
            self.lbl_status.configure(text="GAGAL! Kunci Salah atau terhapus", text_color="red")

    def aksi_reset_key(self):
        jawaban = messagebox.askyesno("WARNING INFO", "Yakin mau reset kunci?\nSemua file lama GAK BAKAL BISA DIBUKA lagi!")
        if jawaban:
            engine.buat_kunci()
            self.lbl_status.configure(text="KEY BARU DIGENERATE", text_color="orange")
            messagebox.showinfo("Info", "Kunci baru telah dibuat.")

if __name__ == "__main__":
    app = AplikasiVault()
    app.mainloop()