from abc import abstractmethod, ABCMeta
from typing import Protocol, Callable

from PySide2.QtCore import QPropertyAnimation, QEasingCurve
from PySide2.QtWidgets import QWidget


class WidgetContainer(Protocol):
    @abstractmethod
    def setupUi(self, widget: QWidget):
        pass


class WidgetCard(metaclass=ABCMeta):
    id: int
    widget: QWidget
    ui: WidgetContainer

    send_message: Callable[['WidgetCard', str, dict], None]

    # Card event messages
    EVENT_MESSAGE_CLOSE_CARD = "CLOSE_CARD"
    # end card event messages

    def __init__(
            self,
            id: int,
            widget: QWidget,
            ui: WidgetContainer,
            send_message_callback: Callable[['WidgetCard', str, dict], None]
    ):
        self.id = id
        self.widget = widget
        self.ui = ui
        self.send_message = send_message_callback
        ui.setupUi(widget)

    def _appear(self, animated_frame):
        _g = animated_frame.geometry()
        _g_init = animated_frame.geometry()
        _g_init.setX(_g_init.x() + _g_init.width())
        self.appearence_animation = QPropertyAnimation(animated_frame, b"geometry")
        self.appearence_animation.setStartValue(_g_init)
        self.appearence_animation.setEndValue(_g)
        self.appearence_animation.setEasingCurve(QEasingCurve.InCurve)
        self.appearence_animation.setDuration(400)
        self.appearence_animation.start(QPropertyAnimation.DeleteWhenStopped)

    def _disappear(self, animated_frame, on_finish: Callable[[], None]):
        _g = animated_frame.geometry()
        _g_init = animated_frame.geometry()
        _g.setX(_g_init.x() + _g_init.width())
        self.disappear_animation = QPropertyAnimation(animated_frame, b"geometry")
        self.disappear_animation.setStartValue(_g_init)
        self.disappear_animation.setEndValue(_g)
        self.disappear_animation.setEasingCurve(QEasingCurve.InCurve)
        self.disappear_animation.setDuration(400)
        self.disappear_animation.start(QPropertyAnimation.DeleteWhenStopped)

        def on_animation_finished():
            self.widget.hide()
            on_finish()

        self.disappear_animation.finished.connect(on_animation_finished)

    @abstractmethod
    def appear(self):
        pass

    @abstractmethod
    def disappear(self, on_finish: Callable[[], None]):
        pass

    @abstractmethod
    def on_message(self, event: str, payload: dict):
        pass
