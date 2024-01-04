from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextField
from kivy.uix.checkbox import CheckBox

class WorkoutExerciseCard(MDCard):
    def __init__(self, exercise, screen_ref, **kwargs):
        super().__init__(**kwargs)
        self.ws = screen_ref
        self.orientation = 'vertical'
        self.size_hint_y = None
        row_height = dp(40)
        header_height = dp(40)
        sets_height = int(exercise["sets"]) * row_height
        self.height = header_height + sets_height

        header_box = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=header_height)
        header_box.add_widget(MDLabel(text="Set", halign="center"))
        header_box.add_widget(MDLabel(text="Previous", halign="center"))
        header_box.add_widget(MDLabel(text="kg", halign="center"))
        header_box.add_widget(MDLabel(text="Reps", halign="center"))
        header_box.add_widget(MDLabel(text="Y", halign="center"))
        self.add_widget(header_box)

        set_box = MDBoxLayout(orientation="vertical", id="set_box")
        self.add_widget(set_box)

        for i in range(int(exercise["sets"])):
            print(exercise["sets"])
            row = MDBoxLayout(orientation="horizontal", size_hint_y=None, height=row_height)
            row.add_widget(MDLabel(text=str(i + 1), halign="center"))
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
            set_box.add_widget(row)

    def checkbox_callback(self, checkbox, value):
        row = checkbox.parent
        volume = float(row.children[1].text) * float(row.children[2].text)
        if value:
            row.children[1].readonly = True
            row.children[2].readonly = True
            self.ws.volume_label_value = str(float(self.ws.volume_label_value) + volume)
            self.ws.sets_label_value = str(int(self.ws.sets_label_value) + 1)
        else:
            row.children[1].readonly = False
            row.children[2].readonly = False
            self.ws.volume_label_value = str(float(self.ws.volume_label_value) - volume)
            self.ws.sets_label_value = str(int(self.ws.sets_label_value) - 1)
