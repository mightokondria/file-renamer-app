import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class FileRenamerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # --- Konfigurasi Jendela Utama ---
        self.title("Aplikasi Rename File Universal")
        self.geometry("800x750")
        self.resizable(False, False)

        # --- Gaya untuk Widget ---
        style = ttk.Style(self)
        style.configure("TButton", padding=6, relief="flat", font=("Helvetica", 10))
        style.configure("TLabel", font=("Helvetica", 11))
        style.configure("TEntry", font=("Helvetica", 11))

        # --- Frame Utama ---
        main_frame = ttk.Frame(self, padding="20 20 20 20")
        main_frame.pack(fill="both", expand=True)

        # --- Variabel untuk menyimpan path dan nama baru ---
        self.folder_path = tk.StringVar()
        self.new_prefix = tk.StringVar()

        # --- BAGIAN INPUT ---
        input_frame = ttk.LabelFrame(main_frame, text="Pengaturan", padding="15 15 15 15")
        input_frame.pack(fill="x", pady=(0, 20))
        input_frame.columnconfigure(1, weight=1)

        # 1. Pilih Folder
        ttk.Label(input_frame, text="Folder Target:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        folder_entry = ttk.Entry(input_frame, textvariable=self.folder_path, state="readonly", width=60)
        folder_entry.grid(row=0, column=1, sticky="we", padx=5, pady=5)
        browse_button = ttk.Button(input_frame, text="Pilih Folder...", command=self.select_folder)
        browse_button.grid(row=0, column=2, sticky="e", padx=5, pady=5)

        # 2. Input Nama Baru
        ttk.Label(input_frame, text="Nama Awalan Baru:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        new_name_entry = ttk.Entry(input_frame, textvariable=self.new_prefix, width=60)
        new_name_entry.grid(row=1, column=1, sticky="we", padx=5, pady=5)
        new_name_entry.insert(0, "Contoh: Joko")

        # 3. Tombol Aksi
        rename_button = ttk.Button(main_frame, text="Mulai Rename", command=self.start_rename, style="Accent.TButton")
        style.configure("Accent.TButton", font=("Helvetica", 12, "bold"))
        rename_button.pack(fill="x", ipady=10, pady=(0, 20))

        # --- BAGIAN LOG OUTPUT ---
        log_frame = ttk.LabelFrame(main_frame, text="Log Proses", padding="15 15 15 15")
        log_frame.pack(fill="both", expand=True)

        # --- PERUBAHAN DI SINI ---
        # Mengubah bg (background) menjadi 'black' dan fg (foreground/tulisan) menjadi 'white'
        self.log_text = tk.Text(log_frame, wrap="word", height=20, state="disabled", bg="black", fg="white", insertbackground="white")
        self.log_text.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

    def select_folder(self):
        """Membuka dialog untuk memilih folder dan menyimpannya."""
        path = filedialog.askdirectory(title="Pilih Folder yang berisi file")
        if path:
            self.folder_path.set(path)
            self.log_message(f"Folder dipilih: {path}")

    def log_message(self, message):
        """Menambahkan pesan ke area log."""
        self.log_text.config(state="normal")
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END) # Auto-scroll ke bawah
        self.log_text.config(state="disabled")

    def start_rename(self):
        """Logika utama untuk melakukan proses rename."""
        folder = self.folder_path.get()
        new_name = self.new_prefix.get()

        if not folder:
            messagebox.showerror("Error", "Silakan pilih folder terlebih dahulu!")
            return
        if not new_name or new_name == "Contoh: Joko":
            messagebox.showerror("Error", "Silakan masukkan nama awalan baru!")
            return
        
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state="disabled")

        self.log_message("="*50)
        self.log_message(f"Memulai proses rename di folder: {folder}")
        self.log_message(f"Nama awalan baru: '{new_name}'")
        self.log_message("="*50)

        renamed_count = 0
        skipped_count = 0

        try:
            files_in_directory = os.listdir(folder)
            
            for filename in files_in_directory:
                if os.path.isfile(os.path.join(folder, filename)):
                    if '.' in filename:
                        prefix, separator, suffix = filename.partition('.')
                        new_filename = f"{new_name}{separator}{suffix}"
                        
                        old_path = os.path.join(folder, filename)
                        new_path = os.path.join(folder, new_filename)
                        
                        try:
                            if os.path.exists(new_path):
                                self.log_message(f"[DILEWATI] File tujuan '{new_filename}' sudah ada.")
                                skipped_count += 1
                            else:
                                os.rename(old_path, new_path)
                                self.log_message(f"[BERHASIL] '{filename}' -> '{new_filename}'")
                                renamed_count += 1
                        except OSError as e:
                            self.log_message(f"[GAGAL] Tidak bisa rename '{filename}': {e}")
                            skipped_count += 1
                    else:
                        self.log_message(f"[DILEWATI] '{filename}' tidak mengandung titik.")
                        skipped_count += 1
        
        except FileNotFoundError:
            messagebox.showerror("Error", "Folder tidak ditemukan. Mohon pilih lagi.")
            return
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan tak terduga: {e}")
            return
            
        self.log_message("="*50)
        self.log_message("Proses Selesai.")
        self.log_message(f"Total file diubah: {renamed_count}")
        self.log_message(f"Total file dilewati: {skipped_count}")
        self.log_message("="*50)
        messagebox.showinfo("Selesai", f"Proses rename selesai!\n\nBerhasil: {renamed_count}\nDilewati/Gagal: {skipped_count}")


if __name__ == "__main__":
    app = FileRenamerApp()
    app.mainloop()