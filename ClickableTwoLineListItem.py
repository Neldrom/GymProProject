from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Line

class ClickableTwoLineListItem(BoxLayout):
    def __init__(self, exercise, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.exercise = exercise
        self.clicked = False  # Property to track whether the item is clicked
        name = exercise['name'].title()
        if len(name) > 35:
            name = name[:35]
        # Label for the exercise name
        label = Label(text=f"{name}", valign='middle', halign='left', size_hint_x=0.7)

        # Add label to the BoxLayout
        self.add_widget(label)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.clicked = not self.clicked  # Toggle the clicked state
            self.draw_selection_line()
            return True
        return super().on_touch_down(touch)

    def draw_selection_line(self):
        self.canvas.before.clear()  # Clear previous canvas instructions

        if self.clicked:
            with self.canvas.before:
                Color(0, 0, 1)  # Blue color
                Line(rectangle=(self.x, self.y, 3, self.height))
        else:
            self.canvas.before.clear()  # Clear the line if not clicked
