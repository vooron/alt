import logging
from typing import Callable

from PySide2.QtGui import QColor
from PySide2.QtWidgets import QWidget, QGraphicsDropShadowEffect

from core.module.impl.gui.cards.card import WidgetCard
from core.module.impl.gui.connection import UIEvent
from core.module.impl.gui.qt.components.ui_main_widget import Ui_MainWidget


class MainCard(WidgetCard):

    def __init__(self, id: int, params: dict):
        super(MainCard, self).__init__(id, QWidget(), Ui_MainWidget(), params)

        ui: Ui_MainWidget = self.ui  # noqa

        # shadow effect
        shadow = QGraphicsDropShadowEffect(self.widget)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))
        ui.drop_shadow_frame.setGraphicsEffect(shadow)

        ui.close_app_button.clicked.connect(lambda: self.dispatch_event(UIEvent(
            name="closeCardClicked",
            payload={}
        )))

        ui.lineEdit.returnPressed.connect(self.on_text_command_entered)

    def on_text_command_entered(self):
        logging.info(f"MainCard on_text_command_entered")
        ui: Ui_MainWidget = self.ui  # noqa
        user_text_command = ui.lineEdit.text()
        user_text_command = user_text_command.strip()
        if not user_text_command:
            return

        self.dispatch_event(UIEvent(
            name="userQueryEntered",
            payload={
                "user_query": user_text_command
            }
        ))

    def appear(self):
        ui: Ui_MainWidget = self.ui  # noqa
        self._appear(ui.drop_shadow_frame)

    def disappear(self, on_finish: Callable[[], None]):
        ui: Ui_MainWidget = self.ui  # noqa
        self._disappear(ui.drop_shadow_frame, on_finish)

    def on_message(self, event: str, payload: dict):
        pass
