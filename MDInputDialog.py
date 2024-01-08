from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField


class Content(MDBoxLayout):
    pass


class MDInputDialog(MDDialog):
    def __init__(self, user, main_screen, **kwargs):
        content = Content()
        self.user = user
        self.main_ref = main_screen
        super().__init__(
            title="Edit Profile",
            type="custom",
            text="Edit your profile details",
            content_cls=content,
            buttons=[
                MDFlatButton(
                    text="Cancel", on_release=lambda *x: self.dismiss()
                ),
                MDFlatButton(
                    text="Save", on_release=lambda *x: self.save_profile(content)
                ),
            ],
            **kwargs
        )
        content.add_widget(MDTextField(hint_text="New Name", size_hint_y=None, height="36dp"))
        content.add_widget(MDTextField(hint_text="New Email", size_hint_y=None, height="36dp"))
        content.add_widget(MDTextField(hint_text="New Password", password=True, password_mask="*",
                                       size_hint_y=None, height="36dp"))

    def save_profile(self, content):
        new_name = content.children[2].text
        new_email = content.children[1].text
        new_password = content.children[0].text

        if new_name:
            self.user.update_name(new_name)
            self.main_ref.ids.profile_name.text = new_name
        if new_email:
            print(new_email)
            self.user.update_email(new_email)
        if new_password:
            print(new_password)
            self.user.update_password(new_password)

        self.dismiss()
