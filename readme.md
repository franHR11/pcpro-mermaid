# PCpro Mermaid - Optimizador de Imágenes

## Descripción
PCpro Mermaid es una herramienta profesional de optimización de imágenes que ofrece dos modos de uso:
- Interfaz gráfica (GUI) con pcpro-Mermaid.py
- Modo servidor/línea de comandos con pcpro-Mermaid-server.py

## Características Principales
- Procesamiento individual o por lotes
- Múltiples formatos soportados
- Optimización inteligente de calidad/tamaño
- Interfaz gráfica intuitiva
- Modo servidor para automatización
- Preservación de proporciones
- Seguimiento en tiempo real
- Informes detallados

## Requisitos del Sistema
```bash
pip install Pillow ttkbootstrap
```

## Guía de Uso

### Modo GUI (pcpro-Mermaid.py)

1. **Iniciar la aplicación:**
   ```bash
   python pcpro-Mermaid.py
   ```

2. **Seleccionar imágenes:**
   - "Seleccionar Carpeta" - Procesa toda una carpeta
   - "Seleccionar Archivos" - Elige imágenes específicas

3. **Configurar salida:**
   - Elegir carpeta destino
   - Seleccionar formato de salida

4. **Procesar:**
   - Hacer clic en "Procesar Imágenes"
   - Monitorear progreso en la barra
   - Ver resultados en tiempo real

### Modo Servidor (pcpro-Mermaid-server.py)

1. **Configuración:**
   Editar variables de entorno:
   ```python
   INPUT_FOLDER = "ruta/entrada"
   OUTPUT_FOLDER = "ruta/salida"
   OUTPUT_FORMAT = "WEBP"
   ```

2. **Ejecución:**
   ```bash
   python pcpro-Mermaid-server.py
   ```

## Formatos Compatibles
- WEBP (recomendado)
- JPG/JPEG
- PNG
- BMP
- TIFF
- GIF
- ICO
- PPM
- JPEG2000

## Parámetros de Optimización
- Ancho máximo: 800px
- Calidad: 85%
- Optimización: Activada
- Proporciones: Preservadas

## Estructura del Proyecto
```
util/
└── tratamiento de imagenes/
    ├── pcpro-Mermaid.py       # Interfaz gráfica
    ├── pcpro-Mermaid-server.py # Modo servidor
    ├── logo.png               # Logo de la aplicación
    └── readme.md              # Documentación
```

## Resultados Proporcionados
- Tamaño original
- Tamaño optimizado
- Porcentaje de reducción
- Tiempo de procesamiento
- Resumen total

## Solución de Problemas

### Errores Comunes
1. **Pillow no instalado:**
   ```bash
   pip install Pillow
   ```

2. **Error de permisos:**
   - Ejecutar como administrador
   - Verificar permisos de carpetas

3. **Imágenes no encontradas:**
   - Comprobar extensiones soportadas
   - Verificar rutas

## Notas de Uso
- Hacer backup de imágenes originales
- Proceso irreversible
- WEBP recomendado para web
- GIFs animados se convierten a estáticos

## Contribuciones
1. Fork del repositorio
2. Crear rama feature
3. Commit cambios
4. Push a la rama
5. Crear Pull Request

## Licencia
MIT License - Ver archivo LICENSE
