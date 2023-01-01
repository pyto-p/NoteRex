from kivymd.uix.screen import MDScreen


class AboutApp(MDScreen):
    def change_screen(self, direction, next):
        self.manager.transition.direction = direction
        self.manager.current = next