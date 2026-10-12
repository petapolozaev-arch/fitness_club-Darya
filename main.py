import flet as ft
from abc import ABC, abstractmethod
from datetime import datetime


# ------------------------------------------------------------------
# Своя мапа (препод запретил dict — делаем на двух списках)
# ------------------------------------------------------------------
class CustomMap:
    """Аналог словаря, но без использования dict. Хранит ключи и значения
    в двух параллельных списках, поиск — через index()."""

    def __init__(self):
        self._keys = []
        self._values = []

    def put(self, key, value):
        if key in self._keys:
            self._values[self._keys.index(key)] = value
        else:
            self._keys.append(key)
            self._values.append(value)

    def get(self, key, default=None):
        if key in self._keys:
            return self._values[self._keys.index(key)]
        return default

    def remove(self, key):
        if key in self._keys:
            i = self._keys.index(key)
            self._keys.pop(i)
            self._values.pop(i)

    def keys(self):
        return list(self._keys)

    def values(self):
        return list(self._values)

    def items(self):
        return list(zip(self._keys, self._values))

    def __contains__(self, key):
        return key in self._keys

    def __len__(self):
        return len(self._keys)

    def __eq__(self, other):
        if not isinstance(other, CustomMap):
            return False
        return self.items() == other.items()

    def __repr__(self):
        return f"CustomMap({self.items()})"

    def __str__(self):
        return f"CustomMap: {len(self)} записей"


# ------------------------------------------------------------------
# Абстрактная сущность клуба
# ------------------------------------------------------------------
class ClubEntity(ABC):
    """Базовый класс для всех сущностей фитнес-клуба.
    Наследники обязаны реализовать два метода ниже."""

    @abstractmethod
    def short_info(self):
        ...

    @abstractmethod
    def full_info(self):
        ...


# ------------------------------------------------------------------
# Тренировка
# ------------------------------------------------------------------
class Training(ClubEntity):

    def __init__(self, tr_id, name, trainer, direction,
                 day, start_time, duration, capacity):
        self._tr_id = tr_id
        self._name = name
        self._trainer = trainer
        self._direction = direction
        self._day = day
        self._start_time = start_time
        self._duration = duration
        self._capacity = capacity
        self._booked = 0

    # ---------- геттеры / сеттеры ----------
    @property
    def tr_id(self):
        return self._tr_id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Название тренировки не может быть пустым")
        self._name = value

    @property
    def trainer(self):
        return self._trainer

    @trainer.setter
    def trainer(self, value):
        self._trainer = value

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        self._direction = value

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, value):
        self._day = value

    @property
    def start_time(self):
        return self._start_time

    @start_time.setter
    def start_time(self, value):
        self._start_time = value

    @property
    def duration(self):
        return self._duration

    @duration.setter
    def duration(self, value):
        self._duration = int(value)

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        if int(value) < 1:
            raise ValueError("Вместимость должна быть > 0")
        self._capacity = int(value)

    @property
    def booked(self):
        return self._booked

    # ---------- магические методы ----------
    def __eq__(self, other):
        if not isinstance(other, Training):
            return False
        return self._tr_id == other._tr_id

    def __lt__(self, other):
        return self._name.lower() < other._name.lower()

    def __gt__(self, other):
        return self._name.lower() > other._name.lower()

    def __hash__(self):
        return hash(self._tr_id)

    def __repr__(self):
        return f"Training(id={self._tr_id}, name={self._name!r})"

    def __str__(self):
        return f"{self._name} ({self._direction}) — {self._day} {self._start_time}"

    # ---------- абстрактные методы ----------
    def short_info(self):
        return f"{self._name} — тренер {self._trainer}"

    def full_info(self):
        free = self._capacity - self._booked
        return f"{self} · {self._duration} мин · свободно {free}/{self._capacity}"

    # ---------- своя логика ----------
    def has_free_seat(self):
        return self._booked < self._capacity

    def book_seat(self):
        if not self.has_free_seat():
            return False
        self._booked += 1
        return True

    def free_seat(self):
        if self._booked > 0:
            self._booked -= 1

    def is_long(self):
        return self._duration >= 60


