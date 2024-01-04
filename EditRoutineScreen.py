from kivy.metrics import dp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.screen import MDScreen
from kivymd.uix.textfield import MDTextField

from GymProProject.ExerciseCard import ExerciseCard
from GymProProject.User import Routine


class EditRoutineScreen(MDScreen):
    def __init__(self, db, Window=None, **kwargs):
        super().__init__(**kwargs)
        self.edit_state = False
        self.routine_to_edit = False
        self.selected_exercises = []
        self.ids.exercises_box.pos = (0, Window.height - dp(100))
        self.db = db
        self.exercises = db.exercises.find()
        self.body_parts = self.db.exercises.distinct("bodyPart")
        self.routine_name_textfield = MDTextField(
            text="",
            hint_text="Routine Name",
            size_hint=(0.8, None),
            pos_hint={"center_x": 0.5, "center_y": 0.9},
            max_text_length=24,
            multiline=False
        )
        self.ids.flayout.add_widget(self.routine_name_textfield)

    def on_pre_enter(self, *args):
        self.ids.exercises_box.clear_widgets()
        if self.selected_exercises:
            for exercise_info in self.selected_exercises:
                exercise_name = exercise_info['name'].title()
                num_sets = exercise_info.get('sets', 1)
                card = ExerciseCard(exercise_name, num_sets=num_sets)
                card.set_delete_button(lambda exercise=exercise_info, _card=card: self.delete_exercise(exercise, _card))
                self.ids.exercises_box.add_widget(card)
        self.add_button = MDRaisedButton(text="Add Exercise",
                                         padding=(100, 10),
                                         pos_hint={'center_x': 0.5},
                                         on_release=self.show_body_part_selection)
        self.ids.exercises_box.canvas.before.clear()
        self.ids.exercises_box.add_widget(self.add_button)

    def delete_exercise(self, exercise, card):
        self.selected_exercises.remove(exercise)
        self.ids.exercises_box.remove_widget(card)

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

    def back_button(self):
        self.manager.current = "main"

    def on_add_routine_button_press(self):
        exercises_in_routine = []
        cards = self.ids.exercises_box.children[1:]  # skip the button child
        if cards:
            for i in range(len(cards)):
                if isinstance(cards[i], ExerciseCard):
                    exercises_in_routine.append({
                        "exercise_id": self.selected_exercises[i]['id'],
                        "sets": str(cards[i].get_set_input_text())
                    })
        routine = Routine(self.routine_name_textfield.text, exercises_in_routine)
        m = self.manager.get_screen("main")
        if self.edit_state:
            m.delete_routine_card(self.routine_to_edit)
            self.edit_state = False
        m.db.users.update_one({"email": m.user.email},
                              {"$push": {"routines": routine.to_dict()}})
        m.load_user_exercises()
        m.add_routine_to_user(routine)
        self.reset()
        self.manager.current = 'main'

    def reset(self):
        self.routine_name_textfield.text = ''
        self.ids.exercises_box.clear_widgets()