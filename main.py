from abc import ABC, abstractmethod
from datetime import datetime
import flet as ft


# ===== Своя структура вместо словаря =====
class MyMap:
    def __init__(self):
        self.k = []
        self.v = []

    def add(self, key, val):
        if key in self.k:
            self.v[self.k.index(key)] = val
        else:
            self.k.append(key)
            self.v.append(val)

    def get(self, key):
        if key in self.k:
            return self.v[self.k.index(key)]
        return None

    def keys(self):
        return self.k

    def __eq__(self, other):
        return isinstance(other, MyMap) and self.k == other.k and self.v == other.v

    def __repr__(self):
        return f"MyMap({len(self.k)})"

    def __str__(self):
        return f"MyMap: {len(self.k)} шт"


# ===== Абстрактный класс =====
class Base(ABC):
    @abstractmethod
    def short(self): ...
    @abstractmethod
    def full(self): ...


# ===== Тренировка =====
class Training(Base):
    def __init__(self, tid, name, coach, day, time, capacity):
        self._tid = tid
        self._name = name
        self._coach = coach
        self._day = day
        self._time = time
        self._capacity = capacity
        self._booked = 0

    @property
    def tid(self):
        return self._tid

    @property
    def name(self):
        return self._name

    @property
    def coach(self):
        return self._coach

    @property
    def day(self):
        return self._day

    @property
    def time(self):
        return self._time

    @property
    def capacity(self):
        return self._capacity

    @property
    def booked(self):
        return self._booked

    @name.setter
    def name(self, v):
        if not v:
            raise ValueError("пустое название")
        self._name = v

    @coach.setter
    def coach(self, v): self._coach = v

    @day.setter
    def day(self, v): self._day = v

    @time.setter
    def time(self, v): self._time = v

    @capacity.setter
    def capacity(self, v): self._capacity = int(v)

    def __eq__(self, other):
        if not isinstance(other, Training):
            return False
        return self._tid == other._tid

    def __lt__(self, other):
        return self._name < other._name

    def __gt__(self, other):
        return self._name > other._name

    def __repr__(self):
        return f"Training({self._tid}, {self._name})"

    def __str__(self):
        return f"{self._name} {self._day} {self._time}"

    def short(self):
        return self._name

    def full(self):
        return f"{self._name} ({self._coach}) {self._capacity - self._booked}/{self._capacity}"

    def есть_место(self):
        return self._booked < self._capacity


# ===== Клиент =====
class Client(Base):
    def __init__(self, login, name):
        self._login = login
        self._name = name
        self._memb = 10
        self._books = []
        self._in = datetime.now()

    @property
    def login(self): return self._login

    @property
    def name(self): return self._name

    @property
    def memb(self): return self._memb

    @property
    def books(self): return self._books

    @property
    def time_in(self): return self._in

    @login.setter
    def login(self, v): self._login = v

    @name.setter
    def name(self, v): self._name = v

    @memb.setter
    def memb(self, v): self._memb = int(v)

    def __eq__(self, other):
        return isinstance(other, Client) and self._login == other._login

    def __lt__(self, other):
        return self._name < other._name

    def __gt__(self, other):
        return self._name > other._name

    def __repr__(self):
        return f"Client({self._login})"

    def __str__(self):
        return self._name

    def short(self):
        return self._login

    def full(self):
        return f"{self._name}, абонемент {self._memb}"

    def zapis(self, tr):
        if tr in self._books:
            return "уже записаны"
        if len(self._books) >= 4:
            return "лимит 4"
        if not tr.есть_место():
            return "мест нет"
        if self._memb <= 0:
            return "абонемент кончился"
        tr._booked += 1
        self._books.append(tr)
        self._memb -= 1
        return "ок"

    def otmena(self, tr):
        if tr not in self._books:
            return "не записаны"
        self._books.remove(tr)
        self._memb += 1
        tr._booked -= 1
        return "ок"


# ===== 10 переопределённых UI-компонентов =====
class MyText(ft.Text):
    def __init__(self, t="", **k):
        super().__init__(value=t, size=14, **k)


class Header(ft.Text):
    def __init__(self, t="", **k):
        super().__init__(value=t, size=22, weight=ft.FontWeight.BOLD, color="#1a237e", **k)


class MyField(ft.TextField):
    def __init__(self, l="", **k):
        super().__init__(label=l, **k)


class Btn(ft.ElevatedButton):
    def __init__(self, t="", click=None, **k):
        super().__init__(text=t, on_click=click, bgcolor="#3949ab", color="white", **k)


class Row2(ft.Row):
    def __init__(self, c=None, **k):
        super().__init__(controls=c or [], **k)


class Col2(ft.Column):
    def __init__(self, c=None, **k):
        super().__init__(controls=c or [], spacing=8, **k)


class Card(ft.Container):
    def __init__(self, content=None, **k):
        super().__init__(content=content, padding=10, bgcolor="#eee", border_radius=6, **k)


class MyList(ft.ListView):
    def __init__(self, **k):
        super().__init__(spacing=4, expand=True, **k)


class MyDropdown(ft.Dropdown):
    def __init__(self, l="", opt=None, **k):
        super().__init__(label=l, options=opt or [], **k)


class Line(ft.Divider):
    def __init__(self):
        super().__init__(height=1)


# ===== Основной класс =====
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

    def load(self):
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

    def show_login(self):
        self.page.controls.clear()
        self.lf = MyField("Логин", width=280)
        self.nf = MyField("Имя", width=280)
        card = Card(Col2([
            Header("Вход"), Line(),
            self.lf, self.nf,
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

    def do(self, tr):
        if tr in self.client.books:
            self.client.otmena(tr)
        else:
            res = self.client.zapis(tr)
            if res != "ок":
                self.page.snack_bar = ft.SnackBar(ft.Text(res))
                self.page.snack_bar.open = True
        self.render()

    def exit(self, e):
        with open("report.txt", "w", encoding="utf-8") as f:
            now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            inn = self.client.time_in.strftime("%d.%m.%Y %H:%M:%S")
            f.write("+----------------------+------------------------+------------------------+\n")
            f.write("|        login         |        time_in         |       time_out         |\n")
            f.write("+----------------------+------------------------+------------------------+\n")
            f.write("| " + self.client.login.ljust(21) + "| " + inn.ljust(23) + "| " + now.ljust(23) + "|\n")
            f.write("+----------------------+------------------------+------------------------+\n")
        self.page.window.close()


def main(page):
    FitnessApp(page)


if __name__ == "__main__":
    ft.app(target=main)