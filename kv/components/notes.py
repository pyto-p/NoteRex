from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDIcon

from kivy.properties import StringProperty
from kivy.event import EventDispatcher


class NoteCard(MDCard):
    def __init__(self, content=None, date=None, id=None, note=None, *args, **kwargs):
        # initialize the note contents of the note card if there is
        if note:
            self.note = note
        else:
            self.note = Note(content, date, id)

        # initializes other components
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
        self.bookmark_icon = MDIcon(
            icon = "star",
            theme_text_color = "Custom",
            text_color = "#E79F48",
        )

    def view(self):
        # viewing the note content
        screen = self.app.screen_manager.get_screen("edit_notes")
        screen.open_note(self.app.screen_manager.current, self)

    def update(self, content, date):
        # updating the note's content
        self.note.set(content, date)

    def add_bookmark_icon(self):
        # add bookmark icon if bookmarked
        if not self.bookmark_icon.parent:
            self.ids["content"].add_widget(self.bookmark_icon)

    def remove_bookmark_icon(self):
        # remove bookmark icon if unbookmarked
        self.ids["content"].remove_widget(self.bookmark_icon)

    def change_screen(self, direction, next):
        self.app.screen_manager.transition.direction = direction
        self.app.screen_manager.current = next


class Note(EventDispatcher):
    """
    Main content of the note card
    
    Properties:
    - u_content: content of the note card
    - u_date_modified: represents the date of the recent modification of the card.
    """
    u_content = StringProperty()
    u_date_modified = StringProperty()

    def __init__(self, content, date, id):
        self.id = id
        self.u_content = content
        self.u_date_modified = date.strftime("%m/%d/%Y")
        self.date_modified = date
        self.is_bookmarked = False

    def set(self, content, date):
        self.u_content = content
        self.u_date_modified = date.strftime("%m/%d/%Y")
        self.date_modified = date
