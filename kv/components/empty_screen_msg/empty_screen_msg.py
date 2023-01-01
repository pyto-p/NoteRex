from kivymd.uix.boxlayout import MDBoxLayout

from kivy.properties import StringProperty


class EmptyScreenMessage(MDBoxLayout):
    img_path = StringProperty()
    message = StringProperty()