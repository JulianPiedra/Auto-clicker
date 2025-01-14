import tkinter as tk
from config.config_manager import load_config, save_config

def open_config_window(parent):
    config_data = load_config()
    hotkey_options = {"F1": "<f1>", "F2": "<f2>", "F3": "<f3>", "F4": "<f4>", "F5": "<f5>", 
                      "F6": "<f6>", "F7": "<f7>", "F8": "<f8>", "F9": "<f9>", "F10": "<f10>", 
                      "F11": "<f11>", "F12": "<f12>"}
    modifier_options = {"": "", "Ctrl": "<ctrl>+", "Alt": "<alt>+", "Shift": "<shift>+"}

    # Crear ventana de configuración
    config_window = tk.Toplevel(parent)
    config_window.title("Configuración")
    config_window.geometry("300x300")
    config_window.resizable(False, False)

    # Obtener claves actuales desde config_data
    start_key = next((k for k, v in hotkey_options.items() if v == config_data["start"]), "")
    stop_key = next((k for k, v in hotkey_options.items() if v == config_data["stop"]), "")
    mod_key = next((k for k, v in modifier_options.items() if v == config_data["mod"]), "")

    # Funciones para actualizar config_data
    def update_start(*args):
        config_data["start"] = hotkey_options[start_var.get()]
        update_stop_options()  # Actualizar opciones de stop

    def update_stop(*args):
        config_data["stop"] = hotkey_options[stop_var.get()]
        update_start_options()  # Actualizar opciones de start

    def update_mod(*args):
        config_data["mod"] = modifier_options[mod_var.get()]

    # Actualizar dinámicamente las opciones de start y stop
    def update_start_options():
        filtered_options = [key for key in hotkey_options.keys() if hotkey_options[key] != config_data["stop"]]
        start_menu["menu"].delete(0, "end")
        for option in filtered_options:
            start_menu["menu"].add_command(label=option, command=tk._setit(start_var, option))
        if start_var.get() not in filtered_options:
            start_var.set(filtered_options[0])

    def update_stop_options():
        filtered_options = [key for key in hotkey_options.keys() if hotkey_options[key] != config_data["start"]]
        stop_menu["menu"].delete(0, "end")
        for option in filtered_options:
            stop_menu["menu"].add_command(label=option, command=tk._setit(stop_var, option))
        if stop_var.get() not in filtered_options:
            stop_var.set(filtered_options[0])

    # Crear menús desplegables y vincularlos
    tk.Label(config_window, text="Hotkey Start").pack(pady=5)
    start_var = tk.StringVar(value=start_key)
    start_var.trace("w", update_start)
    start_menu = tk.OptionMenu(config_window, start_var, *hotkey_options.keys())
    start_menu.pack(pady=5)

    tk.Label(config_window, text="Hotkey Stop").pack(pady=5)
    stop_var = tk.StringVar(value=stop_key)
    stop_var.trace("w", update_stop)
    stop_menu = tk.OptionMenu(config_window, stop_var, *hotkey_options.keys())
    stop_menu.pack(pady=5)

    tk.Label(config_window, text="Modificador").pack(pady=5)
    mod_var = tk.StringVar(value=mod_key)
    mod_var.trace("w", update_mod)
    tk.OptionMenu(config_window, mod_var, *modifier_options.keys()).pack(pady=5)

    # Actualizar opciones al iniciar
    update_start_options()
    update_stop_options()

    # Botón para guardar y cerrar
    tk.Button(config_window, text="Guardar y cerrar", command=lambda: save_and_close(config_data, config_window)).pack(pady=10)

def save_and_close(config_data, window):
    save_config(config_data)
    window.destroy()
