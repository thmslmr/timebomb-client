import npyscreen


class NotifForm(npyscreen.ActionFormMinimal):
    DEFAULT_COLUMNS = 60
    DEFAULT_LINES = 10

    def create(self):
        self.name = "Notification"
        self.keypress_timeout = 1
        self.center_on_display()

        self.text = self.add(
            npyscreen.MultiLineEdit, value="", editable=False, height=5
        )

    def on_ok(self):
        self.parentApp.state["notification"] = {}
        self.parentApp.setNextFormPrevious()

    def while_waiting(self):
        self.text.value = self.parentApp.state["notification"].get("message")
        self.text.update()
