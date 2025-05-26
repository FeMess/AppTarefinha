from app.views.interface import GUI, ft

def main(page: ft.Page):
    interface = GUI(page)
    interface.initialize()

ft.app(main)