from tkinter import Tk, Label, Entry, Button, messagebox
from src.main_window import main_window


def open_auth():
    def auth():
        entered_login = login_entry.get()
        entered_password = password_entry.get()

        if entered_login == "admin" and entered_password == "12345":
            login_window.destroy()
            main_window()
        else:
            messagebox.showwarning("Ошибка", "Неправильный логин или пароль!")

    login_window = Tk()
    login_window.geometry("320x240")
    login_window.title("Employee44 | Авторизация")

    Label(login_window, text="Логин").pack(anchor="w", padx=20, pady=(20, 0))
    login_entry = Entry(login_window)
    login_entry.pack(anchor="w", padx=20)

    Label(login_window, text="Пароль").pack(anchor="w", padx=20, pady=(10, 0))
    password_entry = Entry(login_window, show="*")
    password_entry.pack(anchor="w", padx=20)

    Button(login_window, text="Войти", command=auth).pack(anchor="w", padx=20, pady=15)
    login_window.mainloop()
