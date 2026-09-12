# Factory / Abstract Factory Pattern

The **Abstract Factory** pattern provides an interface for creating *families* of related objects without specifying their concrete classes. A factory encapsulates the "which class to instantiate" decision and keeps the client code decoupled from concrete implementations.

## Core concept

Instead of calling `H264BPVideoExporter()` and `AACAudioExporter()` directly, the client asks a factory for a `VideoExporter` and an `AudioExporter`. Swapping the factory swaps the entire family of objects in one place.

## Files in this folder

| File | Factory mechanism | Notes |
|------|------------------|-------|
| `factory.py` | ABC + concrete factory classes | Classic GoF approach; `ExporterFactory` ABC with `FastExporter`, `HighQualityExporter`, `MasterQualityExporter` |
| `protocol.py` | `Protocol` (structural typing) | Same factories but no inheritance; relies on duck typing |
| `tuple.py` | Tuple of classes | Factory is a `(VideoClass, AudioClass)` tuple; no factory object needed |
| `dataclass.py` | `@dataclass` factory | `MediaExporterFactory` dataclass holds class references and is callable via `__call__` |

All four produce the same result — a paired `VideoExporter` + `AudioExporter` — but differ in how much structure they impose.

---

## Mermaid Diagrams

### Abstract class approach (`factory.py`)

```mermaid
classDiagram
    class ExporterFactory {
        <<abstract>>
        +get_video_exporter() VideoExporter
        +get_audio_exporter() AudioExporter
    }

    class FastExporter {
        +get_video_exporter() H264BPVideoExporter
        +get_audio_exporter() AACAudioExporter
    }

    class HighQualityExporter {
        +get_video_exporter() H264Hi422PVideoExporter
        +get_audio_exporter() AACAudioExporter
    }

    class MasterQualityExporter {
        +get_video_exporter() LosslessVideoExporter
        +get_audio_exporter() WAVAudioExporter
    }

    class VideoExporter {
        <<abstract>>
        +prepare_export(video_data)
        +do_export(folder)
    }

    class AudioExporter {
        <<abstract>>
        +prepare_export(audio_data)
        +do_export(folder)
    }

    class H264BPVideoExporter
    class H264Hi422PVideoExporter
    class LosslessVideoExporter
    class AACAudioExporter
    class WAVAudioExporter

    ExporterFactory <|-- FastExporter
    ExporterFactory <|-- HighQualityExporter
    ExporterFactory <|-- MasterQualityExporter

    VideoExporter <|-- H264BPVideoExporter
    VideoExporter <|-- H264Hi422PVideoExporter
    VideoExporter <|-- LosslessVideoExporter

    AudioExporter <|-- AACAudioExporter
    AudioExporter <|-- WAVAudioExporter

    FastExporter ..> H264BPVideoExporter : creates
    FastExporter ..> AACAudioExporter : creates
    HighQualityExporter ..> H264Hi422PVideoExporter : creates
    HighQualityExporter ..> AACAudioExporter : creates
    MasterQualityExporter ..> LosslessVideoExporter : creates
    MasterQualityExporter ..> WAVAudioExporter : creates
```

### Dataclass approach (`dataclass.py`)

```mermaid
classDiagram
    class MediaExporterFactory {
        +video_class: type
        +audio_class: type
        +__call__() MediaExporter
    }

    class MediaExporter {
        +video: VideoExporter
        +audio: AudioExporter
    }

    MediaExporterFactory ..> MediaExporter : creates
    MediaExporter --> VideoExporter : has
    MediaExporter --> AudioExporter : has
```

---

## Quality presets

| Quality | Video codec | Audio codec |
|---------|------------|------------|
| `low` | H.264 Baseline | AAC |
| `high` | H.264 Hi422P | AAC |
| `master` | Lossless | WAV |
