from typing import Callable

from PySide2.QtCore import QSize
from PySide2.QtGui import QColor, QIcon
from PySide2.QtWidgets import QWidget, QGraphicsDropShadowEffect, QListWidgetItem

from core.module.impl.gui.cards.card import WidgetCard
from core.module.impl.gui.connection import UIEvent
from core.module.impl.gui.qt.components.ui_list_widget import Ui_ListWidget
from settings import UI_RESOURCES_FOLDER


class ListCard(WidgetCard):

    def __init__(self, id: int, params: dict):
        super(ListCard, self).__init__(id, QWidget(), Ui_ListWidget(), params)

        ui: Ui_ListWidget = self.ui  # noqa

        # shadow effect
        shadow = QGraphicsDropShadowEffect(self.widget)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))
        ui.drop_shadow_frame.setGraphicsEffect(shadow)

        for item_data in params['items']:
            icon = QIcon()
            icon.addFile(str(UI_RESOURCES_FOLDER / "icons" / "info-button.svg"), QSize(), QIcon.Normal, QIcon.Off)
            item = QListWidgetItem(icon, item_data['label'])
            ui.list.addItem(item)

        ui.close_app_button.clicked.connect(lambda: self.dispatch_event(UIEvent(
            name="closeCardClicked",
            payload={}
        )))

    def appear(self):
        ui: Ui_ListWidget = self.ui  # noqa
        self._appear(ui.drop_shadow_frame)

    def disappear(self, on_finish: Callable[[], None]):
        ui: Ui_ListWidget = self.ui  # noqa
        self._disappear(ui.drop_shadow_frame, on_finish)

    def on_message(self, event: str, payload: dict):
        pass