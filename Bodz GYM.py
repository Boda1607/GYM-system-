import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3


conn = sqlite3.connect('gym_management.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS members
        (  id INTEGER PRIMARY KEY, name TEXT, contact TEXT, membership_type TEXT, payment_method TEXT, start_date TEXT, end_date TEXT, coach_id INTEGER,
             FOREIGN KEY(coach_id) REFERENCES coaches(id))''')

c.execute('''CREATE TABLE IF NOT EXISTS coaches
             (id INTEGER PRIMARY KEY, name TEXT, contact TEXT)''')

# Functions
def add_member():
    def save():
        name = name_entry.get()
        contact = contact_entry.get()
        membership_type = membership_type_var.get()
        payment_method = payment_method_var.get()
        start_date = start_date_entry.get()
        end_date = end_date_entry.get()
        coach_id = coach_var.get()

        c.execute("INSERT INTO members VALUES (NULL, ?, ?, ?, ?, ?, ?, ?)",
                   (name, contact, membership_type, payment_method, start_date, end_date, coach_id))
        conn.commit()
        messagebox.showinfo('Success', 'Member added successfully')

    top = tk.Toplevel(root)
    top.title('Add Me')
    top.configure(bg='gray10')
    #top.geometry("330x300")
    name_label = tk.Label(top, text='Name')
    name_label.grid(row=0, column=0, pady=2)
    name_entry = tk.Entry(top)
    name_entry.grid(row=0, column=2, pady=2)

    contact_label = tk.Label(top, text='Contact')
    contact_label.grid(row=1, column=0, pady=2)
    contact_entry = tk.Entry(top)
    contact_entry.grid(row=1, column=2, pady=2)

    membership_type_label = tk.Label(top, text='Membership Type')
    membership_type_label.grid(row=2, column=0, pady=1)
    membership_type_var = tk.StringVar()
    membership_type_menu = tk.OptionMenu(top, membership_type_var, 'Gold', 'Silver', 'Bronze')
    membership_type_menu.grid(row=2, column=2, pady=1)

    payment_method_label = tk.Label(top, text='Payment Method')
    payment_method_label.grid(row=3, column=0, pady=1)
    payment_method_var = tk.StringVar()
    payment_method_menu = tk.OptionMenu(top, payment_method_var, 'Credit Card',  'Cash')
    payment_method_menu.grid(row=3, column=2, pady=1)

    start_date_label = tk.Label(top, text='Start Date')
    start_date_label.grid(row=4, column=0, pady=2)
    start_date_entry = tk.Entry(top)
    start_date_entry.grid(row=4, column=2, pady=2)

    end_date_label = tk.Label(top, text='End Date')
    end_date_label.grid(row=5, column=0, pady=2)
    end_date_entry = tk.Entry(top)
    end_date_entry.grid(row=5, column=2, pady=2)

    coach_label = tk.Label(top, text='Coach')
    coach_label.grid(row=6, column=0, pady=2)
    coach_var = tk.StringVar()
    coach_names = [row[1]for row in c.execute("SELECT id, name FROM coaches")]
    coach_menu = tk.OptionMenu(top, coach_var, *coach_names)
    coach_menu.grid(row=6, column=2, pady=2)

    save_button = tk.Button(top, text='Save', command=save)
    save_button.grid(row=7, column=1, pady=10)


def veiw_member():
    members = c.execute('SELECT * FROM members ')
    top = tk.Toplevel(root)
    top.title('View Member')
    top.geometry("860x260")
    top.configure(bg='gray10')
    tree = ttk.Treeview(top)
    tree['columns'] = ('1', '2', '3', '4', '5', '6', '7')
    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('1', anchor=tk.N, width=50)
    tree.column('2', anchor=tk.N, width=50)
    tree.column('3', anchor=tk.N, width=50)
    tree.column('4', anchor=tk.N, width=50)
    tree.column('5', anchor=tk.N, width=50)
    tree.column('6', anchor=tk.N, width=50)
    tree.column('7', anchor=tk.N, width=50)
    tree.heading('1', text='Name')
    tree.heading('2', text='contact')
    tree.heading('3', text='Membership type')
    tree.heading('4', text='payment method')
    tree.heading('5', text='start')
    tree.heading('6', text='end')
    tree.heading('7', text='Coach')

    for member in members:
        tree.insert('', 'end', text=member[0], values=member[1:])
    tree.pack(expand=True, fill='both')


def Add_coach():
    def save():
        name = name_entry.get()
        contact = contact_entry.get()
        c.execute("INSERT INTO coaches VALUES (NULL, ?, ?)",
                (name, contact))
        conn.commit()
        messagebox.showinfo('Success', 'coach added successfully')

    top = tk.Toplevel(root)
    top.title('Add Coach')
    top.geometry("200x100")
    top.configure(bg='gray10')
    name_label = tk.Label(top, text='Name')
    name_label.grid(row=0, column=0, pady=3)
    name_entry = tk.Entry(top)
    name_entry.grid(row=0, column=2, pady=3)

    contact_label = tk.Label(top, text='Number')
    contact_label.grid(row=1, column=0, pady=3)
    contact_entry = tk.Entry(top)
    contact_entry.grid(row=1, column=2, pady=3)

    save_button = tk.Button(top, text='Save', command=save)
    save_button.grid(row=7, column=2, pady=10)




def veiw_coach():
    coaches = c.execute('SELECT * FROM coaches ')
    top = tk.Toplevel(root)
    top.title('view coach')
    top.geometry("400x150")
    tree = ttk.Treeview(top)
    tree['columns'] = ('1', '2', )
    tree.column('#0', width=0, stretch=tk.NO)
    tree.column('1', anchor=tk.N, width=100)
    tree.column('2', anchor=tk.N, width=100)
    tree.heading('1', text='Name')
    tree.heading('2', text='contact')
    for coache in coaches :
        tree.insert('', 'end', text=coache[0], values=coache[1:])
    tree.pack(expand = True, fill='both')





root = tk.Tk()
root.title("Bodz GYM")
root.configure(bg='gray10')
root.geometry("430x200")

Add_member_button = tk.Button(root, text="Add member", command=add_member).pack(pady=10)
Add_coach_button = tk.Button(root, text="Add coach", command=Add_coach).pack(pady=10)
veiw_member_button = tk.Button(root, text="Veiw members", command=veiw_member).pack(pady=10)
veiw_coach_button = tk.Button(root, text="Veiw coach", command=veiw_coach).pack(pady=10)
veiw_coach_button = tk.Button(bg='gray10')

root.mainloop()