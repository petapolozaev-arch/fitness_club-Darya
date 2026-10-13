import flet as ft
from datetime import datetime

from classes import MyMap, Training, Client
from components import MyText, Header, MyField, Btn, Row2, Col2, Card, MyList, Line


# главное окно приложения
class FitnessApp:
    def __init__(self, page):
        self.page = page
        self.page.title = "Фитнес-клуб"
        self.page.padding = 20
        self.client = None
        self.list = []
        self.map = MyMap()
        self.load()
        self.show_login()

    # --- стартовые тренировки ---
    def load(self):
        # вбила руками, чтобы было что показывать
        data = [
            (1, "Йога", "Аня", "Пн", "08:00", 15),
            (2, "Кроссфит", "Игорь", "Вт", "18:00", 20),
            (3, "Пилатес", "Маша", "Ср", "10:00", 10),
            (4, "Бокс", "Дима", "Чт", "20:00", 14),
            (5, "Танцы", "Оля", "Пт", "19:00", 18),
            (6, "Йога 2", "Аня", "Сб", "09:00", 12),
            (7, "Кроссфит 2", "Игорь", "Пн", "19:00", 16),
            (8, "Стретчинг", "Маша", "Вт", "11:00", 20),
            (9, "Кикбоксинг", "Дима", "Ср", "21:00", 10),
            (10, "Хип-хоп", "Оля", "Чт", "18:30", 15),
        ]
        for d in data:
            t = Training(*d)
            self.list.append(t)
            self.map.add(t.tid, t)

    # --- экран входа ---
    def show_login(self):
        self.page.controls.clear()
        self.lf = MyField("Логин", width=280)
        self.nf = MyField("Имя", width=280)
        card = Card(Col2([
            Header("Вход"),
            Line(),
            self.lf,
            self.nf,
            Btn("Войти", self.login, width=280),
        ]))
        self.page.add(Row2([card]))
        self.page.update()

    def login(self, e):
        l = self.lf.value.strip() if self.lf.value else ""
        n = self.nf.value.strip() if self.nf.value else ""
        if not l or not n:
            return
        self.client = Client(l, n)
        self.show_main()

    # --- главный экран ---
    def show_main(self):
        self.page.controls.clear()
        self.memb_text = MyText("Абонемент: " + str(self.client.memb))
        self.sched = MyList()
        self.my = MyList()

        header = Row2([
            Header("Клуб · " + self.client.name),
            self.memb_text,
            Btn("Выход", self.exit),
        ])

        # обернула в контейнер с высотой, иначе списки не рисуются
        body = Row2([
            Card(self.sched, expand=True),
            Card(self.my, expand=True),
        ])

        self.page.add(
            header,
            Row2([MyText("Расписание:"), MyText("Мои записи:")]),
            ft.Container(content=body, height=500, expand=True),
        )
        self.render()
        self.page.update()

    # --- перерисовка после каждого действия ---
    def render(self):
        self.sched.controls.clear()
        for t in sorted(self.list):
            free = t.capacity - t.booked
            btn = "Отмена" if t in self.client.books else "Запись"
            if free <= 0 and t not in self.client.books:
                btn = "нет мест"
            row = Row2([
                MyText(str(t), expand=True),
                MyText(str(free) + "/" + str(t.capacity)),
                Btn(btn, lambda e, x=t: self.do(x)),
            ])
            self.sched.controls.append(Card(row))

        self.my.controls.clear()
        for t in self.client.books:
            row = Row2([
                MyText(str(t), expand=True),
                Btn("Отмена", lambda e, x=t: self.do(x)),
            ])
            self.my.controls.append(Card(row))

        self.memb_text.value = "Абонемент: " + str(self.client.memb)
        self.page.update()

    # --- клик по кнопке ---
    def do(self, tr):
        if tr in self.client.books:
            self.client.otmena(tr)
        else:
            res = self.client.zapis(tr)
            if res != "ок":
                self.page.snack_bar = ft.SnackBar(ft.Text(res))
                self.page.snack_bar.open = True
        self.render()

    # --- выход, сохраняю отчёт ---
    def exit(self, e):
        # формат как в методичке
        with open("report.txt", "w", encoding="utf-8") as f:
            now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            inn = self.client.time_in.strftime("%d.%m.%Y %H:%M:%S")
            f.write("+----------------------+------------------------+------------------------+\n")
            f.write("|        login         |        time_in         |       time_out         |\n")
            f.write("+----------------------+------------------------+------------------------+\n")
            f.write("| " + self.client.login.ljust(21) + "| " + inn.ljust(23) + "| " + now.ljust(23) + "|\n")
            f.write("+----------------------+------------------------+------------------------+\n")
        self.page.window.close()