# ------------------------------------------------------------------
# Клиент клуба
# ------------------------------------------------------------------
class Client(ClubEntity):

    MAX_BOOKINGS = 4

    def __init__(self, login, name, membership=10):
        self._login = login
        self._name = name
        self._membership = membership
        self._bookings = []
        self._time_in = datetime.now()

    # ---------- геттеры / сеттеры ----------
    @property
    def login(self):
        return self._login

    @login.setter
    def login(self, value):
        self._login = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def membership(self):
        return self._membership

    @membership.setter
    def membership(self, value):
        if int(value) < 0:
            raise ValueError("Абонемент не может быть отрицательным")
        self._membership = int(value)

    @property
    def bookings(self):
        return list(self._bookings)

    @property
    def time_in(self):
        return self._time_in

    # ---------- магические методы ----------
    def __eq__(self, other):
        if not isinstance(other, Client):
            return False
        return self._login == other._login

    def __lt__(self, other):
        return self._name.lower() < other._name.lower()

    def __gt__(self, other):
        return self._name.lower() > other._name.lower()

    def __hash__(self):
        return hash(self._login)

    def __repr__(self):
        return f"Client(login={self._login!r})"

    def __str__(self):
        return f"{self._name} ({self._login})"

    # ---------- абстрактные методы ----------
    def short_info(self):
        return self._login

    def full_info(self):
        return (f"{self} — абонемент: {self._membership} занятий, "
                f"записей: {len(self._bookings)}")

    # ---------- бизнес-логика ----------
    def sign_up(self, training):
        if training in self._bookings:
            return False, "Вы уже записаны на эту тренировку"
        if len(self._bookings) >= Client.MAX_BOOKINGS:
            return False, f"Не больше {Client.MAX_BOOKINGS} активных записей"
        if not training.has_free_seat():
            return False, "Свободных мест нет"
        if self._membership <= 0:
            return False, "Абонемент закончился"

        if training.book_seat():
            self._bookings.append(training)
            self._membership -= 1
            return True, f"Вы записаны на «{training.name}»"
        return False, "Не удалось записаться"

    def cancel(self, training):
        if training not in self._bookings:
            return False, "Вы не записаны на эту тренировку"
        self._bookings.remove(training)
        self._membership += 1
        training.free_seat()
        return True, f"Запись на «{training.name}» отменена"

    def can_pay(self):
        return self._membership > 0


# ------------------------------------------------------------------
# Переопределённые UI-компоненты (10 штук)
# ------------------------------------------------------------------
class AppText(ft.Text):
    def __init__(self, value="", size=14, **kwargs):
        super().__init__(value=value, size=size, color="#2c3e50", **kwargs)


class AppTitle(ft.Text):
    def __init__(self, value="", **kwargs):
        super().__init__(
            value=value, size=22,
            weight=ft.FontWeight.BOLD, color="#1a237e", **kwargs
        )


class AppTextField(ft.TextField):
    def __init__(self, label="", **kwargs):
        super().__init__(
            label=label,
            border_color="#3949ab",
            focused_border_color="#1a237e",
            cursor_color="#1a237e",
            **kwargs
        )


class AppButton(ft.ElevatedButton):
    def __init__(self, text="", on_click=None, **kwargs):
        super().__init__(
            text=text, on_click=on_click,
            bgcolor="#3949ab", color="white", **kwargs
        )


class AppRow(ft.Row):
    def __init__(self, controls=None, **kwargs):
        super().__init__(
            controls=controls or [],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            **kwargs
        )


class AppColumn(ft.Column):
    def __init__(self, controls=None, **kwargs):
        super().__init__(controls=controls or [], spacing=10, **kwargs)


class AppContainer(ft.Container):
    def __init__(self, content=None, **kwargs):
        super().__init__(
            content=content,
            padding=12,
            border_radius=8,
            bgcolor="#f5f6fa",
            **kwargs
        )


class AppListView(ft.ListView):
    def __init__(self, **kwargs):
        super().__init__(spacing=6, padding=8, **kwargs)


