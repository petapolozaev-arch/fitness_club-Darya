from abc import ABC, abstractmethod
from datetime import datetime


# ------ MyMap: замена словаря ------
# в задании нельзя dict, поэтому храню ключи и значения в двух списках
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


# ------ Base: общий предок ------
class Base(ABC):
    @abstractmethod
    def short(self): ...

    @abstractmethod
    def full(self): ...


# ------ Training: одна тренировка ------
class Training(Base):
    def __init__(self, tid, name, coach, day, time, capacity):
        self._tid = tid
        self._name = name
        self._coach = coach
        self._day = day
        self._time = time
        self._capacity = capacity
        self._booked = 0

    # свойства (геттеры)
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

    # сеттеры, где надо - с проверкой
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

    # магические методы - требуются в задании
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

    # назвала по-русски, так мне понятнее
    def есть_место(self):
        return self._booked < self._capacity


# ------ Client: клиент клуба ------
class Client(Base):
    def __init__(self, login, name):
        self._login = login
        self._name = name
        self._memb = 10
        self._books = []
        self._in = datetime.now()

    # тут уже устала писать развёрнуто, сделала в одну строку
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

    # запись на тренировку, возвращает строку - что получилось
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