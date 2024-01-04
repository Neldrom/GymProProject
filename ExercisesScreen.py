from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen

from GymProProject.Tab import Tab


class ExercisesScreen(MDScreen):
    """
    ExercisesScreen class represents the screen for displaying exercise details.

    Attributes:
        db: Database instance.
        exercise (dict): Information about the current exercise.
        summary_layout: MDBoxLayout for the summary tab content.
        history_layout: MDBoxLayout for the history tab content.
        how_to_layout: MDBoxLayout for the "How to" tab content.
        last_screen (str): Name of the last screen visited.

    Methods:
        __init__(self, db, **kwargs):
            Initializes the ExercisesScreen.

        on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
            Handles the tab switch event and updates tab content accordingly.

        on_pre_enter(self):
            Method called before entering the screen. Updates UI elements with exercise details.

        back_button(self):
            Navigates back to the last visited screen.
    """

    def __init__(self, db, **kwargs):
        """
        Initializes the ExercisesScreen.

        Parameters:
            db: Database instance.
            **kwargs: Additional keyword arguments for MDScreen.
        """
        super().__init__(**kwargs)
        self.db = db
        self.exercise = {}
        self.summary_layout = MDBoxLayout()
        self.history_layout = MDBoxLayout()
        self.how_to_layout = MDBoxLayout()
        self.last_screen = ''


    def on_tab_switch(self, instance_tabs, instance_tab, instance_tab_label, tab_text):
        """
        Handles the tab switch event and updates tab content accordingly.

        Parameters:
            instance_tabs: MDTabs instance.
            instance_tab: MDFloatLayout representing the content of the current tab.
            instance_tab_label: Label of the current tab.
            tab_text: Text of the current tab.
        """
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
        """
        Method called before entering the screen. Updates UI elements with exercise details.
        """
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
        tab = Tab(title="How to")
        tab.add_widget(self.how_to_layout)
        self.ids.tabs.add_widget(tab)

    def back_button(self):
        """
        Navigates back to the last visited screen.
        """
        self.manager.current = self.last_screen
