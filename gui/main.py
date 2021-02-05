# Compile with:
# venv/lib/python3.8/site-packages/PySide2/uic -g python gui/qt_ui/ui_main.ui > gui/qt_components/ui_main.py


import sys

from PySide2.QtCore import Qt, QTimer, QPropertyAnimation, QRect, QEasingCurve, QVariantAnimation
from PySide2.QtGui import QColor
from PySide2.QtWidgets import QApplication, QMainWindow, QGraphicsDropShadowEffect, QDesktopWidget, \
    QGraphicsOpacityEffect

# GUI FILE
from controller.client import ConnectionClient, Event
from qt_components.ui_main import Ui_MainWindow


class VoiceAnimation:
    is_active: bool = False
    is_finished: bool = True
    window: QMainWindow

    MIN_VALUE: int = 20
    MAX_VALUE: int = 60

    def __init__(self, window: QMainWindow):
        self.window = window

    def _new_animation(self, widget):

        self.is_finished = False

        def set_height(val):
            widget.setFixedHeight(val)

        forward = QVariantAnimation(self.window)
        forward.setStartValue(20)
        forward.setEndValue(60)
        forward.setEasingCurve(QEasingCurve.InCurve)
        forward.setDuration(400)
        forward.valueChanged.connect(set_height)
        forward.start(QPropertyAnimation.DeleteWhenStopped)

        backward = QVariantAnimation(self.window)
        backward.setStartValue(60)
        backward.setEndValue(20)
        backward.setEasingCurve(QEasingCurve.InCurve)
        backward.setDuration(400)
        backward.valueChanged.connect(set_height)

        def controller():
            if self.is_active:
                self._new_animation(widget)
            else:
                self.is_finished = True

        forward.finished.connect(lambda: backward.start(QPropertyAnimation.DeleteWhenStopped))
        backward.finished.connect(controller)

    def start(self):
        # shit with not thread save operations and multiple recursion. Fix later.
        if self.is_active:
            return

        self.is_active = True

        if not self.is_active and not self.is_finished:
            return

        self._new_animation(self.window.ui.dot_animation_dot_1)
        self._new_animation(self.window.ui.dot_animation_dot_2)
        self._new_animation(self.window.ui.dot_animation_dot_3)
        self._new_animation(self.window.ui.dot_animation_dot_4)

    def stop(self):
        self.is_active = False


class MainWindow(QMainWindow):

    WINDOW_WIDTH = 500
    WINDOW_HIGH = 300

    def __init__(self):
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))
        self.ui.drop_shadow_frame.setGraphicsEffect(shadow)

        # control buttons connect
        self.ui.close_app_button.clicked.connect(lambda: self.close())

        screen_top_right_point = QDesktopWidget().rect().topRight()
        self.move(screen_top_right_point.x(), screen_top_right_point.y() + 30)

        self.show()

        self.anim = QPropertyAnimation(self.ui.drop_shadow_frame, b"geometry")
        self.anim.setStartValue(QRect(500, 0, 500, 300))
        self.anim.setEndValue(QRect(0, 0, 500, 300))
        self.anim.setEasingCurve(QEasingCurve.InCurve)
        self.anim.setDuration(400)
        self.anim.start(QPropertyAnimation.DeleteWhenStopped)

        self.voice_animation = VoiceAnimation(self)

        QTimer().singleShot(1000, lambda: self.voice_animation.start())
        QTimer().singleShot(3000, lambda: self.voice_animation.stop())
        QTimer().singleShot(4000, lambda: self.voice_animation.start())
        QTimer().singleShot(10000, lambda: self.voice_animation.stop())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec_())
