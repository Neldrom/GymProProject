from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRoundFlatButton, MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel


class RoutineCard(MDCard):
    def __init__(self, routine, exercises_dict, delete_callback=None, start_callback=None, edit_button=None, Window=None, **kwargs):
        super().__init__(**kwargs)
        self.size = (Window.width - dp(40) * 0.7, dp(120))
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = dp(120)
        self.routine = routine

        first_row_box = MDBoxLayout(
            orientation='horizontal'
        )
        second_row_box = MDBoxLayout(
            orientation='horizontal'
        )
        self.add_widget(first_row_box)
        total_width = Window.width - dp(40) * 0.7
        first_row_box.add_widget(MDLabel(text=f"{routine.name}",
                                         padding=dp(20),
                                         pos_hint={"center_y": .5},
                                         width=(6 / 10 * total_width)))
        first_row_box.add_widget(MDRoundFlatButton(text="Start",
                                                   pos_hint={"center_y": .5},
                                                   width=(6 / 10 * total_width),
                                                   on_release=lambda x: start_callback(routine)))

        # Add delete button
        delete_button = MDIconButton(
            icon='trash-can',
            width=(1 / 10 * total_width),
            pos_hint={'center_y': 0.5},
            on_release=lambda x: delete_callback(routine),  # Call the delete_callback when the button is pressed
        )
        first_row_box.add_widget(delete_button)

        exercises_in_routine = routine.exercises_in_routine
        exercises_text = ''
        for a in exercises_in_routine:
            exercise = exercises_dict[a['exercise_id']]
            exercises_text += exercise['name'] + ", "

        exercises_text = exercises_text[:-2]
        if len(exercises_text) > 65:
            exercises_text = exercises_text[:65] + ".."

        second_row_box.add_widget(
            MDLabel(
                text=exercises_text,
                padding=(dp(20), dp(0)),
                opacity=0.5,
                size_hint_y=0.8,
                font_style="Caption"
            )
        )
        second_row_box.add_widget(
            MDIconButton(
                icon='pencil',
                width=(1 / 10 * total_width),
                pos_hint={'center_y': 0.5},
                on_release=lambda x: edit_button(routine),  # Call the delete_callback when the button is pressed
            )
        )
        self.add_widget(second_row_box)

