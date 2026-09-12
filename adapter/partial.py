from collections.abc import Callable
from functools import partial
from typing import Any

from bs4 import BeautifulSoup

ConfigGetter = Callable[[str], Any]


class Experiment:
    def __init__(self, config_getter: ConfigGetter) -> None:
        self.config_getter = config_getter

    def load_data(self) -> None:
        data_path = self.config_getter("data_path")
        if not data_path:
            raise ValueError("No data path specified.")
        print(f"Loading data from {data_path}.")

    def setup_log(self) -> None:
        log_path = self.config_getter("log_path")
        if not log_path:
            raise ValueError("No log path specified.")
        print(f"Logging to {log_path}.")

    def train_model(self) -> None:
        epoch_count = self.config_getter("epoch_count")
        if not epoch_count:
            raise ValueError("No epoch count specified.")
        print(f"Training for {epoch_count} epochs.")

    def run(self) -> None:
        self.load_data()
        self.setup_log()
        self.train_model()

def get_from_bs(soup: BeautifulSoup, key: str, default: Any = None) -> Any | None:
    value = soup.find(key)
    if value:
        return value.get_text()
    return default
    
def main() -> None:

    with open("config.xml", encoding="utf8") as file:
        config_xml = file.read()
    soup = BeautifulSoup(config_xml, "xml")
    bs_adapter_fn = partial(get_from_bs, soup)

    experiment = Experiment(bs_adapter_fn)
    experiment.run()


if __name__ == "__main__":
    main()