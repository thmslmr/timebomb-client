import npyscreen


class NotifForm(npyscreen.ActionFormMinimal):
    """Display unread notification."""

    DEFAULT_COLUMNS = 60
    DEFAULT_LINES = 10

    def create(self):
        """Create widgets."""
        self.name = "Notification"
        self.keypress_timeout = 1
        self.center_on_display()

        self.text = self.add(
            npyscreen.MultiLineEdit, value="", editable=False, height=5
        )

    def on_ok(self):
        """Mark notificaiton as read and back to previous form."""
        self.parentApp.state.notification.read = True
        self.parentApp.setNextFormPrevious()

    def while_waiting(self):
        """Set text value to notification content."""
        self.text.value = self.parentApp.state.notification.content
        self.text.update()
