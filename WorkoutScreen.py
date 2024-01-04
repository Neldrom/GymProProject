from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField
from kivy.uix.checkbox import CheckBox
from kivy.properties import NumericProperty, partial
from datetime import datetime
from GymProProject.User import Workout
from GymProProject.UserWorkoutCard import UserWorkoutCard


class WorkoutScreen(MDScreen):
    """
    Represents the screen for performing workouts and saving workout data.

    Attributes:
        volume_label_value (NumericProperty): Numeric property for volume label value.
        sets_label_value (NumericProperty): Numeric property for sets label value.

    Methods:
        __init__(db, **kwargs): Initializes a WorkoutScreen instance.
        load_workout_exercises(routine): Loads exercises for the given routine.
        end_workout(): Handles the end of the workout and saves workout data.
        back_button(): Navigates back to the main screen.
        reset(): Resets the volume and sets labels to zero.
    """

    volume_label_value = NumericProperty("0")
    sets_label_value = NumericProperty("0")

    def __init__(self, db, **kwargs):
        """
        Initializes a WorkoutScreen instance.

        Parameters:
            db: Database reference.
            **kwargs: Additional keyword arguments for MDScreen.
        """
        super().__init__(**kwargs)
        self.user = None
        self.exercise_dict = None
        self.title = None
        self.db = db

        self.volume_label = MDLabel(text=f"Volume: {self.volume_label_value}", halign="center")
        self.sets_label = MDLabel(text=f"Sets: {self.sets_label_value}", halign="center")

        self.ids.workout_current_info.add_widget(self.volume_label)
        self.ids.workout_current_info.add_widget(self.sets_label)

    def load_workout_exercises(self, routine):
        """
        Loads exercises for the given routine.

        Parameters:
            routine: Routine instance.
        """
        self.ids.top_bar.title = self.title
        self.ids.exercises_box.clear_widgets()
        for e in routine.exercises_in_routine:
            workout_card = WorkoutExerciseCard(e, self.exercise_dict[e['exercise_id']], screen_ref=self)
            self.ids.exercises_box.add_widget(workout_card)

    def end_workout(self):
        """
        Handles the end of the workout and saves workout data.
        """
        current_utc_time = datetime.utcnow()
        workout = Workout(date=current_utc_time, title=self.title)

        for child in self.ids.exercises_box.children:
            if isinstance(child, WorkoutExerciseCard):
                exercise_data = child.get_exercise_data()
                if len(exercise_data["sets"]) > 1:
                    workout.add_exercise(child.exercise_info["id"], exercise_data["sets"])

        workout_data = workout.to_dict()
        self.db.users.update_one(
            {"email": self.user.email},
            {"$push": {"workouts": workout_data}}
        )

        popup = Popup(title='Workout Saved',
                      content=MDLabel(text='Workout data has been saved.'),
                      size_hint=(None, None), size=(400, 200))
        popup.open()
        m = self.manager.get_screen('main')
        m.ids.statistics.clear_widgets()
        m.user.workouts.append(workout)
        m.add_user_workout_cards(m.user.workouts)
        m.update_statistics_graph(self.user.workouts)
        self.manager.current = "main"

    def back_button(self):
        """
        Navigates back to the main screen.
        """
        self.reset()
        self.manager.current = 'main'

    def reset(self):
        """
        Resets the volume and sets labels to zero.
        """
        self.volume_label_value = 0
        self.sets_label_value = 0
        self.volume_label.text = f"Volume: {self.volume_label_value}"
        self.sets_label.text = f"Sets: {self.sets_label_value}"


