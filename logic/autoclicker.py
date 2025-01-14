import threading
import time
from pynput.keyboard import Controller

active = False
keyboard_controller = Controller()
button = None  

def set_button_reference(btn):
    global button
    button = btn

def toggle_state():
    global active, autoclick_thread, button
    active = not active
    if button:  # Verificar que el botón esté inicializado
        button.config(text="Stop" if active else "Start")
    if active:
        autoclick_thread = threading.Thread(target=autoclick, daemon=True)
        autoclick_thread.start()
    else:
        autoclick_thread = None


def autoclick():
    while active:
        keyboard_controller.press('w')
        keyboard_controller.release('w')
        keyboard_controller.press('d')
        keyboard_controller.release('d')
        keyboard_controller.press('e')
        keyboard_controller.release('e')
        time.sleep(0.1)  
