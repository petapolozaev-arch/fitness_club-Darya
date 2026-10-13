import flet as ft


# тут мои компоненты поверх flet, чтобы одни и те же настройки не прописывать
# по заданию нужно минимум 10, у меня как раз 10 получилось

# тексты
class MyText(ft.Text):
    def __init__(self, t="", **k):
        super().__init__(value=t, size=14, **k)


class Header(ft.Text):
    def __init__(self, t="", **k):
        super().__init__(value=t, size=22, weight=ft.FontWeight.BOLD, color="#1a237e", **k)


# поле ввода
class MyField(ft.TextField):
    def __init__(self, l="", **k):
        super().__init__(label=l, **k)


# кнопка
class Btn(ft.ElevatedButton):
    def __init__(self, t="", click=None, **k):
        super().__init__(text=t, on_click=click, bgcolor="#3949ab", color="white", **k)


# выравнивание
class Row2(ft.Row):
    def __init__(self, c=None, **k):
        super().__init__(controls=c or [], **k)


class Col2(ft.Column):
    def __init__(self, c=None, **k):
        super().__init__(controls=c or [], spacing=8, **k)


# контейнер-карточка и список
class Card(ft.Container):
    def __init__(self, content=None, **k):
        super().__init__(content=content, padding=10, bgcolor="#eee", border_radius=6, **k)


class MyList(ft.ListView):
    def __init__(self, **k):
        super().__init__(spacing=4, expand=True, **k)


# выпадающий список (пригодится для фильтра) и разделитель
class MyDropdown(ft.Dropdown):
    def __init__(self, l="", opt=None, **k):
        super().__init__(label=l, options=opt or [], **k)


class Line(ft.Divider):
    def __init__(self):
        super().__init__(height=1)