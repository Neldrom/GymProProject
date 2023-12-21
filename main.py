from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.list import MDList, OneLineListItem, TwoLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.segmentedcontrol import MDSegmentedControlItem, MDSegmentedControl
from kivymd.uix.textfield import MDTextField
from kivy.core.window import Window
from pymongo_get_database import get_database
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock
from kivymd.uix.tab import MDTabsBase

Window.size = 360, 640


class Tab(MDFloatLayout, MDTabsBase):
    pass


class ExercisesScreen(MDScreen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.exercise = {}
        self.summary_layout = MDBoxLayout()
        self.history_layout = MDBoxLayout()
        self.how_to_layout = MDBoxLayout()
        self.last_screen = ''
        self.ids.tabs.add_widget(Tab(title="Summary"))
        self.ids.tabs.add_widget(Tab(title="History"))
        self.ids.tabs.add_widget(Tab(title="How to"))

    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        if tab_text == "Summary":
            instance_tab.clear_widgets()
            instance_tab.add_widget(self.summary_layout)
        elif tab_text == "History":
            instance_tab.clear_widgets()
            instance_tab.add_widget(self.history_layout)
        elif tab_text == "How to":
            instance_tab.clear_widgets()
            instance_tab.add_widget(self.how_to_layout)

    def on_pre_enter(self):
        self.summary_layout.clear_widgets()
        self.summary_layout = MDFloatLayout(orientation="vertical")
        self.summary_layout.add_widget(MDLabel(text="Summary Content"))
        self.history_layout.clear_widgets()
        self.history_layout = MDFloatLayout(orientation="vertical")
        self.history_layout.add_widget(MDLabel(text="History Content"))
        self.how_to_layout.clear_widgets()
        self.how_to_layout = MDFloatLayout(orientation="vertical", size_hint=(1, 1))
        self.how_to_layout.add_widget(MDLabel(text=f"{self.exercise['name'].title()}", size_hint_y=0.1,
                                              pos_hint={"y": 0.85}, halign="left", padding=20)
                                      )
        list = MDBoxLayout(orientation="vertical", size_hint_y=0.8, pos_hint={"top": 0.85},
                           spacing=10, padding=10)
        for i in range(len(self.exercise['instructions'])):
            instruction_text = f"{i + 1}. {self.exercise['instructions'][i]}"
            list_item = MDLabel(text=instruction_text, padding=10)
            list.add_widget(list_item)
        self.how_to_layout.add_widget(list)
        self.ids.tabs.switch_tab("Summary")

    def back_button(self):
        self.manager.current = self.last_screen


class BodyPartExercisesScreen(MDScreen):
    def __init__(self, exercises, **kwargs):
        super().__init__(**kwargs)
        self.exercises = exercises
        self.exercise_index = 0

    def on_pre_enter(self, *args):
        self.ids.exercise_screen.clear_widgets()
        self.exercises_list = list(self.exercises)
        self.exercise_index = 0
        # Set scroll_y to 1 to keep it at the top
        self.ids.exercise_screen.scroll_y = 1
        self.add_next_exercise(1)
        Clock.schedule_interval(self.add_next_exercise, 1)

    def add_next_exercise(self, dt):
        for i in range(0, 15):
            if self.exercise_index < len(self.exercises_list):
                exercise = self.exercises_list[self.exercise_index]
                label = MDLabel(text=f"{exercise['name'].title()}", size_hint_y=None)
                if self.exercise_index % 2 == 0:
                    label.md_bg_color = (0, 0, 0, 0.55)
                # Bind the touch event to a new function
                label.bind(on_touch_down=lambda instance, touch, exercise=exercise: self.on_label_touch(instance, touch,
                                                                                                        exercise))

                self.ids.exercise_screen.add_widget(label)
                self.exercise_index += 1
            else:
                Clock.unschedule(self.add_next_exercise)
                # Adjust scroll_y after adding items
                self.ids.exercise_screen.scroll_y = 0

    def on_label_touch(self, instance, touch, exercise):
        if instance.collide_point(*touch.pos):
            self.open_exercise(exercise, touch)

    def open_exercise(self, exercise, touch):
        screen = self.manager.get_screen("exercise_screen")
        screen.exercise = exercise
        screen.last_screen = 'body_part_exercise'
        self.manager.current = "exercise_screen"

    def on_add(self):
        self.manager.current = "edit_routine_screen"
        Clock.unschedule(self.add_next_exercise)
        self.ids.exercise_screen.clear_widgets()
        # Set scroll_y back to 1 when clearing the widgets
        self.ids.exercise_screen.scroll_y = 1



class EditRoutineScreen(MDScreen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.ids.edit_routine_layout.pos = (0, Window.height - dp(100))
        self.db = db
        self.exercises = db.exercises.find()
        self.body_parts = self.db.exercises.distinct("bodyPart")
        self.add_button = MDRaisedButton(text="Add Exercise", padding=(100, 10), pos_hint={'center_x': 0.5}
                                         , on_release=self.show_body_part_selection)
        self.ids.edit_routine_layout.add_widget(MDTextField(hint_text="Routine Name"))
        self.ids.edit_routine_layout.add_widget(self.add_button)

    def show_body_part_selection(self, *args):
        self.menu = MDDropdownMenu(
            caller=self.add_button,
            width_mult=4,
        )
        for body_part in self.body_parts:
            self.menu.items.append(
                {
                    "text": f'{body_part.title()}',
                    "viewclass": "OneLineListItem",
                    "height": dp(46),
                    "on_release": lambda x=body_part: self.menu_callback(x),
                }
            )
        self.menu.open()

    def menu_callback(self, body_part, *args):
        body_part_exercises = list(self.db.exercises.find({"bodyPart": body_part}))
        screen_instance = self.manager.get_screen('body_part_exercise')
        if screen_instance:
            screen_instance.exercises = body_part_exercises
        self.menu.dismiss()
        self.manager.current = 'body_part_exercise'

    def on_add_routine_button_press(self):
        self.manager.current = 'main'


class MainScreen(MDScreen):
    def __init__(self, db, **kwargs):
        super().__init__(**kwargs)
        self.db = db
        self.user_id = 'nikimev01@gmail.com'
        self.user_data = self.db.users.find_one({'email': self.user_id})
        self.bind(on_enter=self.RoutineScreen)
        self.exercises_dict = {}
        self.load_user_exercises()

    def load_user_exercises(self):
        user_routines = self.user_data['routines']
        for routine in user_routines:
            for exercise in routine['exercises_in_routine']:
                exercise_id = exercise['exercise_id']
                self.exercises_dict[exercise_id] = self.db.exercises.find_one({'id': exercise_id})

    def on_add_routine_button_press(self):
        self.manager.current = 'edit_routine_screen'

    def RoutineScreen(self, *args):
        if self.user_data:
            self.ids.routine_scroll_view.clear_widgets()
            user_routines = self.user_data.get('routines', [])
            self.routine_layout_width = Window.width - dp(40)
            routine_layout = MDGridLayout(
                size=(self.routine_layout_width, dp(340)),
                cols=1,
                spacing=dp(20),
                padding=dp(20),
                pos=(Window.width / 2 - self.routine_layout_width / 2, Window.height / 2 - dp(120)),
            )
            self.ids.routine_scroll_view.add_widget(routine_layout)
            for routine in user_routines:
                routine_card = MDCard(size=(self.routine_layout_width * 0.7, dp(120)), elevation=3,
                                      orientation='vertical', size_hint_y=None,
                                      height=dp(120))
                first_row_box = MDGridLayout(orientation='lr-tb', cols=2, spacing=dp(20), padding=dp(20),
                                             size=(self.routine_layout_width * 0.7, dp(60)))
                routine_card.add_widget(first_row_box)
                first_row_box.add_widget(MDLabel(text=f"{routine['name']}"))
                first_row_box.add_widget(MDRaisedButton(text="Start Routine", size_hint_x=None, width=dp(120)))
                exercises_in_routine = routine['exercises_in_routine']
                exercises_text = ''
                for a in exercises_in_routine:
                    exercise = self.exercises_dict[a['exercise_id']]
                    exercises_text += exercise['name'] + ", "
                exercises_text = exercises_text[:-2]
                if len(exercises_text) > 65:
                    exercises_text = exercises_text[:65] + ".."
                routine_card.add_widget(MDLabel(text=exercises_text, padding=(dp(20), dp(0)), opacity=0.5,
                                                size_hint_y=0.8,
                                                text_size=(self.routine_layout_width * 0.7 - dp(40), None)))
                routine_layout.add_widget(routine_card)
        else:
            print("User data not found")


class ProfileScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class GymProApp(MDApp):
    def __init__(self):
        super().__init__()
        self.db = get_database()
        self.exercises = self.db.exercises.find()

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.theme_style = "Dark"

        screen_manager = ScreenManager()
        screen_manager.add_widget(EditRoutineScreen(name='edit_routine_screen', db=self.db))
        screen_manager.add_widget(BodyPartExercisesScreen(name="body_part_exercise", exercises=self.exercises))
        screen_manager.add_widget(MainScreen(name='main', db=self.db))
        screen_manager.add_widget(ExercisesScreen(name='exercise_screen', db=self.db))

        return screen_manager


if __name__ == '__main__':
    GymProApp().run()
