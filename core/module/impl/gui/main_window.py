# Compile with:
# venv/lib/python3.8/site-packages/PySide2/uic -g python gui/qt_ui/ui_main.ui > gui/qt_components/ui_main.py
import json
from typing import Dict, Type, Callable

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QMainWindow, QDesktopWidget

from core.module.impl.gui.cards.card import WidgetCard
# GUI FILE
from core.module.impl.gui.commands import on_add_card, on_hide_interface, on_show_interface
from core.module.impl.gui.connection import UiCommunicationSignal
from core.module.impl.gui.qt.components.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    last_used_card_index: int = 0
    cards: Dict[int, WidgetCard]

    commands: Dict[str, Callable[['MainWindow', dict], None]]

    def __init__(self, signals_object: UiCommunicationSignal):
        QMainWindow.__init__(self)

        self.cards = {}
        self._init_controller_communication(signals_object)
        self._init_ui()

        self.commands = {
            "add_card": on_add_card,
            "hide_interface": on_hide_interface,
            "show_interface": on_show_interface
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
        topic = data['topic']
        payload = data['payload']

        print(f"on_message_from_controller({topic}, {payload})", flush=True)
        self.commands[topic](self, payload)

    # === End controller communications ==============

    # === on UI event
    def on_ui_event(self, source_card: WidgetCard, topic: str, payload: dict):
        print(f"on_ui_event[{source_card.__class__.__name__}]({topic}, {payload})", flush=True)
        self.commands[topic](self, payload)

    # === End on UI event

    def add_card(self, card_type: Type, position: int = None):
        self.last_used_card_index += 1
        card = card_type(self.last_used_card_index, self.on_ui_event)
        self.cards[self.last_used_card_index] = card
        card.appear()
        if position is None:
            position = len(self.cards) - 1
        self.ui.verticalLayout.insertWidget(position, card.widget, alignment=Qt.AlignTop)

    def _close_card_command(self, source_card: WidgetCard, payload: dict):
        # TODO: add dependant cards and close all if main closed.
        def remove_card():
            self.ui.verticalLayout.removeWidget(source_card.widget)
            del self.cards[source_card.id]

        source_card.disappear(on_finish=remove_card)
