from functools import partial

from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen

from GymProProject.ClickableTwoLineListItem import ClickableTwoLineListItem


class BodyPartExercisesScreen(MDScreen):
    def __init__(self, exercises, **kwargs):
        super().__init__(**kwargs)
        self.exercises = exercises
        self.selected_exercises = []
        self.search_text = ""

    def on_pre_enter(self, *args):
        # Clear existing widgets
        self.ids.exercise_screen.clear_widgets()

        # Set scroll_y to 1 to keep it at the top
        self.ids.exercise_screen.scroll_y = 1

        # Add the exercises to the layout
        self.add_filtered_exercises()

    def add_filtered_exercises(self):
        # Filter exercises based on the search text
        filtered_exercises = [exercise for exercise in self.exercises if
                              self.search_text.lower() in exercise['name'].lower()]
        # Add filtered exercises to the layout
        for i, exercise in enumerate(filtered_exercises):
            # Create ClickableTwoLineListItem with dynamic height
            label = ClickableTwoLineListItem(exercise, i, self.on_label_touch, size_hint_y=None, height=dp(55))
            if i % 2 == 0:
                label.md_bg_color = (0, 0, 0, 0.55)

            info_button = MDRaisedButton(
                text="Info",
                size_hint_y=None,
                height="55dp",  # Set the same height as the label
                theme_text_color="Custom",
                text_color=(1, 1, 1, 1),
                on_release=partial(self.open_exercise, exercise),
            )
            info_button.pos_hint = {"center_y": 0.5}  # Center the button vertically

            # Create a BoxLayout for each row
            row_layout = MDBoxLayout(
                orientation="horizontal",
                size_hint_y=None,
                height=label.height,  # Set the same height for the row
                spacing=15  # Set the desired spacing between label and button
            )

            # Add widgets to the row layout
            row_layout.add_widget(label)
            row_layout.add_widget(info_button)

            # Add the row layout to the ScrollView
            self.ids.exercise_screen.add_widget(row_layout)

    def open_exercise(self, exercise, button_instance):
        screen = self.manager.get_screen("exercise_screen")
        screen.exercise = exercise
        screen.last_screen = "body_part_exercise"
        self.manager.current = "exercise_screen"

    def on_label_touch(self, exercise):
        if exercise not in self.selected_exercises:
            self.selected_exercises.append(exercise)
        else:
            self.selected_exercises.remove(exercise)

    def on_search_text_change(self, instance, value):
        # Update the search text and refresh the layout
        self.search_text = value
        self.on_pre_enter()

    def on_search_text_focus(self, instance, value):
        if not value:
            # If the search text is empty, reset the layout to show all exercises
            self.on_pre_enter()

    def back_button(self):
        self.manager.current = "edit_routine_screen"

    def on_add(self):
        sc = self.manager.get_screen('edit_routine_screen')
        for e in self.selected_exercises:
            sc.selected_exercises.append(e)
        self.manager.current = "edit_routine_screen"
        self.ids.exercise_screen.clear_widgets()
        # Set scroll_y back to 1 when clearing the widgets
        self.ids.exercise_screen.scroll_y = 1