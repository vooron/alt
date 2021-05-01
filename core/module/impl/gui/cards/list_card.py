from typing import Callable, Dict

from PySide2.QtCore import QSize
from PySide2.QtGui import QColor, QIcon
from PySide2.QtWidgets import QWidget, QGraphicsDropShadowEffect, QListWidgetItem

from core.module.impl.gui.cards.card import WidgetCard
from core.module.impl.gui.qt.components.ui_list_widget import Ui_ListWidget


class ListCard(WidgetCard):

    def __init__(self, id: int, send_message_callback: Callable[['WidgetCard', str, dict], None]):
        super(ListCard, self).__init__(id, QWidget(), Ui_ListWidget(), send_message_callback)

        ui: Ui_ListWidget = self.ui  # noqa

        # shadow effect
        shadow = QGraphicsDropShadowEffect(self.widget)
        shadow.setBlurRadius(20)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 60))
        ui.drop_shadow_frame.setGraphicsEffect(shadow)

        ui.close_app_button.clicked.connect(lambda: self.send_message(self, self.EVENT_MESSAGE_CLOSE_CARD, {}))

    def appear(self):
        ui: Ui_ListWidget = self.ui  # noqa
        self._appear(ui.drop_shadow_frame)

    def disappear(self, on_finish: Callable[[], None]):
        ui: Ui_ListWidget = self.ui  # noqa
        self._disappear(ui.drop_shadow_frame, on_finish)

    def _set_items(self, payload: dict):  # TODO: add deserializer for better documentation
        ui: Ui_ListWidget = self.ui  # noqa
        ui.list.clear()
        for item_data in payload['items']:
            icon = QIcon()
            icon.addFile(u"resources/icons/info-button.svg", QSize(), QIcon.Normal, QIcon.Off)
            item = QListWidgetItem(icon, item_data['label'])
            ui.list.addItem(item)

    def on_message(self, event: str, payload: dict):
        routes: Dict[str, Callable[[dict], None]] = {
            "SET_ITEMS": self._set_items
        }

        route = routes.get(event)
        if not route:
            raise ValueError("Invalid event was provided.")

        route(payload)