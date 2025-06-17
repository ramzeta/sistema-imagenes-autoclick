import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pyautogui
import cv2
import numpy as np
import threading
import time
import os
from PIL import Image
from screeninfo import get_monitors

THRESHOLD = 0.9
INTERVAL = 2  # segundos entre escaneos
CURSOR_OFFSET = 50  # píxeles para mover el cursor después del click

class ImageClickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Detector Múltiple de Imágenes en Pantalla")
        self.root.geometry("600x500")

        self.image_paths = []  # Lista de rutas de imágenes
        self.image_templates = []  # Plantillas OpenCV cargadas
        self.image_names = []  # Nombres de las imágenes
        self.monitor = None
        self.running = False

        self.setup_ui()

    def setup_ui(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Sección de imágenes
        images_frame = ttk.LabelFrame(main_frame, text="Imágenes para detectar", padding="10")
        images_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Botones para manejar imágenes
        btn_frame = ttk.Frame(images_frame)
        btn_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.add_button = ttk.Button(btn_frame, text="Agregar Imágenes", command=self.add_images)
        self.add_button.pack(side=tk.LEFT, padx=(0, 5))
        
        self.clear_button = ttk.Button(btn_frame, text="Limpiar Lista", command=self.clear_images)
        self.clear_button.pack(side=tk.LEFT, padx=5)
        
        # Lista de imágenes cargadas
        self.images_listbox = tk.Listbox(images_frame, height=6, width=70)
        self.images_listbox.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(images_frame, orient="vertical", command=self.images_listbox.yview)
        scrollbar.grid(row=1, column=2, sticky=(tk.N, tk.S))
        self.images_listbox.configure(yscrollcommand=scrollbar.set)
          # Sección de configuración
        config_frame = ttk.LabelFrame(main_frame, text="Configuración de Monitoreo", padding="10")
        config_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Información de monitores detectados
        self.monitors_info_label = ttk.Label(config_frame, text="Detectando monitores...")
        self.monitors_info_label.grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        # Opción de modo de monitoreo
        ttk.Label(config_frame, text="Modo de monitoreo:").grid(row=1, column=0, sticky=tk.W, pady=(5, 5))
        
        self.monitor_mode_var = tk.StringVar(value="all")
        mode_frame = ttk.Frame(config_frame)
        mode_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.radio_all = ttk.Radiobutton(mode_frame, text="Todas las pantallas", variable=self.monitor_mode_var, value="all")
        self.radio_all.pack(side=tk.LEFT, padx=(0, 20))
        
        self.radio_single = ttk.Radiobutton(mode_frame, text="Pantalla específica:", variable=self.monitor_mode_var, value="single")
        self.radio_single.pack(side=tk.LEFT, padx=(0, 10))
        
        self.monitor_combo = ttk.Combobox(mode_frame, state="readonly", width=30)
        self.monitor_combo.pack(side=tk.LEFT)
        
        # Controles de ejecución
        controls_frame = ttk.Frame(main_frame)
        controls_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.start_button = ttk.Button(controls_frame, text="Iniciar Detección", command=self.start_monitoring, state=tk.DISABLED)
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.stop_button = ttk.Button(controls_frame, text="Detener", command=self.stop_monitoring, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT)
        
        # Área de logs
        log_frame = ttk.LabelFrame(main_frame, text="Registro de Actividad", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(10, 0))
        
        self.log_text = tk.Text(log_frame, height=8, width=70)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        log_scrollbar = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        log_scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        # Configurar el grid para que se redimensione
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(3, weight=1)
        images_frame.columnconfigure(0, weight=1)
        config_frame.columnconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        self.load_monitors()

    def load_monitors(self):
        self.monitors = get_monitors()
        monitor_count = len(self.monitors)
        
        # Actualizar información de monitores
        if monitor_count == 1:
            info_text = f"📱 {monitor_count} monitor detectado"
        else:
            info_text = f"📱 {monitor_count} monitores detectados"
            
        total_area = sum(m.width * m.height for m in self.monitors)
        info_text += f" | Área total: {total_area:,} píxeles"
        self.monitors_info_label.config(text=info_text)
        
        # Llenar combobox para selección individual
        monitor_options = []
        for i, m in enumerate(self.monitors):
            option = f"Monitor {i+1}: {m.width}x{m.height} at ({m.x},{m.y})"
            if hasattr(m, 'name') and m.name:
                option += f" - {m.name}"
            monitor_options.append(option)
            
        self.monitor_combo['values'] = monitor_options
        if monitor_options:
            self.monitor_combo.current(0)

    def add_images(self):
        paths = filedialog.askopenfilenames(
            title="Seleccionar imágenes para detectar",
            filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.bmp *.tiff")]
        )
        
        for path in paths:
            if path not in self.image_paths:
                try:
                    # Verificar que la imagen se puede abrir
                    Image.open(path).verify()
                    
                    # Cargar template de OpenCV
                    template = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
                    if template is not None:
                        self.image_paths.append(path)
                        self.image_templates.append(template)
                        filename = os.path.basename(path)
                        self.image_names.append(filename)
                        
                        # Agregar a la lista visual
                        self.images_listbox.insert(tk.END, f"{len(self.image_paths)}. {filename}")
                        self.log(f"✓ Imagen cargada: {filename}")
                    else:
                        self.log(f"✗ Error al cargar: {os.path.basename(path)}")
                except Exception as e:
                    self.log(f"✗ Error con {os.path.basename(path)}: {str(e)}")
        
        # Habilitar botón de inicio si hay imágenes
        if self.image_paths:
            self.start_button.config(state=tk.NORMAL)

    def clear_images(self):
        self.image_paths.clear()
        self.image_templates.clear()
        self.image_names.clear()
        self.images_listbox.delete(0, tk.END)
        self.start_button.config(state=tk.DISABLED)
        self.log("🗑️ Lista de imágenes limpiada")

    def log(self, message):
        """Agregar mensaje al área de logs con timestamp"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def start_monitoring(self):
        if not self.image_paths:
            messagebox.showwarning("Advertencia", "Agrega al menos una imagen primero.")
            return

        # Configurar monitores según el modo seleccionado
        if self.monitor_mode_var.get() == "all":
            self.active_monitors = self.monitors
            mode_text = f"todas las {len(self.monitors)} pantallas"
        else:
            try:
                selected_index = self.monitor_combo.current()
                if selected_index == -1:
                    raise ValueError("No hay monitor seleccionado")
                self.active_monitors = [self.monitors[selected_index]]
                mode_text = f"monitor {selected_index + 1}"
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo seleccionar la pantalla: {e}")
                return

        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.log(f"🎯 Iniciando detección de {len(self.image_paths)} imágenes en {mode_text}")
        
        # Crear hilos para cada monitor
        self.monitor_threads = []
        for i, monitor in enumerate(self.active_monitors):
            thread = threading.Thread(target=self.monitor_loop, args=(monitor, i+1), daemon=True)
            thread.start()
            self.monitor_threads.append(thread)

    def stop_monitoring(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.log("⏹️ Detención solicitada - esperando que terminen todos los hilos...")
        
        # Esperar a que terminen todos los hilos (con timeout)
        if hasattr(self, 'monitor_threads'):
            for thread in self.monitor_threads:
                thread.join(timeout=3.0)
        
        self.log("✅ Detección completamente detenida")

    def move_cursor_away(self, click_x, click_y, monitor_info=""):
        """Mover el cursor lejos del punto de click para no interferir"""
        try:
            screen_width, screen_height = pyautogui.size()
            
            # Calcular posición segura (esquina opuesta)
            if click_x < screen_width // 2:
                safe_x = click_x + CURSOR_OFFSET
            else:
                safe_x = click_x - CURSOR_OFFSET
                
            if click_y < screen_height // 2:
                safe_y = click_y + CURSOR_OFFSET
            else:
                safe_y = click_y - CURSOR_OFFSET
                
            # Asegurar que esté dentro de los límites de pantalla
            safe_x = max(0, min(screen_width - 1, safe_x))
            safe_y = max(0, min(screen_height - 1, safe_y))
            
            pyautogui.moveTo(safe_x, safe_y)
            self.log(f"🖱️ Cursor movido a ({safe_x}, {safe_y}) {monitor_info}")
        except Exception as e:
            self.log(f"⚠️ Error moviendo cursor: {str(e)}")

    def monitor_loop(self, monitor, monitor_number):
        """Loop principal de detección para un monitor específico"""
        region = (monitor.x, monitor.y, monitor.width, monitor.height)
        monitor_info = f"[Monitor {monitor_number}]"
        self.log(f"📱 {monitor_info} Iniciando en región: {region}")

        while self.running:
            try:
                # Capturar pantalla del monitor específico
                screenshot = pyautogui.screenshot(region=region)
                screenshot_np = np.array(screenshot)
                screenshot_gray = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2GRAY)

                # Buscar cada imagen en la captura
                for i, (template, image_name) in enumerate(zip(self.image_templates, self.image_names)):
                    if not self.running:  # Verificar si se detuvo durante el bucle
                        break
                        
                    template_h, template_w = template.shape[:2]
                    
                    # Realizar template matching
                    res = cv2.matchTemplate(screenshot_gray, template, cv2.TM_CCOEFF_NORMED)
                    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

                    if max_val >= THRESHOLD:
                        # Calcular posición del click (coordenadas globales)
                        center_x = max_loc[0] + template_w // 2
                        center_y = max_loc[1] + template_h // 2
                        click_x = region[0] + center_x
                        click_y = region[1] + center_y

                        # Hacer click
                        pyautogui.click(click_x, click_y)
                        
                        # Mover cursor para no interferir
                        self.move_cursor_away(click_x, click_y, monitor_info)
                        
                        # Log del evento
                        self.log(f"🎯 {monitor_info} DETECTADA '{image_name}' (confianza: {max_val:.2f}) → Click en ({click_x}, {click_y})")
                        
                        # Pausa después del click
                        time.sleep(1)
                        break  # Salir del bucle de imágenes para evitar clicks múltiples

            except Exception as e:
                self.log(f"❌ {monitor_info} Error en detección: {str(e)}")

            time.sleep(INTERVAL)

        self.log(f"⏹️ {monitor_info} Monitorización detenida")

if __name__ == "__main__":
    # Configurar pyautogui para mayor seguridad
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    
    root = tk.Tk()
    app = ImageClickerApp(root)
    root.mainloop()
