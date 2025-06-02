import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import cv2
import numpy as np
import threading
import time
from PIL import Image
from screeninfo import get_monitors

THRESHOLD = 0.9
INTERVAL = 2  # segundos entre escaneos

class ImageClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector de Imagen en Pantalla Seleccionada")

        self.image_path = None
        self.monitor = None
        self.running = False

        self.label = tk.Label(root, text="Selecciona una imagen para buscar")
        self.label.pack(pady=5)

        self.select_button = tk.Button(root, text="Seleccionar Imagen", command=self.select_image)
        self.select_button.pack(pady=5)

        self.monitor_label = tk.Label(root, text="Selecciona pantalla:")
        self.monitor_label.pack(pady=5)

        self.monitor_var = tk.StringVar()
        self.monitor_menu = tk.OptionMenu(root, self.monitor_var, "")
        self.monitor_menu.pack(pady=5)

        self.start_button = tk.Button(root, text="Iniciar", command=self.start_monitoring, state=tk.DISABLED)
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Detener", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(pady=5)

        self.load_monitors()

    def load_monitors(self):
        self.monitors = get_monitors()
        monitor_names = [f"{i}: {m.width}x{m.height} at ({m.x},{m.y})" for i, m in enumerate(self.monitors)]
        self.monitor_var.set(monitor_names[0] if monitor_names else "No hay monitores")
        self.monitor_menu['menu'].delete(0, 'end')
        for name in monitor_names:
            self.monitor_menu['menu'].add_command(label=name, command=tk._setit(self.monitor_var, name))

    def select_image(self):
        path = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            try:
                Image.open(path).verify()
                self.image_path = path
                self.label.config(text=f"Imagen: {path}")
                self.start_button.config(state=tk.NORMAL)
            except Exception as e:
                messagebox.showerror("Error", f"Imagen inválida: {e}")

    def start_monitoring(self):
        try:
            selected_index = int(self.monitor_var.get().split(":")[0])
            self.monitor = self.monitors[selected_index]
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo seleccionar la pantalla: {e}")
            return

        if not self.image_path:
            messagebox.showwarning("Advertencia", "Selecciona una imagen primero.")
            return

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.monitor_loop, daemon=True).start()

    def stop_monitoring(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def monitor_loop(self):
        print("[INFO] Iniciando monitorización en pantalla seleccionada...")

        template = cv2.imread(self.image_path, cv2.IMREAD_GRAYSCALE)
        if template is None:
            messagebox.showerror("Error", "No se pudo cargar la imagen.")
            return

        template_h, template_w = template.shape[:2]
        region = (self.monitor.x, self.monitor.y, self.monitor.width, self.monitor.height)

        while self.running:
            screenshot = pyautogui.screenshot(region=region)
            screenshot_np = np.array(screenshot)
            screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

            res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

            if max_val >= THRESHOLD:
                center_x = max_loc[0] + template_w // 2
                center_y = max_loc[1] + template_h // 2
                click_x = region[0] + center_x
                click_y = region[1] + center_y

                print(f"[✓] Imagen detectada (confianza: {max_val:.2f}) → clic en ({click_x}, {click_y})")
                pyautogui.click(click_x, click_y)
                time.sleep(1)  # tiempo de espera tras hacer clic
            else:
                print(f"[✗] No detectada (confianza: {max_val:.2f})")

            time.sleep(INTERVAL)

        print("[INFO] Monitorización detenida.")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageClickerApp(root)
    root.mainloop()
