import tkinter as tk
from logic.hotkey_listener import start_hotkey_listener
from gui.config_window import open_config_window
from logic.autoclicker import set_button_reference, toggle_state
button = None
def start_main_window():
    global button
    main_window = tk.Tk()
    main_window.title("Auto Clicker")
    main_window.geometry("300x200")

    # Crear botón y pasar como argumento
    button = tk.Button(main_window, text="Start", command=lambda: toggle_state())
    button.pack(side=tk.BOTTOM, anchor="e", padx=10, pady=10)
    set_button_reference(button)

    menuStrip = tk.Menu(main_window)
    menuStrip.add_command(label="Configuración", command=lambda: open_config_window(main_window))
    main_window.config(menu=menuStrip)

    # Iniciar el listener de hotkeys
    start_hotkey_listener()

    main_window.mainloop()