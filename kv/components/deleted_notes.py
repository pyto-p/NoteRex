from kivymd.app import MDApp
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.label import MDIcon
from kivymd.uix.snackbar import Snackbar


class DeletedNotes(MDCardSwipe):
    """
    Represents the deleted notes of the user
    """
    def __init__(self, dashboard_card, bookmark_card, *args, **kwargs):
        # storing the deleted note cards
        self.dialog = None
        self.deleted_note = dashboard_card.note
        self.dashboard_card = dashboard_card
        self.bookmark_card = bookmark_card
        
        super().__init__(*args, **kwargs)
        self.app = MDApp.get_running_app()
        self.bookmark_icon = MDIcon(
            icon = "star",
            theme_text_color = "Custom",
            text_color = "#E79F48",
        )

        if self.deleted_note.is_bookmarked:
            self.add_bookmark_icon()

    def add_bookmark_icon(self):
        if not self.bookmark_icon.parent:
            self.ids["content"].add_widget(self.bookmark_icon)

    def view_card(self):
        # view card content only
        if self.open_progress == 1:
            self.change_screen("up", "edit_notes")
            self.app.screen_manager.get_screen("edit_notes").open_note("trash_bin", self.dashboard_card)

    def restore_note(self):
        # restore to dashboard and bookmarks if possible
        if self.bookmark_card:
            self.app.screen_manager.get_screen("bookmarks").add_note(self.bookmark_card)
        self.app.screen_manager.get_screen("dashboard").add_note(self.dashboard_card)
        self.app.screen_manager.get_screen("edit_notes").update_screens_notes_list()
        self.delete_note()
        Snackbar(text="Note restored.", duration=1).open()

    def delete_note(self, *_):
        if self.dialog:
            self.close_dialog()
        self.app.screen_manager.get_screen("trash_bin").permanent_delete_note(self)

    def open_dialog(self):
        if not self.dialog:
            self.dialog = MDDialog(
                title="Do you want to permanently delete this note?",
                type="confirmation",
                buttons=[
                    MDFlatButton(text="DELETE", on_release=self.delete_note),
                    MDFlatButton(text="CANCEL", on_release=self.close_dialog),
                ],
            )
        self.dialog.open()

    def close_dialog(self, *_):
        self.dialog.dismiss(force=True, animation=True)

    def change_screen(self, direction, next):
        self.app.screen_manager.transition.direction = direction
        self.app.screen_manager.current = next
