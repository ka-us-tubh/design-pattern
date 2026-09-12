from typing import Any, Protocol

from bs4 import BeautifulSoup


class Config(Protocol):
    def get(self, key: str) -> Any | None: ...


class Experiment:
    def __init__(self, config: Config) -> None:
        self.config = config

    def load_data(self) -> None:
        data_path = self.config.get("data_path")
        if not data_path:
            raise ValueError("No data path specified.")
        print(f"Loading data from {data_path}.")

    def setup_log(self) -> None:
        log_path = self.config.get("log_path")
        if not log_path:
            raise ValueError("No log path specified.")
        print(f"Logging to {log_path}.")

    def train_model(self) -> None:
        epoch_count = self.config.get("epoch_count")
        if not epoch_count:
            raise ValueError("No epoch count specified.")
        print(f"Training for {epoch_count} epochs.")

    def run(self) -> None:
        self.load_data()
        self.setup_log()
        self.train_model()


class XMLAdapter:
    def __init__(self, soup: BeautifulSoup) -> None:
        self.soup = soup

    def get(self, key: str, default: Any = None) -> Any | None:
        value = self.soup.find(key)
        if value:
            return value.get_text()
        return default


def main() -> None:
    with open("config.xml", encoding="utf8") as file:
        config_xml = file.read()
    bs_xml = BeautifulSoup(config_xml, "xml")
    adapter = XMLAdapter(bs_xml)
    experiment = Experiment(adapter)
    experiment.run()


if __name__ == "__main__":
    main()
