import os
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from kivy.core.window import Window
from view import *


class Noterex(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.icon = "assets/NoterexIcon.png"
        self.screen_manager = MDScreenManager()
        self.load_all_kv_files(os.path.join(os.getcwd(), "kv"))

    def build(self):
        SCREENS = {
            "GettingStarted": GettingStarted(),
            "NotesDashboard": NotesDashboard(),
            "Bookmarks": Bookmarks(),
            "EditNotes": OpenNotes(),
            "TrashBin": TrashBin(),
            "AboutApp": AboutApp(),
        }

        self.theme_cls.material_style = "M3"
        for screen in SCREENS.values():
            self.screen_manager.add_widget(screen)
        return self.screen_manager


if __name__ == "__main__":
    Window.size = (360, 640)
    Window.top = 50
    Window.left = 1160
    Noterex().run()