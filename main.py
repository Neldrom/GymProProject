from collections import defaultdict
from datetime import datetime as dt
from math import sin
from statistics import mean

import matplotlib
import numpy as np
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy_garden.graph import Graph, MeshLinePlot
from kivymd.uix.boxlayout import MDBoxLayout

from GymProProject.BodyPartExercisesScreen import BodyPartExercisesScreen
from GymProProject.EditRoutineScreen import EditRoutineScreen
from GymProProject.ExercisesScreen import ExercisesScreen
from GymProProject.RoutineCard import RoutineCard
from GymProProject.UserWorkoutCard import UserWorkoutCard
from GymProProject.WorkoutScreen import WorkoutScreen
from User import *
from kivy.metrics import dp
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from pymongo_get_database import get_database
from kivymd.uix.button import MDRaisedButton
from kivy_garden.graph import Graph, MeshLinePlot
from matplotlib.dates import date2num

Window.size = 360, 640


class MainScreen(MDScreen):
    def __init__(self, db, exercises, **kwargs):
        super().__init__(**kwargs)
        self.exercises = exercises
        self.db = db
        self.user = None
        self.loaded = False

    def update_statistics_graph(self, workouts):
        if len(workouts) == 0:
            return

        date_volumes = defaultdict(float)  # Accumulate volumes for each date

        for workout in workouts:
            for exercise in workout.exercises:
                date = date2num(workout.date)
                volume = sum(set_data['reps'] * set_data['weight'] for set_data in exercise['sets'])
                date_volumes[date] += volume

        dates, volumes = zip(*date_volumes.items())

        xmin_number = min(dates).item()
        xmax_number = max(dates).item()
        tick = (xmax_number - xmin_number) / 4

        graph = Graph(xlabel='Date', ylabel='Volume',
                      x_ticks_major=tick, y_ticks_major=max(volumes) / 2,
                      y_grid_label=True, padding=5,
                      x_grid=True, xmin=xmin_number, xmax=xmax_number, ymin=0, ymax=max(volumes))

        plot = MeshLinePlot(color=[1, 0, 0, 1])
        plot.points = [(date, volume) for date, volume in zip(dates, volumes)]
        graph.add_plot(plot)

        self.ids.statistics.add_widget(graph)

    def update_user_data(self, user):
        self.user = user
        print(f"User {user.name} successfully logged in.")
        self.exercises_dict = {}
        if not self.loaded:
            self.load_user_exercises()
            self.RoutineScreen()
            self.PastWorkoutsScreen()
            self.loaded = True

    def load_user_exercises(self):
        user_routines = self.user.routines
        for routine in user_routines:
            for exercise in routine.exercises_in_routine:
                exercise_id = exercise['exercise_id']
                self.exercises_dict[exercise_id] = self.db.exercises.find_one({'id': exercise_id})
        for workout in self.user.workouts:
            for exercise in workout.exercises:
                exercise_id = exercise['exercise_id']
                if exercise_id not in self.exercises_dict:
                    self.exercises_dict[exercise_id] = self.db.exercises.find_one({'id': exercise_id})

    def on_add_routine_button_press(self):
        self.manager.get_screen('edit_routine_screen').reset()
        self.manager.current = 'edit_routine_screen'

    def create_routine_card(self, routine):
        routine_layout = self.ids.routine_layout
        routine_card = RoutineCard(routine=routine, exercises_dict=self.exercises_dict,
                                   delete_callback=self.delete_routine_card, edit_button=self.edit_routine_card,
                                   start_callback=self.start_workout, Window=Window)
        routine_layout.add_widget(routine_card)

    def start_workout(self, routine):
        ws = self.manager.get_screen("workout_screen")
        ws.exercise_dict = self.exercises_dict
        ws.title = routine.name
        ws.load_workout_exercises(routine)
        self.manager.current = "workout_screen"

    def add_routine_to_user(self, routine):
        self.user.routines.append(routine)
        self.load_user_exercises()
        self.create_routine_card(routine)

    def delete_routine_card(self, routine):
        self.user.routines.remove(routine)

        self.ids.routine_layout.clear_widgets()
        for updated_routine in self.user.routines:
            self.create_routine_card(updated_routine)

        self.db.users.update_one({"email": self.user.email}, {"$pull": {"routines": {"name": routine.name}}})

    def edit_routine_card(self, routine):
        sc = self.manager.get_screen("edit_routine_screen")
        exercise_list = []
        for exercise in routine.exercises_in_routine:
            a = self.exercises_dict[exercise["exercise_id"]]
            a["sets"] = exercise['sets']
            exercise_list.append(a)
        sc.routine_to_edit = routine
        sc.selected_exercises = exercise_list
        sc.edit_state = True
        sc.routine_name_textfield.text = routine.name
        sc.manager.current = "edit_routine_screen"

    def RoutineScreen(self):
        if self.user:
            routine_layout = self.ids.routine_layout
            if routine_layout.children:
                return
            user_routines = self.user.routines
            self.routine_layout_width = Window.width - dp(40)

            for routine in user_routines:
                self.create_routine_card(routine)

        else:
            print("User data not found")

    def add_user_workout_cards(self, workouts):
        self.ids.workouts.clear_widgets()

        for updated_workout in reversed(workouts):
            self.ids.workouts.add_widget(UserWorkoutCard(updated_workout,
                                                         self.exercises_dict,
                                                         self.delete_workout_card))

    def delete_workout_card(self, workout):
        self.user.workouts.remove(workout)

        self.add_user_workout_cards(self.user.workouts)

        self.db.users.update_one({"email": self.user.email}, {"$pull": {"workouts": {"date": workout.date}}})
        self.ids.statistics.clear_widgets()
        self.update_statistics_graph(self.user.workouts)

    def PastWorkoutsScreen(self):
        self.update_statistics_graph(self.user.workouts)

        self.ids.profile_name.text = self.user.name
        self.add_user_workout_cards(self.user.workouts)

