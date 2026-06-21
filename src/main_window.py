from tkinter import Tk, Frame, Entry, Button, Toplevel, Label, messagebox
from tkinter.ttk import Treeview
from src.services import fetch_employees, add_employee, update_employee, delete_employee


def main_window():
    global tree, entry_text

    def refresh():
        tree.delete(*tree.get_children())
        for user in fetch_employees():
            tree.insert("", "end", values=user)

    def search():
        tree.delete(*tree.get_children())
        users = fetch_employees()
        search_value = entry_text.get().lower()

        if search_value == "refresh()":
            refresh()
            return

        for user in users:
            user_text = " ".join(map(str, user)).lower()
            if search_value in user_text:
                tree.insert("", "end", values=user)

    def sort_column(tree_widget, col, reverse):
        data = [(tree_widget.set(child, col), child) for child in tree_widget.get_children("")]
        data.sort(reverse=reverse)
        for index, (val, child) in enumerate(data):
            tree_widget.move(child, "", index)
        tree_widget.heading(col, command=lambda: sort_column(tree_widget, col, not reverse))

    def open_add_window():
        add_window = Toplevel(root)
        add_window.title("Добавление сотрудника")
        add_window.geometry("500x500")

        fields = {}
        labels = ["Name", "Surname", "ThirdName", "Age", "Sex", "DateAdm", "Position", "Department", "PhoneNumber", "EMail", "Head", "Photo"]
        for i, label_text in enumerate(labels):
            Label(add_window, text=label_text).grid(row=i, column=0, sticky="w", padx=10, pady=4)
            e = Entry(add_window, width=40)
            e.grid(row=i, column=1, padx=10, pady=4)
            fields[label_text] = e

        def save():
            data = [fields[k].get().strip() for k in labels]
            if any(v == "" for v in data[:-1]):
                messagebox.showwarning("Ошибка", "Заполните все обязательные поля!")
                return
            photo_value = data[-1]
            photo_value = f"photo/{photo_value}" if photo_value else None
            add_employee((*data[:-1], photo_value))
            add_window.destroy()
            refresh()

        Button(add_window, text="Сохранить", command=save).grid(row=len(labels), column=0, columnspan=2, pady=15)

    def on_item_click(event):
        selected_item = tree.focus()
        item_values = tree.item(selected_item)
        if not item_values.get("values"):
            return

        emp_id = item_values["values"][0]
        edit_window = Toplevel(root)
        edit_window.title("Карточка сотрудника")
        edit_window.geometry("700x500")

        labels = ["Name", "Surname", "ThirdName", "Age", "Sex", "DateAdm", "Position", "Department", "PhoneNumber", "EMail", "Head", "Photo"]
        entries = {}

        row = fetch_one(emp_id)
        for i, label_text in enumerate(labels):
            Label(edit_window, text=label_text).grid(row=i, column=0, sticky="w", padx=10, pady=4)
            entry = Entry(edit_window, width=45)
            entry.grid(row=i, column=1, padx=10, pady=4)
            entry.insert(0, "" if row[i] is None else row[i])
            entries[label_text] = entry

        def save_changes():
            data = [entries[k].get().strip() for k in labels]
            if any(v == "" for v in data[:-1]):
                messagebox.showwarning("Ошибка", "Заполните все обязательные поля!")
                return
            photo_value = data[-1]
            photo_value = f"photo/{photo_value}" if photo_value else None
            update_employee(emp_id, (*data[:-1], photo_value))
            edit_window.destroy()
            refresh()

        Button(edit_window, text="Сохранить изменения", command=save_changes).grid(
            row=len(labels), column=0, columnspan=2, pady=15
        )

    def fetch_one(emp_id):
        for row in fetch_employees():
            if row[0] == emp_id:
                return row[1:]
        return ("",) * 12

    def open_delete_window():
        del_window = Toplevel(root)
        del_window.geometry("650x300")
        del_window.title("Удаление сотрудника")

        Label(del_window, text="ID сотрудника").pack(anchor="w", padx=20, pady=(20, 0))
        entry_del = Entry(del_window)
        entry_del.pack(anchor="w", padx=20)

        Label(del_window, text="Причина удаления").pack(anchor="w", padx=20, pady=(10, 0))
        entry_prichina = Entry(del_window)
        entry_prichina.pack(anchor="w", padx=20)

        Label(del_window, text="Дата").pack(anchor="w", padx=20, pady=(10, 0))
        entry_dateu = Entry(del_window)
        entry_dateu.pack(anchor="w", padx=20)

        def del_exec():
            em_id = entry_del.get().strip()
            em_prichina = entry_prichina.get().strip()
            em_date = entry_dateu.get().strip()

            if not em_id or not em_prichina or not em_date:
                messagebox.showwarning("Ошибка", "Заполните все поля!")
                return

            delete_employee(em_id, em_prichina, em_date)
            del_window.destroy()
            refresh()

        Button(del_window, text="Удалить", command=del_exec).pack(anchor="w", padx=20, pady=15)

    root = Tk()
    root.title("Employee44 | Учет сотрудников")
    root.geometry("1400x700")

    top = Frame(root)
    top.pack(fill="x", padx=10, pady=10)

    entry_text = Entry(top, width=40)
    entry_text.pack(side="left", padx=(0, 10))
    Button(top, text="Поиск", command=search).pack(side="left", padx=5)
    Button(top, text="Обновить", command=refresh).pack(side="left", padx=5)
    Button(top, text="Добавить", command=open_add_window).pack(side="left", padx=5)
    Button(top, text="Удалить", command=open_delete_window).pack(side="left", padx=5)

    columns = ("id", "Name", "Surname", "ThirdName", "Age", "Sex", "DateAdm", "Position",
               "Department", "PhoneNumber", "EMail", "Head", "Photo")

    tree = Treeview(root, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col, command=lambda c=col: sort_column(tree, c, False))
        tree.column(col, width=110, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    tree.bind("<Double-1>", on_item_click)

    refresh()
    root.mainloop()
