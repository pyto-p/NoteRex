from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton

from kivy.properties import StringProperty, ObjectProperty
from kivy.clock import Clock

from kv.components.notes import NoteCard
from kv.components.deleted_notes import DeletedNotes
from datetime import datetime


class OpenNotes(MDScreen):
    """
    Screen for Opening Notes

    Static variables used are:
    - u_state: defines the current state of the note. Values are "Edit", "View"
    - u_toolbar: for accessing the toolbar properties
    - u_txt_input: for accessing the text input properties
    """
    u_state = StringProperty()
    u_toolbar = ObjectProperty()
    u_txt_input = ObjectProperty()
    u_button_bar = ObjectProperty()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dialog = None
        self.note_card = None
        self.from_screen = "" 
        Clock.schedule_once(lambda dt: self.get_screens())

        self.card_id = 0     # not yet sure about the id system of every notes
        self.check_btn = ["check", self.save_note]
        self.bookmark_btn = ["star-outline", self.bookmark_note]
        self.snackbar = Snackbar(duration=1)

    def open_note(self, from_screen, note_card=None):
        """
        Responsible for opening the note.

        Args:
            state (str): state of the note. Values are "Edit", "View".
            note_card (Notes, optional): for determining if note is opened or a new note. Defaults to None.
        """
        self.note_card = note_card
        self.from_screen = from_screen

        if note_card:
            self.viewing()
            self.u_txt_input.text = note_card.note.u_content
        else:
            self.u_txt_input.text = ""
            self.u_txt_input.cursor = (0, 0)
            self.u_txt_input.focus = True

        if from_screen == "trash_bin":
            self.u_txt_input.readonly = True
            self.bookmark_btn[0] = ""
            self.ids["container"].remove_widget(self.u_button_bar)
        else:
            self.u_txt_input.readonly = False
            if not self.u_button_bar.parent:
                self.ids["container"].add_widget(self.u_button_bar)

    # ========= BUTTON CALLBACK FUNCTIONS =========
    def change_screen(self, direction, next):
        """
        Go to the next screen.

        Args:
            direction (str): the direction of transition.
            next (str): next screen to go to.
        """
        self.manager.transition.direction = direction
        self.manager.current = next

    def save_note(self, *_):
        """
        Function for saving note that is created or edited.
        """        
        if not self.u_txt_input.text:
            self.change_screen("down", self.from_screen)
            return

        date = datetime.now()
        if self.note_card:
            self.note_card.update(self.u_txt_input.text, date)
            self.update_screens_notes_list()
        else:
            note_card = NoteCard(self.u_txt_input.text, date, self.card_id)
            self.note_card = note_card
            self.dashboard.add_note(note_card)
            self.update_screens_notes_list()
            self.card_id += 1

        self.viewing()
        self.open_snackbar("Note saved.")

    def bookmark_note(self, *_):
        if self.note_card.note.is_bookmarked:
            self.bookmarks.remove_note(self.note_card)
            self.open_snackbar("Removed in bookmarks.")
        else:
            bookmark_note_card = NoteCard(note=self.note_card.note)
            self.bookmarks.add_note(bookmark_note_card)
            self.open_snackbar("Added to bookmarks.")

        self.note_card.note.is_bookmarked = not self.note_card.note.is_bookmarked
        self.update_screens_notes_list()
        self.viewing()

    def delete_note(self, *_):
        if self.note_card.parent:
            dn = self.dashboard.remove_note(self.note_card)
            bn = self.bookmarks.remove_note(self.note_card)
            self.trash_bin.add_deleted_note(DeletedNotes(dn, bn))
            self.change_screen("down", self.from_screen)
            self.update_screens_notes_list()
            self.trash_bin.update_deleted_list()
            self.close_dialog()

    def open_format_menu(self):
        print("Format menu opened!")

    def attach_file(self):
        print("attaching a file...")

    # ======= HELPER FUNCTIONS ===========
    def get_screens(self):
        self.dashboard = self.manager.get_screen("dashboard")
        self.bookmarks = self.manager.get_screen("bookmarks")
        self.trash_bin = self.manager.get_screen("trash_bin")

    def editing(self, value):
        """
        TextInput is focused and note is in editing state.

        Args:
            value (bool): if text input was focused or not. Values are `True`, `False`.
        """
        if value and self.from_screen != "trash_bin":
            self.u_state = "Edit Notes"
            self.u_toolbar.right_action_items[0] = self.check_btn

    def viewing(self):
        """
        User saved a note and the note is in viewing state.
        """        
        self.u_state = "View Notes"
        self.bookmark_btn[0] = "star" if self.note_card.note.is_bookmarked else "star-outline"
        self.u_toolbar.right_action_items[0] = self.bookmark_btn

    def update_screens_notes_list(self):
        # updating the dashboard and bookmarks screen
        self.dashboard.update_notes_list()
        self.bookmarks.update_notes_list()

    def open_snackbar(self, text):
        self.snackbar.text = text
        if self.snackbar.parent:
            self.snackbar.dismiss()
        self.snackbar.open()

    def open_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Delete this note?",
                type="confirmation",
                buttons=[
                    MDFlatButton(text="DELETE", on_release=self.delete_note),
                    MDFlatButton(text="CANCEL", on_release=self.close_dialog),
                ]
            )
        self.dialog.open()

    def close_dialog(self, *_):
        self.dialog.dismiss(force=True, animation=True)