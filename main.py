import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading
import os
from erasure_methods import wipe_file_zero_pass, wipe_file_random_pass, wipe_file_dod_three_pass

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class DataWipeApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DataWipe - Secure File Eraser")
        self.geometry("650x400")
        self.file_path = None

        self.label = ctk.CTkLabel(self, text="Select file to erase securely", font=("Arial", 18))
        self.label.pack(pady=20)

        self.select_btn = ctk.CTkButton(self, text="Choose File", command=self.select_file)
        self.select_btn.pack(pady=10)

        self.method_var = ctk.StringVar(value="zero")

        self.radio_zero = ctk.CTkRadioButton(self, text="Zero Pass (1 time overwrite)", variable=self.method_var, value="zero")
        self.radio_zero.pack(pady=2)

        self.radio_random = ctk.CTkRadioButton(self, text="Random Pass (1 time overwrite)", variable=self.method_var, value="random")
        self.radio_random.pack(pady=2)

        self.radio_dod = ctk.CTkRadioButton(self, text="DoD 5220.22-M (3 passes)", variable=self.method_var, value="dod")
        self.radio_dod.pack(pady=2)

        self.progress = ctk.CTkProgressBar(self, width=500)
        self.progress.pack(pady=20)
        self.progress.set(0)

        self.erase_btn = ctk.CTkButton(self, text="Erase Securely", command=self.start_erasure)
        self.erase_btn.pack(pady=10)

    def select_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            messagebox.showinfo("File Selected", f"File selected:\n{self.file_path}")

    def start_erasure(self):
        if not self.file_path:
            messagebox.showerror("Error", "Select a file first!")
            return

        algo = self.method_var.get()
        t = threading.Thread(target=self.erase_file, args=(algo,))
        t.start()

    def erase_file(self, method):
        try:
            self.progress.set(0)

            if method == "zero":
                wipe_file_zero_pass(self.file_path, self.progress)
            elif method == "random":
                wipe_file_random_pass(self.file_path, self.progress)
            else:
                wipe_file_dod_three_pass(self.file_path, self.progress)

            os.remove(self.file_path)
            messagebox.showinfo("Done", "✅ File securely erased!")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = DataWipeApp()
    app.mainloop()
