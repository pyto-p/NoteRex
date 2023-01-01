from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import OneLineIconListItem

from kivy.metrics import dp
from kivy.properties import ObjectProperty, StringProperty

from kv.components.empty_screen_msg import EmptyScreenMessage


class NotesDashboard(MDScreen):
    """
    Main home screen/dashboard screen for creating and viewing notes

    Properties:
    - notes_area: holds all notes created.
    """
    notes_area = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # specifies the list of options for the menu
        menu_list = [
            {
                'viewclass': 'IconListItem',
                'icon': 'cog-outline',
                'text': 'Bookmarks',
                'pos_hint': {"right": 0.95},
                'on_press': lambda: self.change_screen("left", "bookmarks")
            },
            {
                'viewclass': 'IconListItem',
                'icon': 'trash-can-outline',
                'text': 'Trash Bin',
                'pos_hint': {"right": 0.95},
                'on_press': lambda: self.change_screen("left", "trash_bin")
            },
            {
                'viewclass': 'IconListItem',
                'icon': 'help-circle-outline',
                'text': 'About App',
                'pos_hint': {"right": 0.95},
                'on_press': lambda: self.change_screen("left", "about_app")
            }
        ]

        # creating the menu
        self.menu = MDDropdownMenu(
            elevation=2,
            background_color='#FFE4AE',
            items=menu_list,
            width_mult=3,
            max_height=dp(152),
        )

        # indicates no notes yet
        self.empty_message = EmptyScreenMessage(
            img_path="assets/NoNote(Transparent).png",
            message="Dino is sad, can you\n add some notes?"
        )
        self.add_widget(self.empty_message)

    def open_menu(self, button):
        if not self.menu.parent:
            self.menu.caller = button
            self.menu.open()

    def add_note(self, note_card):
        notes_list_size = len(self.notes_area.children)
        self.notes_area.add_widget(note_card, notes_list_size)

    def remove_note(self, note_card):
        for card in self.notes_area.children:
            if card.note.id == note_card.note.id:
                self.notes_area.remove_widget(card)
                return card

    def update_notes_list(self):
        # sorts the notes based on their dates
        self.notes_area.children = sorted(
            self.notes_area.children,
            key=lambda nc: nc.note.date_modified,
        )

        # show empty message if no notes in the screen
        if len(self.notes_area.children) == 0:
            if not self.empty_message.parent:
                self.add_widget(self.empty_message)
        else:
            if self.empty_message.parent:
                self.remove_widget(self.empty_message)

        # add bookmark icon if bookmarked
        for card in self.notes_area.children:
            if card.note.is_bookmarked:
                card.add_bookmark_icon()
            else:
                card.remove_bookmark_icon()

    def change_screen(self, direction, next):
        self.manager.transition.direction = direction
        self.manager.current = next
        self.menu.dismiss()


class IconListItem(OneLineIconListItem):
    """
    Main viewclass for the menu
    - icon: the icon to be shown in the menu.
    """
    icon = StringProperty()