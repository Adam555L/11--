import tkinter as tk
from tkinter import messagebox
import json
import os

# ---------- ТЕМЫ ----------
THEMES = {
    "dark": {
        "bg": "#1e1e2e", "panel": "#313244", "list_bg": "#1e1e2e",
        "text": "#cdd6f4", "title": "#89b4fa", "accent": "#89b4fa",
        "accent_text": "#1e1e2e", "theme_text": "#f9e2af",
        "day_title": "#a6e3a1", "btn_bg": "#313244", "btn_text": "#cdd6f4",
        "reset_bg": "#f38ba8", "exit_bg": "#45475a"
    },
    "gray": {
        "bg": "#7a7a7a", "panel": "#a0a0a0", "list_bg": "#e0e0e0",
        "text": "#1e1e1e", "title": "#ffffff", "accent": "#505050",
        "accent_text": "#ffffff", "theme_text": "#2b2b2b",
        "day_title": "#1e1e1e", "btn_bg": "#c0c0c0", "btn_text": "#1e1e1e",
        "reset_bg": "#b04040", "exit_bg": "#909090"
    },
    "light": {
        "bg": "#ffffff", "panel": "#f0f0f0", "list_bg": "#ffffff",
        "text": "#1e1e1e", "title": "#1a73e8", "accent": "#1a73e8",
        "accent_text": "#ffffff", "theme_text": "#b06000",
        "day_title": "#2e7d32", "btn_bg": "#e0e0e0", "btn_text": "#1e1e1e",
        "reset_bg": "#e57373", "exit_bg": "#bdbdbd"
    }
}


class GymPlanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("План тренировок в зале")
        self.root.geometry("780x640")

        self.data_file = "gym_plan.json"
        self.theme_file = "theme.json"
        self.current_theme = self.load_theme()
        self.current_day = "Понедельник"

        # ---------- ДЕФОЛТНЫЙ ПЛАН ----------
        self.default_plan = {
            "Понедельник": {
                "Тема": "Грудь + Трицепс",
                "Упражнения": [
                    "Жим лёжа — 4x8-10",
                    "Жим гантелей на наклонной — 3x10",
                    "Разводка гантелей — 3x12",
                    "Брусья — 3x10",
                    "Французский жим — 3x12",
                    "Разгибания на блоке — 3x15"
                ]
            },
            "Вторник": {
                "Тема": "Спина + Бицепс",
                "Упражнения": [
                    "Становая тяга — 4x6-8",
                    "Подтягивания — 4x8-12",
                    "Тяга штанги в наклоне — 3x10",
                    "Тяга блока к поясу — 3x12",
                    "Подъём штанги на бицепс — 4x10",
                    "Молотки с гантелями — 3x12"
                ]
            },
            "Среда": {
                "Тема": "Отдых",
                "Упражнения": [
                    "Полный отдых или лёгкое кардио (30 мин)",
                    "Растяжка 15 минут",
                    "Массаж / сауна по желанию"
                ]
            },
            "Четверг": {
                "Тема": "Ноги + Плечи",
                "Упражнения": [
                    "Приседания со штангой — 4x8-10",
                    "Жим ногами — 3x12",
                    "Выпады с гантелями — 3x12",
                    "Румынская тяга — 3x10",
                    "Жим штанги стоя — 4x8-10",
                    "Махи гантелями в стороны — 3x15"
                ]
            },
            "Пятница": {
                "Тема": "Грудь + Спина (суперсеты)",
                "Упражнения": [
                    "Жим лёжа + тяга блока — 4x10",
                    "Жим гантелей + подтягивания — 3x10",
                    "Разводка + тяга гантели — 3x12",
                    "Отжимания на брусьях — 3x12"
                ]
            },
            "Суббота": {
                "Тема": "Руки + Пресс",
                "Упражнения": [
                    "Подъём штанги на бицепс — 4x10",
                    "Французский жим — 4x10",
                    "Молотки — 3x12",
                    "Разгибания на блоке — 3x15",
                    "Скручивания — 4x20",
                    "Планка — 3x60 сек"
                ]
            },
            "Воскресенье": {
                "Тема": "Отдых",
                "Упражнения": [
                    "Полный отдых",
                    "Прогулка 30-60 минут",
                    "Растяжка всего тела"
                ]
            }
        }

        self.plan = self.load_plan()

        # ---------- ВЕРХНЯЯ ПАНЕЛЬ (ТЕМЫ) ----------
        self.top_bar = tk.Frame(root)
        self.top_bar.pack(fill="x", padx=10, pady=(10, 0))

        self.theme_buttons_frame = tk.Frame(self.top_bar)
        self.theme_buttons_frame.pack(side="right")

        tk.Label(self.theme_buttons_frame, text="Тема:").pack(side="left", padx=(0, 5))

        self.theme_buttons = {}
        for key, label, color in [
            ("light", "⚪ Светлая", "#ffffff"),
            ("gray",  "⚫ Серая", "#7a7a7a"),
            ("dark",  "⚫ Чёрная", "#1e1e2e"),
        ]:
            btn = tk.Button(
                self.theme_buttons_frame, text=label,
                font=("Arial", 9), relief="flat", cursor="hand2",
                bg=color,
                fg=("#1e1e1e" if key != "dark" else "#cdd6f4"),
                command=lambda k=key: self.set_theme(k)
            )
            btn.pack(side="left", padx=3)
            self.theme_buttons[key] = btn

        # ---------- ЗАГОЛОВОК ----------
        self.title_label = tk.Label(
            root, text="🏋️ ПЛАН ТРЕНИРОВОК НА НЕДЕЛЮ",
            font=("Arial", 18, "bold")
        )
        self.title_label.pack(pady=15)

        # ---------- ОСНОВНОЙ КОНТЕЙНЕР ----------
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Левая часть — дни недели
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="y", padx=(0, 15))

        self.days_label = tk.Label(
            self.left_frame, text="Дни недели",
            font=("Arial", 12, "bold")
        )
        self.days_label.pack(pady=(0, 10))

        self.day_buttons = {}
        for day in self.plan.keys():
            btn = tk.Button(
                self.left_frame, text=day,
                font=("Arial", 11),
                width=15, anchor="w",
                relief="flat", cursor="hand2",
                command=lambda d=day: self.show_day(d)
            )
            btn.pack(pady=3, fill="x")
            self.day_buttons[day] = btn

        # Правая часть — упражнения
        self.right_frame = tk.Frame(self.main_frame, relief="flat")
        self.right_frame.pack(side="right", fill="both", expand=True)

        self.day_title = tk.Label(self.right_frame, text="", font=("Arial", 16, "bold"))
        self.day_title.pack(pady=(15, 5), anchor="w", padx=20)

        self.day_theme = tk.Label(self.right_frame, text="", font=("Arial", 13, "italic"))
        self.day_theme.pack(pady=(0, 10), anchor="w", padx=20)

        self.ex_list = tk.Listbox(
            self.right_frame,
            font=("Arial", 12),
            relief="flat", bd=0,
            highlightthickness=0,
            activestyle="none"
        )
        self.ex_list.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        # ---------- НИЖНЯЯ ПАНЕЛЬ ----------
        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(fill="x", padx=20, pady=10)

        self.reset_btn = tk.Button(
            self.bottom_frame, text="🔄 Сбросить план",
            font=("Arial", 10),
            relief="flat", cursor="hand2",
            command=self.reset_plan
        )
        self.reset_btn.pack(side="left")

        self.exit_btn = tk.Button(
            self.bottom_frame, text="Выход",
            font=("Arial", 10),
            relief="flat", cursor="hand2",
            command=root.quit
        )
        self.exit_btn.pack(side="right")

        # Применяем тему и показываем первый день
        self.apply_theme()
        self.show_day(list(self.plan.keys())[0])

    # ---------- ДАННЫЕ ----------
    def load_plan(self):
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return self.default_plan
        return self.default_plan

    def save_plan(self):
        try:
            with open(self.data_file, "w", encoding="utf-8") as f:
                json.dump(self.plan, f, ensure_ascii=False, indent=2)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить: {e}")

    # ---------- ПОКАЗ ДНЯ ----------
    def show_day(self, day):
        self.current_day = day
        c = THEMES[self.current_theme]

        for d, btn in self.day_buttons.items():
            if d == day:
                btn.configure(bg=c["accent"], fg=c["accent_text"])
            else:
                btn.configure(bg=c["btn_bg"], fg=c["btn_text"])

        data = self.plan[day]
        self.day_title.configure(text=f"📅 {day}")
        self.day_theme.configure(text=f"Тема: {data['Тема']}")

        self.ex_list.delete(0, tk.END)
        for i, ex in enumerate(data["Упражнения"], 1):
            self.ex_list.insert(tk.END, f"  {i}. {ex}")

    # ---------- СБРОС ----------
    def reset_plan(self):
        if messagebox.askyesno("Подтверждение", "Сбросить план к стандартному?"):
            self.plan = self.default_plan
            self.save_plan()
            self.show_day(self.current_day)

    # ---------- ТЕМА ----------
    def load_theme(self):
        if os.path.exists(self.theme_file):
            try:
                with open(self.theme_file, "r", encoding="utf-8") as f:
                    t = json.load(f).get("theme", "dark")
                    return t if t in THEMES else "dark"
            except Exception:
                pass
        return "dark"

    def save_theme(self):
        try:
            with open(self.theme_file, "w", encoding="utf-8") as f:
                json.dump({"theme": self.current_theme}, f)
        except Exception:
            pass

    def set_theme(self, name):
        if name in THEMES:
            self.current_theme = name
            self.save_theme()
            self.apply_theme()
            self.show_day(self.current_day)

    def apply_theme(self):
        c = THEMES[self.current_theme]

        self.root.configure(bg=c["bg"])
        self.top_bar.configure(bg=c["bg"])
        self.theme_buttons_frame.configure(bg=c["bg"])

        for child in self.theme_buttons_frame.winfo_children():
            if isinstance(child, tk.Label):
                child.configure(bg=c["bg"], fg=c["text"])

        self.title_label.configure(bg=c["bg"], fg=c["title"])

        self.main_frame.configure(bg=c["bg"])
        self.left_frame.configure(bg=c["bg"])
        self.days_label.configure(bg=c["bg"], fg=c["text"])

        self.right_frame.configure(bg=c["panel"])
        self.day_title.configure(bg=c["panel"], fg=c["day_title"])
        self.day_theme.configure(bg=c["panel"], fg=c["theme_text"])

        self.ex_list.configure(
            bg=c["list_bg"], fg=c["text"],
            selectbackground=c["accent"], selectforeground=c["accent_text"]
        )

        self.bottom_frame.configure(bg=c["bg"])
        self.reset_btn.configure(bg=c["reset_bg"], fg=c["accent_text"])
        self.exit_btn.configure(bg=c["exit_bg"], fg=c["text"])

        # Кнопки дней
        for d, btn in self.day_buttons.items():
            btn.configure(
                bg=c["btn_bg"], fg=c["btn_text"],
                activebackground=c["accent"],
                activeforeground=c["accent_text"]
            )

        # Кнопки темы
        for key, btn in self.theme_buttons.items():
            btn.configure(
                fg=("#1e1e1e" if key != "dark" else "#cdd6f4"),
                relief="sunken" if key == self.current_theme else "flat"
            )


# ---------- ЗАПУСК ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = GymPlanApp(root)
    root.mainloop()
