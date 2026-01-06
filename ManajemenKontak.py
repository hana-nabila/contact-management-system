import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# DATABASE SETUP 
def setup_db():
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS contacts 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       first_name TEXT, middle_name TEXT, last_name TEXT, 
                       gender TEXT, age TEXT, address TEXT, phone TEXT)''')
    conn.commit()
    conn.close()

# FUNGSI LOGIKA
def add_to_db(data, window):
    if data[0] == "" or data[-1] == "":
        messagebox.showwarning("Peringatan", "Nama Depan dan Nomor Telepon wajib diisi!")
        return
    
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO contacts (first_name, middle_name, last_name, gender, age, address, phone) VALUES (?,?,?,?,?,?,?)", data)
    conn.commit()
    conn.close()
    window.destroy()
    refresh_table()

def delete_contact():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Hapus", "Pilih baris yang ingin dihapus")
        return
    
    if messagebox.askyesno("Konfirmasi", "Are You Sure You Want To Delete"):
        for item in selected_item:
            values = tree.item(item, 'values')
            conn = sqlite3.connect("contacts.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM contacts WHERE first_name=? AND phone=?", (values[0], values[6]))
            conn.commit()
            conn.close()
        refresh_table()

def refresh_table():
    for row in tree.get_children():
        tree.delete(row)
    conn = sqlite3.connect("contacts.db")
    cursor = conn.cursor()
    cursor.execute("SELECT first_name, middle_name, last_name, gender, age, address, phone FROM contacts")
    for row in cursor.fetchall():
        tree.insert("", "end", values=row)
    conn.close()

def exit_system():
    if messagebox.askyesno("Contact Management System", "Do you want to exit the system"):
        root.destroy()

# JENDELA TAMBAH KONTAK
def open_add_window():
    add_win = tk.Toplevel(root)
    add_win.title("Contact Details")
    add_win.geometry("400x480")
    add_win.configure(bg="#FFF0F5") 

    # Header Popup 
    tk.Label(add_win, text="🌸 Adding New Contacts 🌸", bg="#FF69B4", fg="white", 
             font=("Arial", 14, "bold"), pady=10).pack(fill="x", pady=(0, 10))

    fields = ["First Name", "Middle Name", "Last Name", "Age", "Home Address", "Phone Number"]
    entries = {}

    for field in fields:
        frame = tk.Frame(add_win, bg="#FFF0F5")
        frame.pack(fill="x", padx=20, pady=5)
        tk.Label(frame, text=field, width=15, anchor="w", bg="#FFF0F5", 
                 font=("Arial", 10, "bold"), fg="#DB7093").pack(side="left")
        entry = tk.Entry(frame, highlightthickness=1, highlightbackground="#FFC0CB")
        entry.pack(side="right", expand=True, fill="x")
        entries[field] = entry

    # Gender Radio Buttons
    gender_var = tk.StringVar(value="Male")
    gender_frame = tk.Frame(add_win, bg="#FFF0F5")
    gender_frame.pack(fill="x", padx=20, pady=5)
    tk.Label(gender_frame, text="Gender", width=15, anchor="w", bg="#FFF0F5", 
             font=("Arial", 10, "bold"), fg="#DB7093").pack(side="left")
    tk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male", bg="#FFF0F5").pack(side="left")
    tk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female", bg="#FFF0F5").pack(side="left")

    def save_action():
        data = (entries["First Name"].get(), entries["Middle Name"].get(), entries["Last Name"].get(),
                gender_var.get(), entries["Age"].get(), entries["Home Address"].get(), entries["Phone Number"].get())
        add_to_db(data, add_win)

    # Tombol Simpan 
    tk.Button(add_win, text="💖 Please Save 💖", bg="#FF69B4", fg="white", 
              command=save_action, font=("Arial", 10, "bold"), width=20, pady=5).pack(pady=20)

# GUI UTAMA 
root = tk.Tk()
root.title("Contact Management System")
root.geometry("950x550")
root.configure(bg="#FFC0CB") 

setup_db()

# Judul Utama 
header = tk.Label(root, text="🎀 Contact System 🎀", font=("Arial", 30, "bold"), 
                  bg="#FF1493", fg="white", bd=5, relief="flat", pady=10)
header.pack(pady=20, fill="x")

# Tabel 
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="white", fieldbackground="white", rowheight=25)
style.configure("Treeview.Heading", background="#FFB6C1", foreground="#DB7093", font=("Arial", 10, "bold"))

tree_frame = tk.Frame(root, bg="#FFC0CB")
tree_frame.pack(padx=20, fill="both", expand=True)

columns = ("First Name", "Middle Name", "Last Name", "Gender", "Age", "Home Address", "phone Number")
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="center")

tree.pack(side="left", fill="both", expand=True)

# Scrollbar
sb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
sb.pack(side="right", fill="y")
tree.config(yscrollcommand=sb.set)

# Tombol Bawah 
btn_frame = tk.Frame(root, bg="#FFC0CB")
btn_frame.pack(pady=30)

def create_btn(txt, color, cmd):
    return tk.Button(btn_frame, text=txt, font=("Arial", 11, "bold"), 
                     bg=color, fg="white", width=18, bd=0, pady=10, 
                     cursor="hand2", command=cmd)

create_btn("✨ Add New ✨", "#FF69B4", open_add_window).pack(side="left", padx=15)
create_btn("🗑️ Delete 🗑️", "#DB7093", delete_contact).pack(side="left", padx=15)
create_btn("🚪 Exit 🚪", "#C71585", exit_system).pack(side="left", padx=15)

refresh_table()
root.mainloop()