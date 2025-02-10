import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox
import tkinter as tk  # Añadir esta importación
from PIL import Image, ImageTk
import os
import threading

class ImageOptimizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Optimizador de Imágenes")
        self.root.geometry("800x600")
        
        # Variables
        self.input_folder = ttk.StringVar()
        self.output_folder = ttk.StringVar()
        self.output_format = ttk.StringVar(value="WEBP")
        self.progress = ttk.DoubleVar()
        self.status_text = ttk.StringVar()
        self.selected_files = []  # Nueva variable para archivos seleccionados
        
        # Crear interfaz
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal con estilo
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Logo
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
            logo_img = Image.open(logo_path)
            logo_img = logo_img.resize((150, 150), Image.Resampling.LANCZOS)
            logo_photo = ImageTk.PhotoImage(logo_img)
            logo_label = ttk.Label(main_frame, image=logo_photo)
            logo_label.image = logo_photo
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"Error cargando el logo: {e}")
        
        # Título
        ttk.Label(
            main_frame,
            text="PCpro - Mermaid - Optimizador de Imágenes",
            font=("Helvetica", 16, "bold"),
            bootstyle="primary"
        ).pack(pady=10)
        
        # Frame para entradas
        input_frame = ttk.LabelFrame(main_frame, text="Configuración", padding="10")
        input_frame.pack(fill="x", padx=5, pady=5)
        
        # Carpeta de entrada
        input_container = ttk.Frame(input_frame)
        input_container.pack(fill="x", pady=5)
        ttk.Label(input_container, text="Carpeta de entrada:").pack(side="left")
        ttk.Entry(input_container, textvariable=self.input_folder, width=40).pack(side="left", padx=5)
        ttk.Button(
            input_container,
            text="Seleccionar Carpeta",
            command=self.select_input_folder,
            bootstyle="info"
        ).pack(side="left", padx=2)
        ttk.Button(
            input_container,
            text="Seleccionar Archivos",
            command=self.select_input_files,
            bootstyle="info"
        ).pack(side="left", padx=2)
        
        # Carpeta de salida
        output_container = ttk.Frame(input_frame)
        output_container.pack(fill="x", pady=5)
        ttk.Label(output_container, text="Carpeta de salida:").pack(side="left")
        ttk.Entry(output_container, textvariable=self.output_folder, width=50).pack(side="left", padx=5)
        ttk.Button(
            output_container,
            text="Examinar",
            command=self.select_output_folder,
            bootstyle="info"
        ).pack(side="left")
        
        # Formato de salida con más opciones
        format_container = ttk.Frame(input_frame)
        format_container.pack(fill="x", pady=5)
        ttk.Label(format_container, text="Formato de salida:").pack(side="left")
        formats = [
            "WEBP", "JPG", "JPEG", "PNG", "BMP", 
            "TIFF", "GIF", "ICO", "PPM", "JPEG2000"
        ]
        ttk.Combobox(
            format_container,
            textvariable=self.output_format,
            values=formats,
            width=20
        ).pack(side="left", padx=5)
        
        # Barra de progreso mejorada
        self.progress_bar = ttk.Progressbar(
            main_frame,
            variable=self.progress,
            maximum=100,
            bootstyle="success-striped"
        )
        self.progress_bar.pack(fill="x", padx=5, pady=10)
        
        # Estado
        ttk.Label(
            main_frame,
            textvariable=self.status_text,
            bootstyle="info"
        ).pack(pady=5)
        
        # Botón procesar
        ttk.Button(
            main_frame,
            text="Procesar Imágenes",
            command=self.start_processing,
            bootstyle="success",
            width=20
        ).pack(pady=10)
        
        # Resultados con scroll
        result_frame = ttk.LabelFrame(main_frame, text="Resultados", padding="10")
        result_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Scrollbar para resultados
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.result_text = ttk.Text(
            result_frame,
            height=10,
            width=70,
            yscrollcommand=scrollbar.set
        )
        self.result_text.pack(fill="both", expand=True)
        scrollbar.config(command=self.result_text.yview)

    def select_input_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.input_folder.set(folder)
            
    def select_output_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.output_folder.set(folder)

    def select_input_files(self):
        files = filedialog.askopenfilenames(
            filetypes=[
                ("Imágenes", "*.png *.jpg *.jpeg *.gif"),
                ("Todos los archivos", "*.*")
            ]
        )
        if files:
            self.selected_files = files
            self.input_folder.set("Archivos seleccionados: " + str(len(files)))
    
    def optimizar_imagen(self, input_path, output_path, max_width=800, quality=85, format=None):
        with Image.open(input_path) as img:
            ratio = max_width / float(img.size[0])
            height = int(float(img.size[1]) * ratio)
            
            if ratio < 1:
                img = img.resize((max_width, height), Image.Resampling.LANCZOS)
            
            if format:
                output_path = os.path.splitext(output_path)[0] + "." + format.lower()
                img.save(output_path, quality=quality, optimize=True, format=format)
            else:
                img.save(output_path, quality=quality, optimize=True)
    
    def get_file_size(self, filepath):
        return os.path.getsize(filepath) / (1024 * 1024)
    
    def process_images(self):
        try:
            output_folder = self.output_folder.get()
            output_format = self.output_format.get().lower()
            
            if not output_folder:
                messagebox.showerror("Error", "Seleccione una carpeta de salida")
                return

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            # Determinar qué imágenes procesar
            imagenes = []
            if self.selected_files:  # Si hay archivos seleccionados individualmente
                imagenes = [(os.path.dirname(f), os.path.basename(f)) for f in self.selected_files]
            else:  # Si se seleccionó una carpeta
                input_folder = self.input_folder.get()
                if not input_folder or not os.path.exists(input_folder):
                    messagebox.showerror("Error", "Seleccione una carpeta de entrada válida o archivos individuales")
                    return
                files = [f for f in os.listdir(input_folder) 
                        if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                imagenes = [(input_folder, f) for f in files]

            if not imagenes:
                self.status_text.set("No se encontraron imágenes para procesar")
                return

            total_original = 0
            total_optimizado = 0
            procesadas = 0

            for i, (folder, filename) in enumerate(imagenes):
                try:
                    input_path = os.path.join(folder, filename)
                    name, _ = os.path.splitext(filename)
                    output_path = os.path.join(output_folder, f"{name}.{output_format}")

                    original_size = self.get_file_size(input_path)
                    total_original += original_size

                    self.optimizar_imagen(input_path, output_path, format=output_format)

                    optimized_size = self.get_file_size(output_path)
                    total_optimizado += optimized_size
                    procesadas += 1

                    progress = (i + 1) / len(imagenes) * 100
                    self.progress.set(progress)

                    result = f"Procesado: {filename}\n"
                    result += f"Original: {original_size:.2f}MB\n"
                    result += f"Optimizado: {optimized_size:.2f}MB\n"
                    result += f"Reducción: {((original_size - optimized_size) / original_size) * 100:.1f}%\n\n"

                    self.result_text.insert(tk.END, result)
                    self.result_text.see(tk.END)

                except Exception as e:
                    self.result_text.insert(tk.END, f"Error procesando {filename}: {str(e)}\n")
                    continue

            if procesadas > 0:
                final_result = "\nRESUMEN FINAL\n"
                final_result += f"Imágenes procesadas: {procesadas}\n"
                final_result += f"Total original: {total_original:.2f}MB\n"
                final_result += f"Total optimizado: {total_optimizado:.2f}MB\n"
                final_result += f"Reducción total: {((total_original - total_optimizado) / total_original) * 100:.1f}%\n"

                self.result_text.insert(tk.END, final_result)
                self.status_text.set("Procesamiento completado")
            else:
                self.status_text.set("No se pudo procesar ninguna imagen")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error durante el procesamiento: {str(e)}")
            self.status_text.set("Error durante el procesamiento")
    
    def start_processing(self):
        if (not self.input_folder.get() and not self.selected_files) or not self.output_folder.get():
            messagebox.showerror("Error", "Seleccione archivos o carpeta de entrada y carpeta de salida")
            return

        self.result_text.delete(1.0, tk.END)
        self.progress.set(0)
        self.status_text.set("Procesando...")

        # Iniciar procesamiento en un hilo separado
        thread = threading.Thread(target=self.process_images)
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")  # Puedes cambiar el tema: "cosmo", "darkly", "litera", "minty", "lumen", etc.
    app = ImageOptimizerGUI(root)
    root.mainloop()
