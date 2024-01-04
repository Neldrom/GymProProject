from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from GymProProject.Tab import Tab


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
        self.ids.top_bar.title = self.exercise['name'].title()
        self.summary_layout.clear_widgets()
        self.summary_layout = MDFloatLayout(orientation="vertical")
        self.summary_layout.add_widget(MDLabel(text="Summary Content"))
        self.history_layout.clear_widgets()
        self.history_layout = MDFloatLayout(orientation="vertical")
        self.history_layout.add_widget(MDLabel(text="History Content"))
        self.how_to_layout.clear_widgets()
        self.how_to_layout = MDFloatLayout(orientation="vertical", size_hint=(1, 1))
        instruction_list = MDBoxLayout(orientation="vertical", size_hint_y=0.9, pos_hint={"top": 0.9},
                                       spacing=10, padding=10)
        for i in range(len(self.exercise['instructions'])):
            instruction_text = f"{i + 1}. {self.exercise['instructions'][i]}"
            list_item = MDLabel(text=instruction_text, padding=10)
            instruction_list.add_widget(list_item)
        self.how_to_layout.add_widget(instruction_list)
        self.ids.tabs.switch_tab("Summary")

    def back_button(self):
        self.manager.current = self.last_screen
