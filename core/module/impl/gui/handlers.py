from core.module.impl.gui.cards.card import WidgetCard
from core.module.impl.gui.cards.list_card import ListCard
from core.module.impl.gui.cards.main_card import MainCard

cards_mapping: dict = {
    "MainCard": MainCard,
    "ListCard": ListCard
}


# === CommandMessage handlers ===============================
def on_add_card(main_window: 'MainWindow', payload: dict):
    card_type = cards_mapping[payload['card_type']]
    params = payload["params"]
    main_window.add_card(card_type, params)


def on_hide_interface(main_window: 'MainWindow', payload: dict):
    # also all cards should be closed
    main_window.hide()


def on_show_interface(main_window: 'MainWindow', payload: dict):
    main_window.show()


# === UIEvent handlers ===============================
def on_user_query_entered(main_window: 'MainWindow', source_card: WidgetCard, payload: dict):
    main_window.emit_to_controller("userQueryEntered", payload)


def on_close_card_clicked(main_window: 'MainWindow', source_card: WidgetCard, payload: dict):
    main_window.close_card(source_card)
