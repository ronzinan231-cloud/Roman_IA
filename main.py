# Импорт библиотек
import tkinter as tk
from tkinter import messagebox
import requests
import json
import os

# Имя файла для сохранения избранных пользователей
POISK_FILE = 'poisk.json'


class GitHubFinderApp:
    def __init__(self, window):
        self.window = window
        self.window.title("Поиск пользователей GitHub")
        self.window.geometry("400x400")

        self.poisk = self.load_poisk()

        # UI: Поле поиска
        tk.Label(window, text="Введите логин пользователя GitHub:").pack(pady=(10, 0))
        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(window, textvariable=self.search_var, width=40)
        self.search_entry.pack(pady=5)

        # UI: Кнопка поиска
        self.search_btn = tk.Button(window, text="Найти", command=self.search_user)
        self.search_btn.pack(pady=5)

        # UI: Список результатов
        tk.Label(window, text="Результаты поиска:").pack()
        self.results_listbox = tk.Listbox(window, width=50, height=8)
        self.results_listbox.pack(pady=5)

        # UI: Кнопка добавления в избранное
        self.add_fav_btn = tk.Button(window, text="Добавить в избранное", command=self.add_to_poisk)
        self.add_fav_btn.pack(pady=5)

        # UI: Список избранного
        tk.Label(window, text="Избранные пользователи:").pack()
        self.fav_listbox = tk.Listbox(window, width=50, height=8)
        self.fav_listbox.pack(pady=5)
        self.update_fav_listbox()

    def search_user(self):
        query = self.search_var.get().strip()

        # Проверка корректности ввода (поле не должно быть пустым)
        if not query:
            messagebox.showwarning("Ошибка ввода", "Поле поиска не должно быть пустым.")
            return

        try:
            # Использование GitHub API для поиска пользователей
            url = f"https://api.github.com/search/users?q={query}"
            response = requests.get(url)

            if response.status_code == 200:
                data = response.json()
                self.results_listbox.delete(0, tk.END)

                # Отображаем первые 15 результатов
                for item in data.get('items', [])[:15]:
                    self.results_listbox.insert(tk.END, item['login'])

                if not data.get('items'):
                    messagebox.showinfo("Результат", "Пользователи не найдены.")
            else:
                messagebox.showerror("Ошибка API", f"Не удалось выполнить запрос. Код: {response.status_code}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Ошибка сети", f"Произошла ошибка при подключении: {e}")

    def add_to_poisk(self):
        selection = self.results_listbox.curselection()
        if not selection:
            messagebox.showwarning("Внимание!", "Выберите пользователя из списка результатов.")
            return

        username = self.results_listbox.get(selection[0])

        if username not in self.poisk:
            self.poisk.append(username)
            self.save_poisk()
            self.update_fav_listbox()
            messagebox.showinfo("Получилось", f"Пользователь '{username}' добавлен в избранное.")
        else:
            messagebox.showinfo("Информация", "Этот пользователь уже находится в избранном.")

    def load_poisk(self):
        if os.path.exists(POISK_FILE):
            with open(POISK_FILE, 'r', encoding='utf-8') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return []
        return []

    def save_poisk(self):
        with open(POISK_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.poisk, f, indent=4, ensure_ascii=False)

    def update_fav_listbox(self):
        self.fav_listbox.delete(0, tk.END)
        for user in self.poisk:
            self.fav_listbox.insert(tk.END, user)


if __name__ == "__main__":
    window = tk.Tk()
    app = GitHubFinderApp(window)
    window.mainloop()



