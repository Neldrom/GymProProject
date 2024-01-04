from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField


class ExerciseCard(MDBoxLayout):
    def __init__(self, exercise_name, num_sets=1, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spacing = 10
        self.height = dp(80)
        self.size_hint_y = None

        self.title = MDLabel(
            width=self.height,
            text=exercise_name,
            valign="center",
            pos_hint={'center_y': 0.5}
        )

        self.icon = MDIconButton(
            icon='trash-can',
            size_hint_x=None,
            valign="center",
            pos_hint={'center_y': 0.5}
        )

        self.set_input = MDTextField(
            text=str(num_sets),
            hint_text="Set",
            input_filter="int",
            pos_hint={'center_y': 0.5},
            max_text_length=3
        )

        self.add_widget(self.title)
        self.add_widget(self.set_input)
        self.add_widget(self.icon)

    def set_delete_button(self, func):
        self.icon.on_release = func

    def get_set_input_text(self):
        return self.set_input.text

