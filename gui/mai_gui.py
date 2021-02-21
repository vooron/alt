# Compile with:
# venv/lib/python3.8/site-packages/PySide2/uic -g python gui/qt_ui/ui_main.ui > gui/qt_components/ui_main.py


import asyncio
import sys
import threading
from typing import Dict, Type, Callable

from PySide2.QtCore import Qt, QObject, Signal
from PySide2.QtWidgets import QApplication, QMainWindow, QDesktopWidget

from controller.client import Event, ConnectionClient
from gui.cards.card import WidgetCard
from gui.cards.list_card import ListCard
from gui.cards.main_card import MainCard
# GUI FILE
from qt_components.ui_main_window import Ui_MainWindow


class MainWindow(QMainWindow):
    last_used_card_index: int = 0
    cards: Dict[int, WidgetCard]

    client: ConnectionClient

    def __init__(self, client: ConnectionClient):
        QMainWindow.__init__(self)

        self.client = client
        self.controller_message_signal = ControllerMessageSignal()
        self.controller_message_signal.data.connect(self.on_controller_event_message)

        # TODO: make size adjust to protect from transparent non-clickable zone.
        self.cards = {}

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        screen_top_right_point = QDesktopWidget().rect().topRight()
        self.move(screen_top_right_point.x(), screen_top_right_point.y() + 30)

        self.add_card(MainCard)
        self.show()

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

    def _send_user_text_command(self, source_card: WidgetCard, payload: dict):
        asyncio.run(self.client.expose_event(Event("", "USER_TEXT_COMMAND_ENTERED", payload)))

    def on_ui_event(self, source_card: WidgetCard, event: str, payload: dict):
        routes: Dict[str, Callable[[WidgetCard, dict], None]] = {  # TODO: refactor
            "CLOSE_CARD": self._close_card_command,
            "USER_TEXT_COMMAND_ENTERED": self._send_user_text_command
        }

        route = routes.get(event)
        if not route:
            raise ValueError("Invalid event was provided.")

        route(source_card, payload)

    def on_controller_event_message(self, data: str):
        event = Event.from_message(data)
        if event.action == "SHOW_COMMAND_VARIANTS":  # TODO: add routing with commands
            self.add_card(ListCard)  # TODO: refactor work with initial params
            self.cards[self.last_used_card_index].on_message("SET_ITEMS", event.payload)
        else:
            print("Unknown action!")
            return


class ControllerMessageSignal(QObject):
    # https://stackoverflow.com/questions/36453462/pyqt5-qobject-cannot-create-children-for-a-parent-that-is-in-a-different-thread
    data = Signal(str)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    client = ConnectionClient("FrontEnd")
    main_window = MainWindow(client)


    def init_client():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(
            client.start(
                lambda event: main_window.controller_message_signal.data.emit(event.to_message())
            )
        )
        loop.run_forever()


    t1 = threading.Thread(target=init_client)
    t1.start()

    sys.exit(app.exec_())
