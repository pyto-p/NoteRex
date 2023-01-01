from kivymd.uix.screenmanager import MDScreenManager


class WindowManager(MDScreenManager):
    __instance = None

    @staticmethod
    def get_instance():
        if WindowManager.__instance:
            return WindowManager.__instance
        WindowManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if WindowManager.__instance is not None:
            raise Exception("This is a singleton class. Cannot be instantiated.")
        else:
            WindowManager.__instance = self

    def change_screen(self, direction, next):
        self.transition.direction = direction
        self.current = next