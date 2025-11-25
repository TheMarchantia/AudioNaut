import sys
import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import os
from PIL import Image, ImageTk

# Paths
SCRIPT_PATH = "Voice_Commands.py"
MANUAL_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "gaming manual.png")
LIBRARY_BG_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "Library BG.png")
BG_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "UI BG.png")
TEXTBOX_BG_IMAGE_PATH = os.path.join(os.path.dirname(__file__), "TEXTBOX BG.png")

class VoiceControlUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Voice Control Gaming")
        self.root.geometry("800x600")
        self.root.state('zoomed')
        self.root.configure(bg="black")

        self.bg_label = tk.Label(self.root)
        self.bg_label.place(relwidth=1, relheight=1)

        self.update_bg()
        self.process = None
        self.selected_button = None

        self.main_menu()

    def update_bg(self):
        try:
            bg_image = Image.open(BG_IMAGE_PATH)
            bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.bg_label.config(image=self.bg_photo)
        except Exception as e:
            print("Error loading background image:", e)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            if widget != self.bg_label:
                widget.destroy()

    def main_menu(self):
        self.clear_screen()
        self.create_button("Start Gaming", self.start_script, 0.5, 0.4)
        self.create_button("Commands Manual", self.show_manual, 0.5, 0.5)
        self.create_button("Exit", self.root.quit, 0.5, 0.6)


    def show_manual(self):
        self.clear_screen()
        self.update_bg()
        try:
            img = Image.open(MANUAL_IMAGE_PATH)
            img = img.resize((900, 625), Image.Resampling.LANCZOS)
            self.manual_img = ImageTk.PhotoImage(img)
            tk.Label(self.root, image=self.manual_img, bg="black").place(relx=0.5, rely=0.4, anchor="center")
        except Exception as e:
            print("Error loading manual image:", e)
        self.create_button("Back", self.main_menu, 0.5, 0.8)

    
    def create_button(self, text, command, x, y):
        btn = tk.Button(self.root, text=text, font=("Comic Sans MS", 14, "bold"), bg="#FFDE59", fg="#000",
                        padx=20, pady=10, relief="ridge", bd=4, command=lambda: self.on_button_click(btn, command), width=20)
        btn.bind("<Enter>", lambda e: btn.config(bg="#FFA500"))
        btn.bind("<Leave>", lambda e: self.update_button_color(btn))
        btn.place(relx=x, rely=y, anchor="center")
        return btn

    def create_rounded_button(self, text, command, x, y):
        btn = tk.Button(self.root, text=text, font=("Comic Sans MS", 14, "bold"), bg="#8CFF9E", fg="#000",
                        padx=20, pady=10, relief="ridge", bd=4, command=lambda: self.on_button_click(btn, command), width=20)
        btn.bind("<Enter>", lambda e: btn.config(bg="#6FE48E"))
        btn.bind("<Leave>", lambda e: self.update_button_color(btn))
        btn.place(relx=x, rely=y, anchor="center")
        return btn

    def on_button_click(self, btn, command):
        btn.config(bg="#FFA500" if btn["bg"] == "#FFDE59" else "#6FE48E")
        self.selected_button = btn
        command()


    def update_button_color(self, btn):
        if btn != self.selected_button:
            btn.config(bg="#FFDE59" if btn["bg"] != "#6FE48E" else "#8CFF9E")

    def start_script(self):
        try:
            self.process = subprocess.Popen(
                 [sys.executable, "-u", SCRIPT_PATH],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            self.create_text_display()
            threading.Thread(target=self.read_output, daemon=True).start()
            self.stop_button.config(text="Stop", command=self.stop_script)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start script: {e}")

    def create_text_display(self):
        self.clear_screen()
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(expand=True, fill=tk.BOTH)

        try:
            textbox_bg_image = Image.open(TEXTBOX_BG_IMAGE_PATH)
            textbox_bg_image = textbox_bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()), Image.Resampling.LANCZOS)
            self.textbox_bg_photo = ImageTk.PhotoImage(textbox_bg_image)
            textbox_bg_label = tk.Label(self.text_frame, image=self.textbox_bg_photo)
            textbox_bg_label.place(relwidth=1, relheight=1)
        except Exception as e:
            print("Error loading TEXTBOX BG.png:", e)

        tk.Label(self.text_frame, text="Recognizing Speech:", font=("Comic Sans MS", 22, "bold"), bg="#8CFF9E", fg="black").pack(pady=5)

        self.text_box = tk.Text(
            self.text_frame,
            height=10,
            width=50,
            bg="white",
            fg="black",
            font=("ManAparajitagal", 20),
            bd=2,
            highlightbackground="black",
            highlightthickness=1
        )
        self.text_box.pack(pady=10)
        self.text_box.config(state=tk.DISABLED)

        self.create_button("Back", self.main_menu, 0.5, 0.75)
        self.stop_button = self.create_button("Stop", self.stop_script, 0.5, 0.85)

    def read_output(self):
        while self.process and self.process.poll() is None:
            output = self.process.stdout.readline()
            if output:
                self.update_text(output.strip())

    def update_text(self, text):
        self.text_box.config(state=tk.NORMAL)
        self.text_box.insert(tk.END, text + "\n")
        self.text_box.see(tk.END)
        self.text_box.config(state=tk.DISABLED)

    def stop_script(self):
        if self.process:
            self.process.terminate()
        
        self.text_box.config(state=tk.NORMAL)
        self.text_box.delete(1.0, tk.END)
        self.text_box.insert(tk.END, "Script stopped.\n")
        self.text_box.config(state=tk.DISABLED)
        self.stop_button.config(text="Start", command=self.start_script)


if __name__ == "__main__":
    root = tk.Tk()
    app = VoiceControlUI(root)
    root.mainloop()  