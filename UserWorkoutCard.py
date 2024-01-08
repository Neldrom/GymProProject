from datetime import datetime

import pytz
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from tzlocal import get_localzone


class UserWorkoutCard(MDBoxLayout):
    """
    Represents a card displaying information about a user's workout.

    Attributes:
        workout (Workout): The workout object containing details.
        exercise_dict (dict): Dictionary containing exercise details.
        delete_callback (function): Callback function to delete the workout.

    Methods:
        __init__(workout, exercise_dict, delete_callback, **kwargs): Initializes the UserWorkoutCard instance.
    """

    def __init__(self, workout, exercise_dict, delete_callback, **kwargs):
        """
        Initializes a UserWorkoutCard.

        Parameters:
            workout (Workout): The workout object containing details.
            exercise_dict (dict): Dictionary containing exercise details.
            delete_callback (function): Callback function to delete the workout.
            **kwargs: Additional keyword arguments for MDCard.
        """
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.adaptive_height = True
        self.workout = workout
        self.md_bg_color = (0, 0, 0, .5)
        self.radius = 15
        local_timezone = get_localzone()
        local_date = workout.date.replace(tzinfo=pytz.UTC).astimezone(local_timezone)

        # First Row - Date
        first_row_box = MDBoxLayout(orientation="horizontal", padding=10, adaptive_height = True)
        first_row_box.add_widget(
            MDLabel(text=f"{workout.title}    ||     {local_date.strftime('%m/%d/%Y, %H:%M:%S')}",
                    halign="center", adaptive_height=True, pos_hint={'center_y': 0.5}))
        delete_button = MDIconButton(
            icon='trash-can',
            pos_hint={'center_y': 0.5},
            on_release=lambda x: delete_callback(self.workout),
        )
        first_row_box.add_widget(delete_button)

        # Second Row - Volume and Sets
        second_row_box = MDBoxLayout(orientation="horizontal", padding=10, adaptive_height=True)

        # Exercises Layout
        exercises_layout = MDBoxLayout(orientation="vertical", spacing=10, padding=10, adaptive_height=True)

        volume = 0
        sets = 0
        ex_height = 0

        # Loop through exercises in the workout
        for e in workout.exercises:
            exercise = exercise_dict[e["exercise_id"]]
            exercise_label = MDLabel(text=f"{exercise['name'].title()}", theme_text_color="Primary", font_style="H6",
                                     adaptive_height=True)

            set_info_layout = MDBoxLayout(orientation="vertical", adaptive_height = True)
            set_info_layout.add_widget(exercise_label)
            set_height = dp(30)

            # Loop through sets in each exercise
            for set_data in e['sets']:
                reps = set_data["reps"]
                weight = set_data["weight"]
                set_info = MDLabel(text=f"Reps: {reps}, Weight: {weight}", theme_text_color="Secondary",
                                   adaptive_height=True)
                set_info_layout.add_widget(set_info)
                volume += weight * reps
                sets += 1
                set_height += dp(30)

            set_info_layout.height = set_height
            ex_height += set_height
            exercises_layout.add_widget(set_info_layout)

        second_row_box.add_widget(MDLabel(text=f"Volume: {str(volume)}", theme_text_color="Secondary",
                                          adaptive_height=True))
        second_row_box.add_widget(MDLabel(text=f"Sets: {str(sets)}", theme_text_color="Secondary",
                                          adaptive_height=True))

        # Adding content to the card
        self.add_widget(first_row_box)
        self.add_widget(second_row_box)
        self.add_widget(exercises_layout)
        exercises_layout.height = ex_height  # Adjust the proportion as needed
        self.height = first_row_box.height + second_row_box.height + exercises_layout.height
