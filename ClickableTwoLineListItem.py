from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line

class ClickableTwoLineListItem(BoxLayout):
    """
    ClickableTwoLineListItem class represents a custom widget for displaying a two-line list item
    with the ability to toggle selection.

    Attributes:
        exercise (dict): Information about the exercise to display.
        index (int): Index of the item.
        on_label_touch (function): Callback function for label touch event.
        clicked (bool): Property to track whether the item is clicked.

    Methods:
        __init__(self, exercise, index, on_label_touch, **kwargs):
            Initializes the ClickableTwoLineListItem.

        on_label_touch_down(self, instance, touch):
            Handles the touch down event on the label. Toggles the clicked state and notifies the callback.

        draw_selection_line(self):
            Draws a selection line on the widget based on its clicked state.
    """

    def __init__(self, exercise, index, on_label_touch, **kwargs):
        """
        Initializes the ClickableTwoLineListItem.

        Parameters:
            exercise (dict): Information about the exercise to display.
            index (int): Index of the item.
            on_label_touch (function): Callback function for label touch event.
            **kwargs: Additional keyword arguments for BoxLayout.
        """
        super().__init__(orientation='horizontal', **kwargs)
        self.exercise = exercise
        self.index = index
        self.on_label_touch = on_label_touch  # Callback function for label touch
        self.clicked = False  # Property to track whether the item is clicked
        name = exercise['name'].title()

        # Label for the exercise name
        label = Label(text=f"{name}", valign='middle', halign='left', size_hint_x=0.7)
        label.bind(on_touch_down=self.on_label_touch_down)  # Bind touch event to the method

        # Add label to the BoxLayout
        self.add_widget(label)

    def on_label_touch_down(self, instance, touch):
        """
        Handles the touch down event on the label.
        Toggles the clicked state and notifies the callback.

        Parameters:
            instance: The Label instance.
            touch: The touch event.
        """
        if instance.collide_point(*touch.pos):
            self.clicked = not self.clicked  # Toggle the clicked state
            self.on_label_touch(self.exercise)  # Notify the callback
            self.draw_selection_line()
            return True

    def draw_selection_line(self):
        """
        Draws a selection line on the widget based on its clicked state.
        """
        self.canvas.before.clear()  # Clear previous canvas instructions

        if self.clicked:
            with self.canvas.before:
                Color(0, 0, 1)  # Blue color
                Line(rectangle=(self.x, self.y, 3, self.height))
        else:
            self.canvas.before.clear()
