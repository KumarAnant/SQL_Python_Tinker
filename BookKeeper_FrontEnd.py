'''
Program to stor book records, Title, Author, Year, ISBN Number

User interaction:
View all records
Search an entry
Add an entry
Update entry
Delete
Close
'''
import os
os.chdir('E:/OneDrive/AmateurWork/Python/Udemy/BookKeeper')
import tkinter as TK
import pyodbc
conn_str = (
	        r'Driver={SQL Server};'
	        r'Server=(local);'
	        r'Database=TestDatabase;'
	        r'Trusted_Connection=yes;'
	    )
    
conn = pyodbc.connect(conn_str) 

def connect():
    if conn:
        print("Yes, we are connected.")
        cur = conn.cursor()
        if cur.tables(table='BookKeeper', tableType='TABLE').fetchone():
            print("Table exists")
            rows = cur.fetchall()
            print(rows)
        else:
            cur.execute('''CREATE TABLE {tab}
                        (id INT IDENTITY(1, 1) PRIMARY KEY NOT NULL,
                        title VARCHAR(60) NOT NULL,
                        author VARCHAR(40),
                        year INT,
                        ISBN INT);'''.format(tab="BookKeeper"))
            print ("New table created")
        conn.commit()        

def insert(title, author, year, isbn):
    if conn:
        cur = conn.cursor()
        cur.execute('''INSERT INTO dbo.BookKeeper
                        (title, author, year, ISBN)
                        VALUES(?, ?, ?, ?)
                    ''', (title, author, year, isbn))
        print('One record added')
        conn.commit()

def view():    
    if conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM BookKeeper')
        rows = cur.fetchall()
        return(rows)

def search(title = "", author = "", year = "", isbn = ""):   
    if conn:
        cur = conn.cursor()
        cur.execute('''SELECT * FROM BookKeeper
                        WHERE title = ? OR author = ? OR year = ? OR isbn  = ?
                        ''', (title, author, year, isbn))
        rows = cur.fetchall()
        return(rows)


def delete(id):    
    if conn:
        cur = conn.cursor()
        cur.execute('''DELETE FROM dbo.BookKeeper
                        WHERE id  = ?
                        ''', (id))

def update(id, title, author, year, isbn):
    if conn:
        cur = conn.cursor()
        cur.execute('''UPDATE dbo.BookKeeper
                        SET title = ?, author = ?, year = ?, ISBN = ?
                        WHERE id  = ?
                        ''', (title, author, year, isbn, id))        
        conn.commit()


def get_selected_row(event):
        global selected_id
        index = list_books.curselection()[0]        
        selected_tuple = list_books.get(index)
        print(selected_tuple)
        selected_id = selected_tuple.split(', ')[0][1:]
        e_Title.delete(0, TK.END)
        e_Title.insert(TK.END, selected_tuple.split(', ')[1][1:-1])
        e_Author.delete(0, TK.END)
        e_Author.insert(TK.END, selected_tuple.split(', ')[2][1:-1])
        e_Year.delete(0, TK.END)
        e_Year.insert(TK.END, selected_tuple.split(', ')[3])
        e_ISBN.delete(0, TK.END)
        e_ISBN.insert(TK.END, selected_tuple.split(', ')[4][:-1])
        return(selected_tuple)


def ViewCommand():
    list_books.delete(0, TK.END)
    for row in view():
        list_books.insert(TK.END, row)

def search_command():
    list_books.delete(0, TK.END)
    for row in search(title=title_text.get(), 
                                            author=author_text.get(),
                                            year=year_text.get(),
                                            isbn=ISBN_text.get()
                                            ):
        list_books.insert(TK.END, row)

def add_command():
        insert(title=title_text.get(), 
                author=author_text.get(),
                year=year_text.get(),
                isbn=ISBN_text.get())
        list_books.delete(0, TK.END)
        list_books.insert(TK.END, (title_text.get(), 
                                author_text.get(),
                                year_text.get(),
                                ISBN_text.get()))

def delete_command():
        delete(selected_id)

def update_command():
    update(selected_id, title_text.get(), author_text.get(), year_text.get(), ISBN_text.get())

window = TK.Tk()
l_Title = TK.Label(window, text = 'Title')
l_Title.grid(row = 0, column = 0)

l_Auth = TK.Label(window, text = 'Author')
l_Auth.grid(row = 0, column = 2)

l_Year = TK.Label(window, text = 'Year')
l_Year.grid(row = 1, column = 0)

l_ISBN = TK.Label(window, text = 'ISBN')
l_ISBN.grid(row = 1, column = 2)

title_text = TK.StringVar()
e_Title = TK.Entry(window, textvariable = title_text)
e_Title.grid(row = 0, column = 1)

author_text = TK.StringVar()
e_Author = TK.Entry(window, textvariable = author_text)
e_Author.grid(row = 0, column = 3)

year_text = TK.StringVar()
e_Year = TK.Entry(window, textvariable = year_text)
e_Year.grid(row = 1, column = 1)

ISBN_text = TK.StringVar()
e_ISBN = TK.Entry(window, textvariable = ISBN_text)
e_ISBN.grid(row = 1, column = 3)

list_books =  TK.Listbox(window, height = 6, width = 35)
list_books.grid(row = 2, column = 0, columnspan = 2, rowspan = 6)

sb1 = TK.Scrollbar(window)
sb1.grid(row = 2, column = 2, rowspan = 6)

list_books.configure(yscrollcommand = sb1.set)
sb1.configure(command = list_books.yview)

list_books.bind('<<ListboxSelect>>', get_selected_row)

b1 = TK.Button(window, text = 'View All', width = 12, command = ViewCommand)
b1.grid(row = 2, column = 3)

b2 = TK.Button(window, text = 'Search Entry', width = 12, command = search_command)
b2.grid(row = 3, column = 3)

b3 = TK.Button(window, text = 'Add Entry', width = 12, command = add_command)
b3.grid(row = 4, column = 3)

b4 = TK.Button(window, text = 'Update', width = 12, command = update_command)
b4.grid(row = 5, column = 3)

b5 = TK.Button(window, text = 'Delete', width = 12, command = delete_command)
b5.grid(row = 6, column = 3)

b6 = TK.Button(window, text = 'Close', width = 12, command = window.destroy)
b6.grid(row = 7, column = 3)

window.mainloop()
