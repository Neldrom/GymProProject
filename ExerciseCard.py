from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField


class ExerciseCard(MDBoxLayout):
    """
    ExerciseCard class represents a custom widget for displaying an exercise card.

    Attributes:
        title: MDLabel for displaying the exercise name.
        icon: MDIconButton for the delete button.
        set_input: MDTextField for entering the number of sets.

    Methods:
        __init__(self, exercise_name, num_sets=1, **kwargs):
            Initializes the ExerciseCard.

        set_delete_button(self, func):
            Sets the function to be called when the delete button is pressed.

        get_set_input_text(self):
            Returns the text entered in the set_input MDTextField.
    """

    def __init__(self, exercise_name, num_sets=1, **kwargs):
        """
        Initializes the ExerciseCard.

        Parameters:
            exercise_name (str): Name of the exercise.
            num_sets (int): Number of sets (default is 1).
            **kwargs: Additional keyword arguments for MDBoxLayout.
        """
        super().__init__(**kwargs)
        self.orientation = "horizontal"
        self.spacing = 10
        self.height = dp(80)
        self.size_hint_y = None

        self.title = MDLabel(
            width=self.height,
            text=exercise_name,
            valign="center",
            pos_hint={'center_y': 0.5}
        )

        self.icon = MDIconButton(
            icon='trash-can',
            size_hint_x=None,
            valign="center",
            pos_hint={'center_y': 0.5}
        )

        self.set_input = MDTextField(
            text=str(num_sets),
            hint_text="Set",
            input_filter="int",
            pos_hint={'center_y': 0.5},
            max_text_length=3
        )

        self.add_widget(self.title)
        self.add_widget(self.set_input)
        self.add_widget(self.icon)

    def set_delete_button(self, func):
        """
        Sets the function to be called when the delete button is pressed.

        Parameters:
            func: Function to be called on button press.
        """
        self.icon.on_release = func

    def get_set_input_text(self):
        """
        Returns the text entered in the set_input MDTextField.

        Returns:
            str: Text entered in the set_input.
        """
        return self.set_input.text
