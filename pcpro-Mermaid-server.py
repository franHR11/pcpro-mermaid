try:
    from PIL import Image
    print("Pillow instalado correctamente")
except ImportError:
    print("Error: Pillow no instalado")
    print("Ejecuta: pip install Pillow")
    exit(1)

import os

# Configuración de rutas (puedes modificar estas variables)
INPUT_FOLDER = "E:\\xampp\\htdocs\\pcpro\\static"  # Usar doble backslash y quitar el slash finals/pcpro/static")
OUTPUT_FOLDER = "E:\\xampp\\htdocs\\pcpro\\static\\imagenes_tratadas"  # Usar doble backslash y quitar el slash finalgenes_tratadas")
OUTPUT_FORMAT = "WEBP"  # Formato de salida por defecto: webp

def optimizar_imagen(input_path, output_path, max_width=800, quality=85, format=None):
    """
    Optimiza una imagen reduciendo su tamaño y calidad manteniendo buena apariencia
    """
    with Image.open(input_path) as img:
        # Calcular nuevo tamaño manteniendo proporción
        ratio = max_width / float(img.size[0])
        height = int(float(img.size[1]) * ratio)
        
        if ratio < 1:  # Solo redimensionar si la imagen es más grande que max_width
            img = img.resize((max_width, height), Image.Resampling.LANCZOS)
        
        # Si se especifica un formato, convertir la imagen
        if format:
            output_path = os.path.splitext(output_path)[0] + "." + format
            img.save(output_path, 
                     quality=quality, 
                     optimize=True,
                     format=format.upper())  # Convertir a mayúsculas para PIL
        else:
            # Guardar con optimización en el formato original
            img.save(output_path, 
                    quality=quality, 
                    optimize=True)

def get_file_size(filepath):
    """Retorna el tamaño del archivo en MB"""
    return os.path.getsize(filepath) / (1024 * 1024)

def esperar_tecla():
    """Espera cualquier tecla para continuar"""
    print("Presione cualquier tecla para continuar...")
    import msvcrt
    msvcrt.getch()
    return True

def main():
    global INPUT_FOLDER, OUTPUT_FOLDER, OUTPUT_FORMAT

    # Usar las rutas configurables
    input_folder = INPUT_FOLDER
    output_folder = OUTPUT_FOLDER
    output_format = OUTPUT_FORMAT.lower()

    print(f"Carpeta de imágenes de entrada: {input_folder}")
    print(f"Carpeta de imágenes de salida: {output_folder}")
    print(f"Formato de salida: {output_format}")

    # Validar formato de salida
    supported_formats = [ext[1:].lower() for ext in Image.registered_extensions().keys()]
    
    if output_format not in supported_formats:
        print(f"Error: El formato '{output_format}' no es soportado por Pillow.")
        print(f"Formatos soportados: {supported_formats}")
        return

    # Crear carpetas si no existen
    if not os.path.exists(input_folder):
        print(f"Creando carpeta de entrada: {input_folder}")
        try:
            os.makedirs(input_folder)
            print("Por favor, coloque las imágenes en la carpeta y ejecute el script nuevamente.")
            return
        except Exception as e:
            print(f"Error al crear la carpeta: {str(e)}")
            return

    if not os.path.exists(output_folder):
        print(f"Creando carpeta de salida: {output_folder}")
        try:
            os.makedirs(output_folder)
        except Exception as e:
            print(f"Error al crear la carpeta: {str(e)}")
            return

    # Obtener lista de imágenes
    imagenes = [f for f in os.listdir(input_folder) 
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    
    if not imagenes:
        print("No se encontraron imágenes para procesar")
        return

    print(f"Se encontraron {len(imagenes)} imágenes")
    print("Iniciando procesamiento...")
    print("-" * 50)
    
    total_original = 0
    total_optimizado = 0
    procesadas = 0
    
    for filename in imagenes:
        input_path = os.path.join(input_folder, filename)
        
        # Construir la ruta de salida con el nuevo formato
        name, ext = os.path.splitext(filename)
        output_filename = name + "." + output_format
        output_path = os.path.join(output_folder, output_filename)
        
        try:
            # Obtener tamaño original
            original_size = get_file_size(input_path)
            total_original += original_size
            
            # Optimizar imagen, pasando el formato de salida
            optimizar_imagen(input_path, output_path, format=output_format)
            
            # Obtener tamaño optimizado
            optimized_size = get_file_size(output_path)
            total_optimizado += optimized_size
            procesadas += 1
            
            # Mostrar resultados individuales
            reduccion = ((original_size - optimized_size) / original_size) * 100
            print(f"Archivo: {filename}")
            print(f"Original: {original_size:.2f}MB")
            print(f"Optimizado: {optimized_size:.2f}MB")
            print(f"Reducción: {reduccion:.1f}%")
            print("-" * 50)
            
        except Exception as e:
            print(f"Error procesando {filename}: {str(e)}")
            continue
    
    # Mostrar resumen final solo si se procesaron imágenes
    if procesadas > 0:
        print("\nRESUMEN FINAL")
        print(f"Imágenes procesadas: {procesadas}")
        print(f"Total original: {total_original:.2f}MB")
        print(f"Total optimizado: {total_optimizado:.2f}MB")
        reduccion_total = ((total_original - total_optimizado) / total_original) * 100
        print(f"Reducción total: {reduccion_total:.1f}%")
    else:
        print("\nNo se pudo procesar ninguna imagen")

if __name__ == "__main__":
    main()