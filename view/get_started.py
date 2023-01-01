from kivymd.uix.screen import MDScreen


class GettingStarted(MDScreen):
    def change_screen(self, direction, next):
        self.manager.transition.direction = direction
        self.manager.current = next