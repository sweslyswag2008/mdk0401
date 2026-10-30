import hashlib
import tkinter as tk
from tkinter import messagebox

MAX_ATTEMPTS = 3


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


STAFF = {
    "admin":     {"hash": hash_password("lib2026"),   "role": "Администратор"},
    "librarian": {"hash": hash_password("books123"),  "role": "Библиотекарь"},
}


class LoginWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.attempts_left = MAX_ATTEMPTS
        self.show_password = tk.BooleanVar(value=False)

        root.title("Библиотека — вход")
        root.geometry("380x340")
        root.resizable(False, False)

        tk.Label(root, text="Библиотека", font=("Arial", 18, "bold")).pack(pady=(18, 0))
        tk.Label(root, text="Система учёта книг", fg="#555").pack(pady=(0, 12))

        tk.Label(root, text="Логин:").pack(anchor="w", padx=45)
        self.entry_login = tk.Entry(root, width=32)
        self.entry_login.pack(padx=45, pady=4)
        self.entry_login.focus()

        tk.Label(root, text="Пароль:").pack(anchor="w", padx=45)
        self.entry_password = tk.Entry(root, width=32, show="*")
        self.entry_password.pack(padx=45, pady=4)

        tk.Checkbutton(
            root, text="Показать пароль",
            variable=self.show_password, command=self.toggle_password,
        ).pack(anchor="w", padx=45)

        self.status = tk.Label(root, text=f"Попыток: {self.attempts_left}", fg="#555")
        self.status.pack(pady=(10, 0))

        tk.Button(
            root, text="Войти", width=16, command=self.check_login,
            bg="#2F5D8A", fg="white", activebackground="#244A6E", cursor="hand2",
        ).pack(pady=14)

        root.bind("<Return>", self.check_login)

    def toggle_password(self):
        self.entry_password.config(show="" if self.show_password.get() else "*")

    def check_login(self, event=None):
        login = self.entry_login.get().strip()
        password = self.entry_password.get()

        if not login or not password:
            messagebox.showwarning("Внимание", "Введите логин и пароль.")
            return

        user = STAFF.get(login)
        if user and user["hash"] == hash_password(password):
            messagebox.showinfo("Вход выполнен", f"Здравствуйте, {login}!\nРоль: {user['role']}")
            return

        self.attempts_left -= 1
        if self.attempts_left == 0:
            messagebox.showerror("Доступ закрыт", "Три неудачные попытки. Программа закрывается.")
            self.root.destroy()
            return

        messagebox.showerror("Ошибка", "Неверный логин или пароль.")
        self.status.config(text=f"Попыток: {self.attempts_left}")
        self.entry_password.delete(0, tk.END)
        self.entry_password.focus()


if __name__ == "__main__":
    root = tk.Tk()
    LoginWindow(root)
    root.mainloop()