class WorkoutExerciseCard(MDCard):
    """
    Represents a card for a specific exercise in a workout.

    Attributes:
        ws (WorkoutScreen): Reference to the parent WorkoutScreen.
        exercise_info (dict): Exercise information.
        **kwargs: Additional keyword arguments for MDCard.

    Methods:
        __init__(exercise, exercise_info, screen_ref, **kwargs): Initializes a WorkoutExerciseCard instance.
        open_exercise(exercise, button_instance): Opens the exercise screen.
        get_exercise_data(): Retrieves exercise data from the card.
        checkbox_callback(checkbox, value): Callback method for the checkbox state change.
    """

    def __init__(self, exercise, exercise_info, screen_ref, **kwargs):
        """
        Initializes a WorkoutExerciseCard instance.

        Parameters:
            exercise (dict): Exercise details.
            exercise_info (dict): Exercise information.
            screen_ref (WorkoutScreen): Reference to the parent WorkoutScreen.
            **kwargs: Additional keyword arguments for MDCard.
        """
        super().__init__(**kwargs)
        self.ws = screen_ref
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.exercise_info = exercise_info

        row_height = dp(40)
        header_height = dp(40)
        sets_height = int(exercise["sets"]) * row_height
        self.height = header_height * 2 + sets_height

        title_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=header_height)
        title = MDLabel(text=exercise_info['name'].title(), halign="center", height=header_height)
        title_box.add_widget(title)
        info_button = MDRaisedButton(
            text="Info",
            size_hint_y=None,
            height="55dp",
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            on_release=partial(self.open_exercise, exercise_info),
        )
        info_button.pos_hint = {"center_y": 0.5}
        title_box.add_widget(info_button)
        self.add_widget(title_box)

        header_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=header_height)
        header_box.add_widget(MDLabel(text="Set", halign="center"))
        header_box.add_widget(MDLabel(text="kg", halign="center"))
        header_box.add_widget(MDLabel(text="Reps", halign="center"))
        header_box.add_widget(MDLabel(text="Check", halign="center"))
        self.add_widget(header_box)

        self.set_box = MDBoxLayout(orientation="vertical", id="set_box")
        self.add_widget(self.set_box)

        for i in range(int(exercise["sets"])):
            row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=row_height)
            row.add_widget(MDLabel(text=str(i + 1), halign="center"))
            md_textfield1 = MDTextField(halign="center", mode="round",
                                        input_filter="float", text="0")
            md_textfield2 = MDTextField(halign="center", mode="round",
                                        input_filter="int", text="0")
            row.add_widget(md_textfield1)
            row.add_widget(md_textfield2)
            checkbox = CheckBox()
            checkbox.bind(active=self.checkbox_callback)
            row.add_widget(checkbox)
            self.set_box.add_widget(row)

    def open_exercise(self, exercise, button_instance):
        """
        Opens the exercise screen.

        Parameters:
            exercise: Exercise details.
            button_instance: Button instance triggering the event.
        """
        screen = self.ws.manager.get_screen("exercise_screen")
        screen.exercise = exercise
        screen.last_screen = "workout_screen"
        self.ws.manager.current = "exercise_screen"

    def get_exercise_data(self):
        """
        Retrieves exercise data from the card.

        Returns:
            dict: Exercise data.
        """
        exercise_data = {
            "sets": []
        }

        for child in self.set_box.children:
            if isinstance(child, MDBoxLayout):
                try:
                    reps = int(child.children[1].text)
                    weight = float(child.children[2].text)
                    checked = child.children[0].active

                    if checked:
                        set_data = {
                            "reps": reps,
                            "weight": weight,
                        }
                        exercise_data["sets"].append(set_data)
                except IndexError as e:
                    print(f"IndexError: {e}")

        return exercise_data

    def checkbox_callback(self, checkbox, value):
        """
        Callback method for the checkbox state change.

        Parameters:
            checkbox: Checkbox widget.
            value: New state of the checkbox (True if checked, False if unchecked).
        """
        row = checkbox.parent
        volume = float(row.children[1].text) * float(row.children[2].text)
        if value:
            row.children[1].readonly = True
            row.children[2].readonly = True
            self.ws.volume_label_value = float(self.ws.volume_label_value) + volume
            self.ws.volume_label.text = f"Volume {self.ws.volume_label_value}"
            self.ws.sets_label_value = int(self.ws.sets_label_value) + 1
            self.ws.sets_label.text = f"Sets {self.ws.sets_label_value}"

        else:
            row.children[1].readonly = False
            row.children[2].readonly = False
            self.ws.volume_label_value = float(self.ws.volume_label_value) - volume
            self.ws.volume_label.text = f"Volume {self.ws.volume_label_value}"
            self.ws.sets_label_value = int(self.ws.sets_label_value) - 1
            self.ws.sets_label.text = f"Sets {self.ws.sets_label_value}"
