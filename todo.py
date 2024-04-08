import tkinter as tk
from tkinter import messagebox


import mysql.connector

def add_todo():
    todo_id = todo_id_entry.get()
    todo_name = todo_name_entry.get()
    todo_task = todo_task_entry.get()

    try:
        todo_id = int(todo_id)
    except ValueError:
        messagebox.showerror("Error", "TODO ID must be an integer!")
        return

    if todo_id < 0:
        messagebox.showerror("Error", "TODO ID cannot be negative!")
        return

    mydb = mysql.connector.connect(
        host="localhost",
        user=" root",
        password="new_password",
        database="todo"
    )
    
    cursor = mydb.cursor()
      
    sql = "INSERT INTO todoapp (todo_id, todo_name, todo_task) VALUES (%s, %s, %s)"
    val = (todo_id, todo_name, todo_task)

    try:
        cursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "TODO added successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

    mydb.close()

    todo_id_entry.delete(0, tk.END)
    todo_name_entry.delete(0, tk.END)
    todo_task_entry.delete(0, tk.END)



def delete_todo():
    todo_id = todo_id_entry.get()
    
    try:
        todo_id = int(todo_id)
    except ValueError:
        messagebox.showerror("Error", "TODO ID must be an integer!")
        return

    if todo_id < 0:
        messagebox.showerror("Error", "TODO ID cannot be negative!")
        return


    mydb = mysql.connector.connect(
        host="localhost",
        user=" root",
        password="new_password",
        database="todo"
    )

    cursor = mydb.cursor()

    sql = "DELETE FROM todoapp WHERE todo_id = %s"
    val = (todo_id,)

    try:
        cursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "TODO deleted successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

    mydb.close()

    todo_id_entry.delete(0, tk.END)

def update_todo():
    todo_id = todo_id_entry.get()
    todo_name = todo_name_entry.get()
    todo_task = todo_task_entry.get()


    try:
        todo_id = int(todo_id)
    except ValueError:
        messagebox.showerror("Error", "TODO ID must be an integer!")
        return

    if todo_id < 0:
        messagebox.showerror("Error", "TODO ID cannot be negative!")
        return


    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="new_password",
        database="todo"
    )

    cursor = mydb.cursor()

    sql = "UPDATE todoapp SET todo_name = %s, todo_task = %s WHERE todo_id = %s"
    val = (todo_name, todo_task, todo_id)

    try:
        cursor.execute(sql, val)
        mydb.commit()
        messagebox.showinfo("Success", "TODO updated successfully!")
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error: {err}")

    mydb.close()

    todo_id_entry.delete(0, tk.END)
    todo_name_entry.delete(0, tk.END)
    todo_task_entry.delete(0, tk.END)

def select_todo():
    todo_id = todo_id_entry.get()

    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="new_password",
        database="todo"
    )

    cursor = mydb.cursor()

    if todo_id == "*":
        sql = "SELECT * FROM todoapp"
        cursor.execute(sql)
        results = cursor.fetchall()
        
        if results:
            todo_details = ""
            for result in results:
                todo_details += f"TODO ID: {result[0]}\nTODO Name: {result[1]}\nTODO Task: {result[2]}\n\n"
            messagebox.showinfo("All TODOs", todo_details)
        else:
            messagebox.showinfo("Error", "No TODOs found.")
    else:
        
        try:
            todo_id = int(todo_id)
        except ValueError:
            messagebox.showerror("Error", "TODO ID must be an integer!")
            return

        sql = "SELECT * FROM todoapp WHERE todo_id = %s"
        val = (todo_id,)

        cursor.execute(sql, val)
        result = cursor.fetchone()

        if result:
            messagebox.showinfo("TODO Details", f"TODO ID: {result[0]}\nTODO Name: {result[1]}\nTODO Task: {result[2]}")
        else:
            messagebox.showinfo("Error", "TODO not found.")

    mydb.close()


root = tk.Tk()
root.title("TODO App")

frame = tk.Frame(root)
frame.pack(padx=16, pady=16)

tk.Label(frame, text="TODO ID:").grid(row=0, column=0, padx=5, pady=5)
tk.Label(frame, text="TODO Name:").grid(row=1, column=0, padx=5, pady=5)
tk.Label(frame, text="TODO Task:").grid(row=2, column=0, padx=5, pady=5)

todo_id_entry = tk.Entry(frame)
todo_id_entry.grid(row=0, column=1, padx=5, pady=5)
todo_name_entry = tk.Entry(frame)
todo_name_entry.grid(row=1, column=1, padx=5, pady=5)
todo_task_entry = tk.Entry(frame)
todo_task_entry.grid(row=2, column=1, padx=5, pady=5)

add_button = tk.Button(frame, text="Add TODO", command=add_todo)
add_button.grid(row=3, column=0, columnspan=2, pady=5)

delete_button = tk.Button(frame, text="Delete TODO", command=delete_todo)
delete_button.grid(row=4, column=0, columnspan=2, pady=5)

update_button = tk.Button(frame, text="Update TODO", command=update_todo)
update_button.grid(row=5, column=0, columnspan=2, pady=5)

select_button = tk.Button(frame, text="Select TODO", command=select_todo)
select_button.grid(row=6, column=0, columnspan=2, pady=5)

root.mainloop()