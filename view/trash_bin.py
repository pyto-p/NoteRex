from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu

from kivy.properties import ObjectProperty
from kivy.metrics import dp

from kv.components.empty_screen_msg import EmptyScreenMessage


class TrashBin(MDScreen):
    u_deleted_list = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        menu_list = [
            {
                'viewclass': 'OneLineListItem',
                'text': 'Restore All',
                'on_press': self.restore_all_notes
            },
            {
                'viewclass': 'OneLineListItem',
                'text': 'Delete All',
                'on_press': self.delete_all_notes
            },
        ]

        self.menu = MDDropdownMenu(
            elevation=2,
            background_color='#FFE4AE',
            items=menu_list,
            width_mult=2,
            max_height=dp(102),
        )

        self.empty_message = EmptyScreenMessage(
            img_path="assets/GettingStarted2(Transparent).png",
            message="Dino can keep and clean\n your mess"
        )
        self.add_widget(self.empty_message)

    def open_menu(self, button):
        if not self.menu.parent:
            self.menu.caller = button
            self.menu.open()

    def add_deleted_note(self, deleted_card):
        self.u_deleted_list.add_widget(deleted_card)

    def delete_all_notes(self):
        self.menu.dismiss()
        self.u_deleted_list.clear_widgets()
        self.update_deleted_list()

    def restore_all_notes(self):
        self.menu.dismiss()
        while self.u_deleted_list.children:
            card = self.u_deleted_list.children[len(self.u_deleted_list.children) - 1]
            card.restore_note()
        self.update_deleted_list()

    def permanent_delete_note(self, deleted_card):
        self.u_deleted_list.remove_widget(deleted_card)
        self.update_deleted_list()

    def update_deleted_list(self):
        self.u_deleted_list.children = sorted(
            self.u_deleted_list.children,
            key=lambda dn: dn.deleted_note.date_modified,
        )

        if len(self.u_deleted_list.children) == 0:
            if not self.empty_message.parent:
                self.add_widget(self.empty_message)
        else:
            if self.empty_message.parent:
                self.remove_widget(self.empty_message)

    def change_screen(self, direction, next):
        self.manager.transition.direction = direction
        self.manager.current = next