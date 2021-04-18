import spacy

from configs_main import apps_config_factory
from text_to_command.configuration_units import SessionConfiguration, SystemConfiguration
from text_to_command.indexer import Indexer
from text_to_command.intent_resolver import IntentResolver
import matplotlib.pyplot as plt

indexer = Indexer(spacy.load("en_core_web_md"))
intent_resolver = IntentResolver(indexer)

query = "Send Ann a message Buy some potato with Telegram"
# query = "Set sound to 50%"
# query = "Sound up"
# query = "Increase brightness on 10"  # problems!

commands = intent_resolver.resolve_intent_recommendations(
    query,
    apps_config_factory(),
    SystemConfiguration([]), SessionConfiguration("", [])
)


for c in sorted(commands, key=lambda x: x.score, reverse=True)[:1]:
    print("SCORE:", c.score)
    print("DISTRIBUTION", c.distribution)
    plt.bar(query.split(" "), c.distribution)
    plt.show()
