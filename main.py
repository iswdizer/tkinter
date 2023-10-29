import tkinter as tk
from tkinter import ttk
import sqlite3

class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = DB()
        self.view_rercods()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0',bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./img/add.png')
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.add_img, command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT)

        self.tree=ttk.Treeview(self, columns=('Id', 'Name', 'tel', 'Email'), height=45, show ='headings')
        self.tree.column('Id', width=30, anchor=tk.CENTER)
        self.tree.column('Name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150,anchor=tk.CENTER)
        self.tree.column('Email',width=150,anchor=tk.CENTER)

        self.tree.heading('Id',text='Id')
        self.tree.heading('Name',text='ФИО')
        self.tree.heading('tel',text='Телефон')
        self.tree.heading('Email',text='E-mail')
         
        self.tree.pack(side=tk.LEFT)

    def open_dialog(self):
        Child()

    def records(self, name, tel, email):
        self.db.insert_data(name, tel, email)
        self.view_rercods()

    def view_rercods(self):
        self.db.cur.execute("select * from db")        
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]
        


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('Добавить')
        self.geometry('400x200')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()

        label_name = tk.Label(self,text='ФИО')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y =80) 
        label_sum = tk.Label(self, text='Email:')
        label_sum.place(x=50, y=110)

        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y=170)
        
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(
                         self.entry_name.get(),
                         self.entry_email.get(),
                         self.entry_tel.get()))
        self.btn_ok.bind('<Button-1>', lambda event: self.destroy(), add='+')
    


class DB:
    def __init__(self):
        self.conn = sqlite3.connect('db.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''create table if not exists db (
            id integer primary key,
            name text,
            email text,
            tel text
            )
        ''')
        self.conn.commit()

    def insert_data(self, name, email, tel):
        self.cur.execute('insert into db (name, email, tel) values (?, ?, ?)', (name, email, tel))
        self.conn.commit()

if __name__ == '__main__':
   root = tk.Tk()
   app = Main(root)
   app.pack()

   root.title('Телефон')
   root.geometry('665x450')
   root.resizable(False, True)
   root.mainloop() 