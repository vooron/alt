# Compile with:
# venv/lib/python3.8/site-packages/PySide2/uic -g python gui/qt_ui/ui_main.ui > gui/qt_components/ui_main.py
import json
from typing import Dict, Type, Callable

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QDesktopWidget

from core.module.impl.gui.cards.card import WidgetCard
from core.module.impl.gui.connection import UiCommunicationSignal, CommandMessage, UIEvent
# GUI FILE
from core.module.impl.gui.handlers import on_add_card, on_hide_interface, on_user_query_entered, \
    on_close_card_clicked
from core.module.impl.gui.qt.components.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    last_used_card_index: int = 0
    cards: Dict[int, WidgetCard]

    command_handlers: Dict[str, Callable[['MainWindow', dict], None]]
    event_handlers: Dict[str, Callable[['MainWindow', WidgetCard, dict], None]]

    controller_signals_object: UiCommunicationSignal

    def __init__(self, signals_object: UiCommunicationSignal):
        QMainWindow.__init__(self)

        self.cards = {}
        self._init_controller_communication(signals_object)
        self._init_ui()

        self.command_handlers = {
            "add_card": on_add_card,
            "hide_interface": on_hide_interface
        }

        self.event_handlers = {
            "userQueryEntered": on_user_query_entered,
            "closeCardClicked": on_close_card_clicked
        }

    def _init_controller_communication(self, signals_object: UiCommunicationSignal):
        self.controller_signals_object = signals_object
        self.controller_signals_object.ui_input.connect(self.on_message_from_controller)

    def _init_ui(self):
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        screen_top_right_point = QDesktopWidget().rect().topRight()
        self.move(screen_top_right_point.x(), screen_top_right_point.y() + 30)

    # === Controller communications ==============
    def emit_to_controller(self, topic: str, payload: dict):
        print(f"emit_to_controller({topic}, {payload})", flush=True)
        self.controller_signals_object.ui_output.emit(json.dumps(dict(
            topic=topic,
            payload=payload
        )))

    def on_message_from_controller(self, message: str):
        data = json.loads(message)
        command = CommandMessage(*data)

        print(f"on_message_from_controller({command.topic}, {command.payload})", flush=True)
        self.command_handlers[command.topic](self, command.payload)

    # === End controller communications ==============

    # === on UI event
    def on_ui_event(self, source_card: WidgetCard, event: UIEvent):
        print(f"on_ui_event[{source_card.__class__.__name__}]({event.name}, {event.payload})", flush=True)
        self.event_handlers[event.name](self, source_card, event.payload)

    # === End on UI event

    def add_card(self, card_type: Type, params: dict, position: int = None):
        self.last_used_card_index += 1
        card = card_type(self.last_used_card_index, params)
        card.set_on_event(lambda event: self.on_ui_event(card, event))
        self.cards[self.last_used_card_index] = card
        card.appear()
        if position is None:
            position = len(self.cards) - 1
        self.ui.verticalLayout.insertWidget(position, card.widget, alignment=Qt.AlignTop)
        self.resize(self.ui.verticalLayout.sizeHint())

        self.show()

    def close_card(self, source_card: WidgetCard):
        # TODO: add dependant cards and close all if main closed.
        def remove_card():
            self.ui.verticalLayout.removeWidget(source_card.widget)
            del self.cards[source_card.id]
            self.resize(self.ui.verticalLayout.sizeHint())
            if not self.cards:
                self.hide()

        source_card.disappear(on_finish=remove_card)
