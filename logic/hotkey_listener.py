from pynput import keyboard
from config.config_manager import load_config
from logic.autoclicker import toggle_state


def start_hotkey_listener():
    hotkey_listener = None
    config_data = load_config()

    if hotkey_listener and hotkey_listener.running:
        hotkey_listener.stop()

    hotkey_listener = keyboard.GlobalHotKeys({
        config_data["start"]: lambda: toggle_state(),
        config_data["stop"]: lambda: toggle_state(),
    })
    hotkey_listener.start()
