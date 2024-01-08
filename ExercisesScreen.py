import webbrowser

import pytz
from kivy.metrics import dp
from kivy.uix.image import AsyncImage, Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDRoundFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.tab import MDTabsBase
from tzlocal import get_localzone
from kivy.network.urlrequest import UrlRequest

from GymProProject.Tab import Tab

import requests

headers = {
    "X-RapidAPI-Key": "e37565dbcamsh675ac36172f4b4ep126430jsn710a482feaad",
    "X-RapidAPI-Host": "exercisedb.p.rapidapi.com"
}


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
        self.user = None
        self.image = None
        self.summary_layout = MDFloatLayout(orientation="vertical", size_hint=(1, 1))
        self.history_layout = MDFloatLayout(orientation="vertical", size_hint=(1, 1))
        self.how_to_layout = MDFloatLayout(orientation="vertical", size_hint=(1, 1))

        self.last_screen = ''
        tab = Tab(title="How to")
        tab.add_widget(self.how_to_layout)
        self.ids.tabs.add_widget(tab)
        self.ids.tabs.add_widget(Tab(title="Summary"))
        self.ids.tabs.add_widget(Tab(title="History"))

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

        # Update the content of existing layouts without recreating them
        self.summary_layout.clear_widgets()

        summery_box = MDBoxLayout(orientation="vertical", spacing=10, padding=10, md_bg_color=(0, 0, 0, .5),
                                  radius=15, pos_hint={"top": 1}, adaptive_height=True)

        summery_box.add_widget(MDLabel(text=f"Equipment: {self.exercise['equipment'].title()}",
                                       adaptive_height=True))

        summery_box.add_widget(MDLabel(text=f"Target: {self.exercise['target'].title()}",
                                       adaptive_height=True))

        secondary_box = MDBoxLayout(orientation="horizontal", adaptive_height=True)
        secondary_box.add_widget(MDLabel(text="Secondary: ", adaptive_size=True))
        muscles = MDBoxLayout(orientation="vertical")
        for muscle in self.exercise["secondaryMuscles"]:
            muscles.add_widget(MDLabel(text=f"{muscle.title()}", adaptive_height=True))
        secondary_box.add_widget(muscles)

        summery_box.add_widget(secondary_box)
        summery_box.add_widget(MDRoundFlatButton(text='GIF', size=(200, 50), size_hint=(None, None),
                                                 pos_hint={"center_x": .5}, on_press=self.link_open))
        self.summary_layout.add_widget(summery_box)

        self.history_layout.clear_widgets()

        # Set up the MDScrollView
        history_scroll_view = MDScrollView(
            bar_width=0,
            bar_width_x=0,
            do_scroll_y=True,
            do_scroll_x=False,
            size_hint=(1, 1),
            scroll_x=0
        )

        # Set up the MDBoxLayout to contain workout cards
        history_box = MDBoxLayout(orientation="vertical", spacing=10, padding=10, adaptive_height=True)
        # Add workout cards to the MDBoxLayout

        for workout in self.user.get_exercise_history(self.exercise['id']):
            workout_card = MDBoxLayout(orientation="vertical", adaptive_height=True, md_bg_color=(0, 0, 0, .5),
                                       radius=15, padding=10)
            workout_card.add_widget(MDLabel(text=workout["title"], adaptive_height=True, padding=(10, 5)))
            local_timezone = get_localzone()
            local_date = workout["date"].replace(tzinfo=pytz.UTC).astimezone(local_timezone)
            workout_card.add_widget(
                MDLabel(adaptive_height=True, padding=(10, 5), text=str(local_date.strftime('%m/%d/%Y, %H:%M:%S'))))
            set_num = 0
            for set in workout["sets"]:
                set_num += 1
                workout_card.add_widget(MDLabel(text=f"{set_num}. {set['weight']} kg x {set['reps']} reps",
                                                adaptive_height=True, padding=(10, 5)))
            history_box.add_widget(workout_card)
        if len(history_box.children) == 0:
            history_box.add_widget(MDLabel(text="No history for this exercise", adaptive_height=True, padding=(10, 5)))
        # Add the MDBoxLayout to the MDScrollView
        history_scroll_view.add_widget(history_box)

        # Add the MDScrollView to the parent layout
        self.history_layout.add_widget(history_scroll_view)
        self.how_to_layout.clear_widgets()
        instruction_list = MDBoxLayout(orientation="vertical", size_hint_y=0.9, pos_hint={"top": 1},
                                       spacing=10, padding=10)
        for i in range(len(self.exercise['instructions'])):
            instruction_text = f"{i + 1}. {self.exercise['instructions'][i]}"
            list_item = MDLabel(text=instruction_text, padding=10)
            instruction_list.add_widget(list_item)
        self.how_to_layout.add_widget(instruction_list)

        # Set the default tab to "How to"
        default_tab_text = "How to"
        self.ids.tabs.switch_tab(default_tab_text)

    def link_open(self, instance):
        url = "https://exercisedb.p.rapidapi.com/exercises/name/{}".format(self.exercise['name'].replace(" ", "%20"))
        print(url)
        response = requests.get(url, headers=headers)
        response = response.json()
        webbrowser.open(response[0]['gifUrl'])

    def on_success(self, request, result):
        gif_url = result[0]['gifUrl'] if result else None
        if gif_url:
            # Update the AsyncImage source with the retrieved GIF URL
            self.summary_layout.children[1].texture.source = gif_url
        else:
            # Handle the case where the GIF URL is not available
            pass

    def back_button(self):
        """
        Navigates back to the last visited screen.
        """
        self.manager.current = self.last_screen
