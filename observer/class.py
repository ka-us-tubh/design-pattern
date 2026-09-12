from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, event):
        pass

class EventEmitter:
    def __init__(self):
        self.observers = []
    
    def subscribe(self, observer):
        self.observers.append(observer)
    
    def unsubscribe(self, observer):
        self.observers.remove(observer)
    
    def emit(self, event):
        for observer in self.observers:
            observer.update(event)

class EmailNotifier(Observer):
    def update(self, event):
        print(f"Sending email: {event}")

class LogNotifier(Observer):
    def update(self, event):
        print(f"Logging: {event}")

# Usage
emitter = EventEmitter()
emitter.subscribe(EmailNotifier())
emitter.subscribe(LogNotifier())

emitter.emit("User registered")