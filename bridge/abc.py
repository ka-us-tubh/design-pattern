"""
Bridge Pattern — Abstract Base Class approach

Devices (Webcam, DSLRCamera) and StreamingServices (YouTube, Twitch) vary
independently. StreamingService holds a list of Buffer callables (devices)
as the bridge between the two hierarchies.
"""

import logging
import random
import string
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field

# ---------------------------------------------------------------------------
# Shared data types
# ---------------------------------------------------------------------------

def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


BufferData = str
Buffer = Callable[[], BufferData]


# ---------------------------------------------------------------------------
# Devices  (Implementors)
# ---------------------------------------------------------------------------

def webcam() -> BufferData:
    return "###WEBCAMDATA###"


def dslr_camera() -> BufferData:
    return "###DSLRDATA###"


# ---------------------------------------------------------------------------
# Streaming service  (Abstraction)
# ---------------------------------------------------------------------------

@dataclass
class StreamingService(ABC):

    devices: list[Buffer] = field(default_factory=list)

    def add_device(self, device: Buffer) -> None:
        self.devices.append(device)

    def retrieve_buffer_data(self) -> list[BufferData]:
        return [device() for device in self.devices]

    @abstractmethod
    def start_stream(self) -> str: ...

    @abstractmethod
    def fill_buffer(self, stream_reference: str) -> None: ...

    @abstractmethod
    def stop_stream(self, stream_reference: str) -> None: ...


# ---------------------------------------------------------------------------
# Concrete streaming services  (Refined Abstractions)
# ---------------------------------------------------------------------------

class YouTubeStreamingService(StreamingService):
    def start_stream(self) -> str:
        ref = generate_id()
        logging.info(f"Starting YouTube stream with reference {ref}.")
        return ref

    def fill_buffer(self, stream_reference: str) -> None:
        buffer_data = self.retrieve_buffer_data()
        logging.info(
            f"Received buffer data: {buffer_data}. Sending to YouTube stream: {stream_reference}."
        )

    def stop_stream(self, stream_reference: str) -> None:
        logging.info(f"Closing YouTube stream with reference {stream_reference}.")


class TwitchStreamingService(StreamingService):
    def start_stream(self) -> str:
        ref = generate_id()
        logging.info(f"Starting Twitch stream with reference {ref}.")
        return ref

    def fill_buffer(self, stream_reference: str) -> None:
        buffer_data = self.retrieve_buffer_data()
        logging.info(
            f"Received buffer data: {buffer_data}. Sending to Twitch stream: {stream_reference}."
        )

    def stop_stream(self, stream_reference: str) -> None:
        logging.info(f"Closing Twitch stream with reference {stream_reference}.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    logging.basicConfig(level=logging.INFO)

    service = YouTubeStreamingService()
    service.add_device(webcam)
    ref = service.start_stream()
    service.fill_buffer(ref)
    service.stop_stream(ref)

    service2 = TwitchStreamingService()
    service2.add_device(dslr_camera)
    service2.add_device(webcam)
    ref2 = service2.start_stream()
    service2.fill_buffer(ref2)
    service2.stop_stream(ref2)


if __name__ == "__main__":
    main()
