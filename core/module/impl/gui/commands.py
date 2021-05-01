from core.module.impl.gui.cards.main_card import MainCard
from core.module.impl.gui.main_window import MainWindow

cards_mapping: dict = {
    "MainCard": MainCard,
}


def on_add_card(main_window: MainWindow, payload: dict):
    card_type = cards_mapping[payload['card_type']]
    params = payload["params"]
    main_window.add_card(card_type)


def on_hide_interface(main_window: MainWindow, payload: dict):
    # also all cards should be closed
    main_window.hide()


def on_show_interface(main_window: MainWindow, payload: dict):
    main_window.show()