class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class LoginScreen(MDScreen):
    def __init__(self, db, main_screen, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.main_screen = main_screen
        self.email_input = MDTextField(hint_text="Email", pos_hint={'center_x': 0.5, 'center_y': 0.7},
                                       size_hint=(0.8, None), height=dp(40))
        self.password_input = MDTextField(hint_text="Password", password=True,
                                          pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                          size_hint=(0.8, None), height=dp(40))
        self.login_button = MDRaisedButton(text="Login", pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                           on_release=self.on_login)
        self.register_button = MDRaisedButton(text="Register", pos_hint={'center_x': 0.5, 'center_y': 0.4},
                                              on_release=self.on_register_button)
        self.add_widget(self.email_input)
        self.add_widget(self.password_input)
        self.add_widget(self.login_button)
        self.add_widget(self.register_button)

    def on_login(self, *args):
        email = self.email_input.text
        password = self.password_input.text

        # change to variables
        user_data = self.db.users.find_one({'email': email, 'password': password})

        if user_data:
            user = User.from_dict(user_data)

            self.manager.get_screen("edit_routine_screen").user = user
            self.manager.get_screen("workout_screen").user = user

            self.main_screen.update_user_data(user)
            self.manager.current = 'main'
        else:
            # Display an error message or handle unsuccessful login
            print("Login failed. Invalid credentials.")

    def on_register_button(self, *args):
        # Switch to the register screen
        self.manager.current = 'register'


class RegisterScreen(MDScreen):
    def __init__(self, db, main_screen, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.main_screen = main_screen
        self.name_input = MDTextField(hint_text="Name", pos_hint={'center_x': 0.5, 'center_y': 0.8},
                                      size_hint=(0.8, None), height=dp(40))
        self.email_input = MDTextField(hint_text="Email", pos_hint={'center_x': 0.5, 'center_y': 0.7},
                                       size_hint=(0.8, None), height=dp(40))
        self.password_input = MDTextField(hint_text="Password", password=True,
                                          pos_hint={'center_x': 0.5, 'center_y': 0.6},
                                          size_hint=(0.8, None), height=dp(40))
        self.register_button = MDRaisedButton(text="Register", pos_hint={'center_x': 0.5, 'center_y': 0.5},
                                              on_release=self.on_register)
        self.add_widget(self.name_input)
        self.add_widget(self.email_input)
        self.add_widget(self.password_input)
        self.add_widget(self.register_button)

    def on_register(self, *args):
        name = self.name_input.text
        email = self.email_input.text
        password = self.password_input.text

        # You might want to add more validation for the input fields

        # Insert the new user into the database
        user_data = {
            'name': name,
            'email': email,
            'password': password,
            'routines': [],
            'workouts': []
        }

        # Insert the user into the database
        result = self.db.users.insert_one(user_data)

        if result.inserted_id:
            # Registration successful, you can redirect to the login screen or main screen
            self.manager.current = 'login'
        else:
            # Display an error message or handle unsuccessful registration
            print("Registration failed.")


class GymProApp(MDApp):
    def __init__(self):
        super().__init__()
        self.db = get_database()
        self.exercises = self.db.exercises.find()

    def build(self):
        Builder.load_file("GymPro.kv")
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"
        main_screen = MainScreen(name='main', db=self.db, exercises=self.exercises)
        # Create LoginScreen and pass the main_screen reference
        login_screen = LoginScreen(name='login', db=self.db, main_screen=main_screen)

        screen_manager = ScreenManager()
        screen_manager.add_widget(login_screen)
        screen_manager.add_widget(EditRoutineScreen(name='edit_routine_screen', db=self.db, Window=Window))
        screen_manager.add_widget(BodyPartExercisesScreen(name="body_part_exercise", exercises=self.exercises))
        screen_manager.add_widget(main_screen)
        screen_manager.add_widget(RegisterScreen(name='register', db=self.db, main_screen=main_screen))
        screen_manager.add_widget(WorkoutScreen(name="workout_screen", db=self.db))
        screen_manager.add_widget(ExercisesScreen(name='exercise_screen', db=self.db))

        return screen_manager


# Run the app
if __name__ == '__main__':
    GymProApp().run()
