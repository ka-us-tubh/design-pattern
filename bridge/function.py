"""
Bridge Pattern — Function / Callable approach

Devices are plain functions (Buffer callables) rather than classes.
Services accept a single Buffer callable via constructor injection,
keeping the bridge as lightweight as possible.
"""

import logging
import random
import string
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

# ---------------------------------------------------------------------------
# Shared data types
# ---------------------------------------------------------------------------

def generate_id(length: int = 8) -> str:
    return "".join(random.choices(string.ascii_uppercase, k=length))


BufferData = str
Buffer = Callable[[], BufferData]


# ---------------------------------------------------------------------------
# Service protocol  (Abstraction interface)
# ---------------------------------------------------------------------------

class StreamingService(Protocol):
    def start_stream(self) -> str: ...
    def fill_buffer(self, stream_reference: str) -> None: ...
    def stop_stream(self, stream_reference: str) -> None: ...


# ---------------------------------------------------------------------------
# Devices  (Implementors — plain functions)
# ---------------------------------------------------------------------------

def webcam() -> BufferData:
    return "###WEBCAMDATA###"


def dslr_camera() -> BufferData:
    return "###DSLRDATA###"


# ---------------------------------------------------------------------------
# Concrete streaming services  (Refined Abstractions)
# ---------------------------------------------------------------------------

@dataclass
class YouTubeStreamingService:
    buffer: Buffer

    def start_stream(self) -> str:
        ref = generate_id()
        logging.info(f"Starting YouTube stream with reference {ref}.")
        return ref

    def fill_buffer(self, stream_reference: str) -> None:
        buffer_data = self.buffer()
        logging.info(
            f"Received buffer data: {buffer_data}. Sending to YouTube stream: {stream_reference}."
        )

    def stop_stream(self, stream_reference: str) -> None:
        logging.info(f"Closing YouTube stream with reference {stream_reference}.")


@dataclass
class TwitchStreamingService:
    buffer: Buffer

    def start_stream(self) -> str:
        ref = generate_id()
        logging.info(f"Starting Twitch stream with reference {ref}.")
        return ref

    def fill_buffer(self, stream_reference: str) -> None:
        buffer_data = self.buffer()
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

    service = YouTubeStreamingService(webcam)
    ref = service.start_stream()
    service.fill_buffer(ref)
    service.stop_stream(ref)

    service2 = TwitchStreamingService(dslr_camera)
    ref2 = service2.start_stream()
    service2.fill_buffer(ref2)
    service2.stop_stream(ref2)


if __name__ == "__main__":
    main()
