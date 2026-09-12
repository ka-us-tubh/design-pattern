"""
Bridge Pattern — Protocol approach

Both the device (Implementor) and service (Abstraction) sides are defined
with Protocol, relying on structural typing instead of inheritance.
Each service receives a single StreamingDevice via constructor injection.
"""

import logging
import random
import string
from dataclasses import dataclass
from typing import Protocol

# ---------------------------------------------------------------------------
# Shared data types
# ---------------------------------------------------------------------------

def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


BufferData = str


# ---------------------------------------------------------------------------
# Device protocol  (Implementor interface)
# ---------------------------------------------------------------------------

class StreamingDevice(Protocol):
    def get_buffer_data(self) -> BufferData: ...


# ---------------------------------------------------------------------------
# Service protocol  (Abstraction interface)
# ---------------------------------------------------------------------------

class StreamingService(Protocol):
    def start_stream(self) -> str: ...
    def fill_buffer(self, stream_reference: str) -> None: ...
    def stop_stream(self, stream_reference: str) -> None: ...


# ---------------------------------------------------------------------------
# Concrete devices  (Concrete Implementors)
# ---------------------------------------------------------------------------

class Webcam:
    def get_buffer_data(self) -> BufferData:
        return "###WEBCAMDATA###"


class DSLRCamera:
    def get_buffer_data(self) -> BufferData:
        return "###DSLRDATA###"


# ---------------------------------------------------------------------------
# Concrete streaming services  (Refined Abstractions)
# ---------------------------------------------------------------------------

@dataclass
class YouTubeStreamingService:
    device: StreamingDevice

    def start_stream(self) -> str:
        ref = generate_id()
        logging.info(f"Starting YouTube stream with reference {ref}.")
        return ref

    def fill_buffer(self, stream_reference: str) -> None:
        buffer_data = self.device.get_buffer_data()
        logging.info(
            f"Received buffer data: {buffer_data}. Sending to YouTube stream: {stream_reference}."
        )

    def stop_stream(self, stream_reference: str) -> None:
        logging.info(f"Closing YouTube stream with reference {stream_reference}.")


@dataclass
class TwitchStreamingService:
    device: StreamingDevice

    def start_stream(self) -> str:
        ref = generate_id()
        logging.info(f"Starting Twitch stream with reference {ref}.")
        return ref

    def fill_buffer(self, stream_reference: str) -> None:
        buffer_data = self.device.get_buffer_data()
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

    service = YouTubeStreamingService(Webcam())
    ref = service.start_stream()
    service.fill_buffer(ref)
    service.stop_stream(ref)

    service2 = TwitchStreamingService(DSLRCamera())
    ref2 = service2.start_stream()
    service2.fill_buffer(ref2)
    service2.stop_stream(ref2)


if __name__ == "__main__":
    main()
