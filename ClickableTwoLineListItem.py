from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line

class ClickableTwoLineListItem(BoxLayout):
    def __init__(self, exercise, index, on_label_touch, **kwargs):
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
        if instance.collide_point(*touch.pos):
            self.clicked = not self.clicked  # Toggle the clicked state
            self.on_label_touch(self.exercise)  # Notify the callback
            self.draw_selection_line()
            return True

    def draw_selection_line(self):
        self.canvas.before.clear()  # Clear previous canvas instructions

        if self.clicked:
            with self.canvas.before:
                Color(0, 0, 1)  # Blue color
                Line(rectangle=(self.x, self.y, 3, self.height))
        else:
            self.canvas.before.clear()