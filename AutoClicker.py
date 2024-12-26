import tkinter as tk
import threading
import json
import os
import time
from pynput import keyboard
from pynput.keyboard import Controller

# Variables globales
active = False
autoclick_thread = None 
button = None
keyboard_controller = Controller()  # Crear una instancia global del controlador

# Cargar configuración
config_file = "config.json"
if os.path.exists(config_file):
    with open(config_file, "r") as file:
        config_data = json.load(file)   
else:
    #create config file with default values
    config_data = { 
        "start": "<f1>",
        "stop": "<f2>",
        "mod": ""
    }
    with open(config_file, "w") as file:
        json.dump(config_data, file)

def toggle_state():
    global active, autoclick_thread
    active = not active
    if active:
        button.config(text="Stop")
        autoclick_thread = threading.Thread(target=autoclick, daemon=True)
        autoclick_thread.start()
    else:
        button.config(text="Start")


def autoclick():
    while active:
        # Simulación de pulsaciones usando el controlador
        keyboard_controller.press('w')
        keyboard_controller.release('w')
        
        keyboard_controller.press('d')
        keyboard_controller.release('d')

        keyboard_controller.press('e')
        keyboard_controller.release('e')

        # Salir si el estado se desactiva
        if not active:
            break

def on_hotkey(key):
    global active
    if key == config_data["start"]:
        if not active:
            toggle_state()
    elif key == config_data["stop"]:
        if active:
            toggle_state()

def listen_hotkeys():
    start, stop = None, None
    if config_data["mod"] != "":
        start, stop = config_data["mod"], config_data["mod"]
    start += config_data["start"]
    stop += config_data["stop"]
    
    with keyboard.GlobalHotKeys({
        start: lambda: on_hotkey(str(config_data["start"])),
        stop: lambda: on_hotkey(str(config_data["stop"]))
    }) as listener:
        listener.join()


import tkinter as tk

# Diccionarios de opciones
hotkey_options = {"F1": "<f1>", "F2": "<f2>", "F3": "<f3>", "F4": "<f4>", "F5": "<f5>", 
                  "F6": "<f6>", "F7": "<f7>", "F8": "<f8>", "F9": "<f9>", "F10": "<f10>", 
                  "F11": "<f11>", "F12": "<f12>"}
modifier_options = {"": "", "Ctrl": "<ctrl>+", "Alt": "<alt>+", "Shift": "<shift>+", "Tab": "<tab>+"}

# Configuración inicial
config_data = {"start": "<f5>", "stop": "<f8>", "mod": "<ctrl>+"}

def configure_window():
    global config_data
    # Crear ventana de configuración
    config_window = tk.Toplevel()
    config_window.title("Configuración")
    config_window.geometry("200x300")
    config_window.resizable(False, False)
    
    # Obtener claves actuales desde config_data
    start_key = next((k for k, v in hotkey_options.items() if v == config_data["start"]), "")
    stop_key = next((k for k, v in hotkey_options.items() if v == config_data["stop"]), "")
    mod_key = next((k for k, v in modifier_options.items() if v == config_data["mod"]), "")
    
    # Función para actualizar config_data con los valores seleccionados
    def update_start(*args):
        config_data["start"] = hotkey_options[start_var.get()]
    
    def update_stop(*args):
        config_data["stop"] = hotkey_options[stop_var.get()]
    
    def update_mod(*args):
        config_data["mod"] = modifier_options[mod_var.get()]
    
    # Crear etiquetas y menús desplegables
    tk.Label(config_window, text="Hotkey Start").pack(pady=5)
    start_var = tk.StringVar(value=start_key)
    start_var.trace("w", update_start)  # Vincular cambios a la actualización
    tk.OptionMenu(config_window, start_var, *hotkey_options.keys()).pack(pady=5)
    
    tk.Label(config_window, text="Hotkey Stop").pack(pady=5)
    stop_var = tk.StringVar(value=stop_key)
    stop_var.trace("w", update_stop)  # Vincular cambios a la actualización
    tk.OptionMenu(config_window, stop_var, *hotkey_options.keys()).pack(pady=5)
    
    tk.Label(config_window, text="Modificador").pack(pady=5)
    mod_var = tk.StringVar(value=mod_key)
    mod_var.trace("w", update_mod)  # Vincular cambios a la actualización
    tk.OptionMenu(config_window, mod_var, *modifier_options.keys()).pack(pady=5)
    
    # Botón para cerrar ventana
    tk.Button(config_window, text="Guardar y cerrar", command=config_window.destroy).pack(pady=10)

# Crear ventana principal
root = tk.Tk()
root.title("Ventana principal")
root.geometry("300x200")

# Botón para abrir la ventana de configuración
tk.Button(root, text="Abrir configuración", command=configure_window).pack(pady=20)

root.mainloop()

    
    
    

def main():
    global button
    # Crear main_window
    main_window = tk.Tk()
    main_window.title("Auto Clicker")
    main_window.geometry("300x200")
    
    button = tk.Button(main_window, text="Start", command=toggle_state)
    button.pack(side=tk.BOTTOM, anchor="e", padx=10, pady=10)
    
    menuStrip = tk.Menu(main_window)
    menuStrip.add_command(label="Configuración", command=lambda: configure_window())
    main_window.config(menu=menuStrip)
    
    # Crear hilo para escuchar hotkeys
    threading.Thread(target=listen_hotkeys, daemon=True).start()

    # Ejecutar main_window
    main_window.mainloop()

if __name__ == "__main__":
    main()