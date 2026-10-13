import flet as ft
from main_window import FitnessApp


def main(page):
    FitnessApp(page)


if __name__ == "__main__":
    ft.app(target=main)