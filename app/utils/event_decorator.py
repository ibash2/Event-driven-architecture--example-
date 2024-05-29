from typing import Callable, Dict

event_handlers: Dict[str, Callable] = {}


def event_handler(event_name: str):
    def decorator(func: Callable):
        event_handlers[event_name] = func
        return func

    return decorator


def get_handler(event_name: str) -> Callable:
    return event_handlers.get(event_name)
