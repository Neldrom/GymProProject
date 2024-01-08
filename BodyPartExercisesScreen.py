# Import necessary modules and classes
from functools import partial
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.screen import MDScreen

# Import custom ClickableTwoLineListItem class
from GymProProject.ClickableTwoLineListItem import ClickableTwoLineListItem


class BodyPartExercisesScreen(MDScreen):
    """
    BodyPartExercisesScreen class represents the screen for displaying and selecting exercises
    related to a specific body part in a fitness application.

    Attributes:
        exercises (list): List of exercises to display.
        selected_exercises (list): List to store selected exercises.
        search_text (str): Text used for filtering exercises.

    Methods:
        on_pre_enter(self, *args):
            Method called before entering the screen. Clears existing widgets and adds filtered exercises.

        add_filtered_exercises(self):
            Adds filtered exercises to the layout based on the search text.

        open_exercise(self, exercise, button_instance):
            Navigates to the exercise screen with detailed information for the selected exercise.

        on_label_touch(self, exercise):
            Handles the touch event on ClickableTwoLineListItem to select or deselect an exercise.

        on_search_text_change(self, instance, value):
            Updates the search text and refreshes the layout.

        on_search_text_focus(self, instance, value):
            Resets the layout to show all exercises when the search text is empty.

        back_button(self):
            Navigates back to the "edit_routine_screen."

        on_add(self):
            Adds selected exercises to the "edit_routine_screen" and navigates back to it.
    """

    def __init__(self, exercises, **kwargs):
        super().__init__(**kwargs)
        self.exercises = exercises
        self.selected_exercises = []
        self.search_text = ""

    def on_pre_enter(self, *args):
        """
        Method called before entering the screen.
        Clears existing widgets and adds filtered exercises.
        """
        self.ids.exercise_screen.clear_widgets()
        # Set scroll_y to 1 to keep it at the top
        self.ids.exercise_screen.scroll_y = 1
        self.add_filtered_exercises()

    def add_filtered_exercises(self):
        """
        Adds filtered exercises to the layout based on the search text.
        """
        filtered_exercises = [exercise for exercise in self.exercises if
                              self.search_text.lower() in exercise['name'].lower()]
        # Add filtered exercises to the layout
        for i, exercise in enumerate(filtered_exercises):
            # Create ClickableTwoLineListItem with dynamic height
            label = ClickableTwoLineListItem(exercise, i, self.on_label_touch, size_hint_y=None, height=dp(55))
            if i % 2 == 0:
                label.md_bg_color = (0, 0, 0, 0.55)

            # Create an "Info" button for each exercise
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
        """
        Navigates to the exercise screen with detailed information for the selected exercise.

        Parameters:
            exercise (dict): Selected exercise information.
            button_instance: Button instance triggering the navigation.
        """
        screen = self.manager.get_screen("exercise_screen")
        screen.exercise = exercise
        screen.last_screen = "body_part_exercise"
        self.manager.current = "exercise_screen"

    def on_label_touch(self, exercise):
        """
        Handles the touch event on ClickableTwoLineListItem to select or deselect an exercise.

        Parameters:
            exercise (dict): Selected exercise information.
        """
        if exercise not in self.selected_exercises:
            self.selected_exercises.append(exercise)
        else:
            self.selected_exercises.remove(exercise)

    def on_search_text_change(self, instance, value):
        """
        Updates the search text and refreshes the layout.

        Parameters:
            instance: The TextInput instance.
            value (str): New search text.
        """
        # Update the search text and refresh the layout
        self.search_text = value
        self.on_pre_enter()

    def on_search_text_focus(self, instance, value):
        """
        Resets the layout to show all exercises when the search text is empty.

        Parameters:
            instance: The TextInput instance.
            value (bool): Focus state.
        """
        if not value:
            # If the search text is empty, reset the layout to show all exercises
            self.on_pre_enter()

    def back_button(self):
        """
        Navigates back to the "edit_routine_screen."
        """
        self.manager.current = "edit_routine_screen"

    def on_add(self):
        """
        Adds selected exercises to the "edit_routine_screen" and navigates back to it.
        Clears existing widgets and sets scroll_y back to 1 when clearing the widgets.
        """
        sc = self.manager.get_screen('edit_routine_screen')
        for e in self.selected_exercises:
            sc.selected_exercises.append(e)
        self.manager.current = "edit_routine_screen"
        self.ids.exercise_screen.clear_widgets()
        self.ids.exercise_screen.scroll_y = 1
