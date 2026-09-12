# Event Bus
class EventBus:
    def __init__(self):
        self.handlers = {}

    def subscribe(self, event_type, handler):
        if event_type not in self.handlers:
            self.handlers[event_type] = []
        self.handlers[event_type].append(handler)

    def publish(self, event):
        event_type = event.get('type')
        if event_type in self.handlers:
            for handler in self.handlers[event_type]:
                try:
                    handler(event)
                except Exception as e:
                    print(f"Handler error: {e}")

# Services
def send_confirmation_email(event):
    user_id = event['user_id']
    order_id = event['order_id']
    print(f"Sending email to user {user_id} for order {order_id}")

def update_inventory(event):
    items = event['items']
    print(f"Updating inventory for {items}")

def send_notification(event):
    user_id = event['user_id']
    print(f"Sending push notification to user {user_id}")

# Setup
event_bus = EventBus()
event_bus.subscribe('order_placed', send_confirmation_email)
event_bus.subscribe('order_placed', update_inventory)
event_bus.subscribe('order_placed', send_notification)

# Trigger event
event_bus.publish({
    'type': 'order_placed',
    'order_id': 12345,
    'user_id': 789,
    'items': ['item1', 'item2']
})