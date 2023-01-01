from kivymd.uix.screen import MDScreen
from kivy.properties import ObjectProperty

from kv.components.empty_screen_msg import EmptyScreenMessage


class Bookmarks(MDScreen):
    """
    Represents bookmark screen

    Properties:
    - notes_area: holds all bookmark cards
    """
    notes_area = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.empty_message = EmptyScreenMessage(
            img_path="assets/NoNote(Transparent).png",
            message="Dino can bookmark\n your notes"
        )
        self.add_widget(self.empty_message)

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
            key=lambda nc: nc.note.date_modified
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