class AppDropdown(ft.Dropdown):
    def __init__(self, label="", options=None, **kwargs):
        super().__init__(
            label=label,
            options=options or [],
            border_color="#3949ab",
            focused_border_color="#1a237e",
            **kwargs
        )


class AppDivider(ft.Divider):
    def __init__(self):
        super().__init__(height=1, color="#c5cae9")


# ------------------------------------------------------------------
# Приложение
# ------------------------------------------------------------------
class FitnessApp:

    REPORT_FILE = "report.txt"
    DIRECTIONS = ["Йога", "Кроссфит", "Пилатес", "Бокс", "Танцы"]
    DAYS = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб"]

    def __init__(self, page):
        self._page = page
        self._client = None
        self._trainings_list = []
        self._trainings_by_id = CustomMap()

        self._setup_page()
        self._load_demo_trainings()
        self._build_login_view()

    # ---------- окно ----------
    def _setup_page(self):
        p = self._page
        p.title = "Фитнес-клуб"
        p.padding = 20
        p.theme_mode = ft.ThemeMode.LIGHT
        try:
            p.window.width = 1100
            p.window.height = 740
        except Exception:
            p.window_width = 1100
            p.window_height = 740
        p.on_disconnect = self._on_disconnect

    # ---------- стартовые данные ----------
    def _load_demo_trainings(self):
        demo = [
            (1, "Утренняя йога", "Анна Смирнова", "Йога", "Пн", "08:00", 60, 15),
            (2, "Хатха-йога", "Анна Смирнова", "Йога", "Ср", "19:00", 90, 12),
            (3, "Кроссфит PRO", "Игорь Петров", "Кроссфит", "Вт", "18:00", 60, 20),
            (4, "Кроссфит начинающим", "Игорь Петров", "Кроссфит", "Чт", "17:00", 45, 25),
            (5, "Пилатес для спины", "Мария Кузнецова", "Пилатес", "Пн", "10:00", 55, 10),
            (6, "Пилатес продвинутый", "Мария Кузнецова", "Пилатес", "Пт", "11:00", 60, 8),
            (7, "Бокс для взрослых", "Дмитрий Волков", "Бокс", "Ср", "20:00", 90, 14),
            (8, "Бокс для детей", "Дмитрий Волков", "Бокс", "Сб", "11:00", 60, 16),
            (9, "Хип-хоп", "Ольга Романова", "Танцы", "Вт", "19:30", 75, 18),
            (10, "Современные танцы", "Ольга Романова", "Танцы", "Чт", "20:00", 60, 15),
            (11, "Силовая тренировка", "Игорь Петров", "Кроссфит", "Пт", "18:30", 70, 12),
            (12, "Растяжка", "Анна Смирнова", "Йога", "Сб", "09:00", 45, 20),
        ]
        for row in demo:
            tr = Training(*row)
            self._trainings_list.append(tr)
            self._trainings_by_id.put(tr.tr_id, tr)

    # ---------- статические методы ----------
    @staticmethod
    def validate_time(value):
        if not value or ":" not in value:
            return False
        parts = value.split(":")
        if len(parts) != 2:
            return False
        try:
            h, m = int(parts[0]), int(parts[1])
        except ValueError:
            return False
        return 0 <= h <= 23 and 0 <= m <= 59

    @staticmethod
    def validate_duration(value):
        try:
            d = int(value)
        except (TypeError, ValueError):
            return False
        return 15 <= d <= 180

    # ---------- экран входа ----------
    def _build_login_view(self):
        p = self._page
        p.controls.clear()

        self._login_field = AppTextField(label="Логин", width=300)
        self._name_field = AppTextField(label="Ваше имя", width=300)

        card = AppContainer(
            content=AppColumn(
                [
                    AppTitle("Вход в фитнес-клуб"),
                    AppDivider(),
                    self._login_field,
                    self._name_field,
                    AppButton("Войти", on_click=self._on_login_click, width=300),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=380,
        )

        p.add(ft.Row([card], alignment=ft.MainAxisAlignment.CENTER, expand=True))
        p.update()

    def _on_login_click(self, e):
        login = (self._login_field.value or "").strip()
        name = (self._name_field.value or "").strip()
        if not login or not name:
            self._show_snack("Заполните логин и имя")
            return
        self._client = Client(login, name, membership=10)
        self._build_main_view()

    # ---------- главный экран ----------
    def _build_main_view(self):
        p = self._page
        p.controls.clear()

        self._search_field = AppTextField(label="Поиск тренировки", width=320)
        self._search_field.on_change = self._on_filter_change

        self._direction_filter = AppDropdown(
            label="Направление", width=220, value="Все",
            options=[ft.dropdown.Option("Все")]
            + [ft.dropdown.Option(d) for d in FitnessApp.DIRECTIONS],
        )
        self._direction_filter.on_change = self._on_filter_change

        self._membership_text = AppText("", size=16)
        self._update_membership_text()

        self._schedule_view = AppListView(expand=True)
        self._my_view = AppListView(expand=True)

        header = AppRow(
            [
                AppTitle(f"Клуб · {self._client.name}"),
                ft.Container(expand=True),
                self._membership_text,
                AppButton("Сохранить отчёт и выйти", on_click=self._on_exit_click),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        schedule_tab = AppColumn(
            [
                AppRow([self._search_field, self._direction_filter]),
                AppContainer(self._schedule_view, expand=True),
            ],
            expand=True,
        )

        my_tab = AppColumn(
            [
                AppText("Мои записи (лимит 4 активных):"),
                AppContainer(self._my_view, expand=True),
            ],
            expand=True,
        )

        tabs = ft.Tabs(
            selected_index=0, expand=True,
            tabs=[
                ft.Tab(text="Расписание", content=schedule_tab),
                ft.Tab(text="Добавить тренировку", content=self._build_add_tab()),
                ft.Tab(text="Мои записи", content=my_tab),
            ],
        )

        p.add(header, tabs)
        self._render_schedule()
        self._render_my()
        p.update()

    def _build_add_tab(self):
        self._new_name = AppTextField(label="Название", width=340)
        self._new_trainer = AppTextField(label="Тренер", width=340)
        self._new_time = AppTextField(label="Время (HH:MM)", width=160)
        self._new_duration = AppTextField(label="Длительность (мин)", width=200)
        self._new_capacity = AppTextField(label="Мест", width=120)
        self._new_direction = AppDropdown(
            label="Направление", width=240,
            options=[ft.dropdown.Option(d) for d in FitnessApp.DIRECTIONS],
        )
        self._new_day = AppDropdown(
            label="День", width=120,
            options=[ft.dropdown.Option(d) for d in FitnessApp.DAYS],
        )

        return AppColumn([
            AppTitle("Добавить тренировку"),
            AppDivider(),
            self._new_name,
            self._new_trainer,
            AppRow([self._new_day, self._new_time, self._new_duration, self._new_capacity]),
            self._new_direction,
            AppButton("Добавить в расписание", on_click=self._on_add_training_click),
        ])

    # ---------- отрисовка ----------
    def _update_membership_text(self):
        self._membership_text.value = f"Абонемент: {self._client.membership} занятий"

    def _on_filter_change(self, e):
        self._render_schedule()

    def _render_schedule(self):
        query = (self._search_field.value or "").strip().lower()
        direction = self._direction_filter.value or "Все"

        self._schedule_view.controls.clear()
        for tr in sorted(self._trainings_list):
            if query and query not in tr.name.lower():
                continue
            if direction != "Все" and tr.direction != direction:
                continue
            self._schedule_view.controls.append(self._make_training_row(tr))
        self._page.update()

    def _make_training_row(self, tr):
        signed_up = tr in self._client.bookings
        free = tr.capacity - tr.booked

        if signed_up:
            btn_text, btn_disabled = "Отменить", False
        elif free <= 0:
            btn_text, btn_disabled = "Мест нет", True
        else:
            btn_text, btn_disabled = "Записаться", False

        return AppContainer(
            content=AppRow([
                AppText(str(tr), expand=True),
                AppText(f"[{tr.direction}]", width=110),
                AppText(f"{tr.duration} мин", width=80),
                AppText(f"{free}/{tr.capacity}", width=80),
                AppButton(
                    btn_text, width=120, disabled=btn_disabled,
                    on_click=lambda e, t=tr: self._toggle_training(t),
                ),
            ])
        )

    def _render_my(self):
        self._my_view.controls.clear()
        bookings = self._client.bookings
        if not bookings:
            self._my_view.controls.append(AppText("Пока нет активных записей."))
        else:
            for tr in bookings:
                self._my_view.controls.append(
                    AppContainer(AppRow([
                        AppText(str(tr), expand=True),
                        AppButton(
                            "Отменить", width=120,
                            on_click=lambda e, t=tr: self._toggle_training(t),
                        ),
                    ]))
                )
        self._page.update()

    # ---------- действия ----------
    def _toggle_training(self, tr):
        if tr in self._client.bookings:
            ok, msg = self._client.cancel(tr)
        else:
            ok, msg = self._client.sign_up(tr)

        if ok:
            self._show_snack(msg)
            self._update_membership_text()
        else:
            self._show_snack("Ошибка: " + msg)

        self._render_schedule()
        self._render_my()

    def _on_add_training_click(self, e):
        name = (self._new_name.value or "").strip()
        trainer = (self._new_trainer.value or "").strip()
        time_val = (self._new_time.value or "").strip()
        duration = (self._new_duration.value or "").strip()
        capacity = (self._new_capacity.value or "").strip()
        direction = self._new_direction.value
        day = self._new_day.value

        if not name or not trainer:
            self._show_snack("Заполните название и тренера")
            return
        if not FitnessApp.validate_time(time_val):
            self._show_snack("Время в формате HH:MM (например 18:30)")
            return
        if not FitnessApp.validate_duration(duration):
            self._show_snack("Длительность — от 15 до 180 минут")
            return
        try:
            cap_int = int(capacity)
            if cap_int < 1:
                raise ValueError
        except (TypeError, ValueError):
            self._show_snack("Некорректное число мест")
            return
        if not direction or not day:
            self._show_snack("Выберите направление и день")
            return

        new_id = max(self._trainings_by_id.keys() or [0]) + 1
        new_tr = Training(
            new_id, name, trainer, direction, day,
            time_val, int(duration), cap_int,
        )
        self._trainings_list.append(new_tr)
        self._trainings_by_id.put(new_id, new_tr)

        self._new_name.value = ""
        self._new_trainer.value = ""
        self._new_time.value = ""
        self._new_duration.value = ""
        self._new_capacity.value = ""
        self._new_direction.value = None
        self._new_day.value = None

        self._render_schedule()
        self._page.update()
        self._show_snack(f"Тренировка «{name}» добавлена")

    def _show_snack(self, text):
        self._page.snack_bar = ft.SnackBar(ft.Text(text))
        self._page.snack_bar.open = True
        self._page.update()

    # ---------- отчёт ----------
    def _save_report(self):
        if self._client is None:
            return
        time_out = datetime.now()
        fmt = "%d.%m.%Y %H:%M:%S"

        col1, col2, col3 = 22, 24, 24
        sep = "+" + "-" * col1 + "+" + "-" * col2 + "+" + "-" * col3 + "+"

        rows = [
            sep,
            "|" + "login".center(col1) + "|"
            + "time_in".center(col2) + "|"
            + "time_out".center(col3) + "|",
            sep,
            "|" + f" {self._client.login}".ljust(col1)
            + "|" + f" {self._client.time_in.strftime(fmt)}".ljust(col2)
            + "|" + f" {time_out.strftime(fmt)}".ljust(col3) + "|",
            sep,
        ]

        with open(FitnessApp.REPORT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(rows))

    def _on_exit_click(self, e):
        self._save_report()
        try:
            self._page.window.close()
        except Exception:
            try:
                self._page.window_close()
            except Exception:
                pass

    def _on_disconnect(self, e):
        self._save_report()


def main(page: ft.Page):
    FitnessApp(page)


if __name__ == "__main__":
    ft.app(target=main)