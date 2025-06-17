# 🎯 Guía de Uso - Sistema Multi-Pantalla de Detección de Imágenes

## 🆕 Nuevas Características v3.0

### ✅ **Detección Multi-Pantalla**
- Analiza **TODAS las pantallas simultáneamente** por defecto
- También permite seleccionar una pantalla específica
- **Hilos independientes** para cada monitor
- **Máxima eficiencia** y cobertura total

### ✅ **Detección Múltiple**
- Puedes cargar **múltiples imágenes** a la vez
- El sistema detecta cualquiera de las imágenes cargadas
- Identifica **cuál imagen** fue detectada en los logs

### ✅ **Movimiento Inteligente del Cursor**
- Después de hacer click, el cursor **se mueve automáticamente**
- Evita que el puntero interfiera con la detección
- Se mueve a una posición segura (50 píxeles de distancia)

### ✅ **Interfaz Avanzada**
- **Información detallada** de todos los monitores detectados
- **Modo de monitoreo** configurable (todas las pantallas vs específica)
- **Logs por monitor** para identificar dónde ocurrió cada detección
- **Área de logs** en tiempo real con timestamps

## 🚀 Cómo Usar

### 1. **Cargar Imágenes**
- Haz click en "Agregar Imágenes"
- Selecciona una o múltiples imágenes (.png, .jpg, .jpeg, .bmp, .tiff)
- Verás la lista de imágenes cargadas

### 2. **Configurar Modo de Monitoreo**
- **"Todas las pantallas"** (Recomendado): Busca en todos los monitores simultáneamente
- **"Pantalla específica"**: Busca solo en el monitor seleccionado
- Verás información de cuántos monitores fueron detectados

### 3. **Iniciar Detección**
- Click en "Iniciar Detección"
- El sistema creará hilos independientes para cada pantalla activa
- Cada hilo busca todas las imágenes cada 2 segundos
- Los logs mostrarán en qué monitor ocurrió cada detección

### 4. **Detener**
- Click en "Detener" para parar todos los hilos de detección
- El sistema esperará que todos los hilos terminen ordenadamente

## 📊 Logs de Actividad

Los logs muestran:
- 📱 **Información de monitores** detectados y regiones de monitoreo
- ✓ **Imágenes cargadas** exitosamente
- 🎯 **Detecciones y clicks** realizados con identificación de monitor
- �️ **Movimientos de cursor** para evitar interferencias
- ⏹️ **Inicio y parada** del sistema multi-hilo
- ❌ **Errores** si ocurren

### Ejemplo de logs:
```
[14:32:15] 📱 3 monitores detectados | Área total: 6,220,800 píxeles
[14:32:20] 🎯 Iniciando detección de 2 imágenes en todas las 3 pantallas
[14:32:21] 📱 [Monitor 1] Iniciando en región: (0, 0, 1920, 1080)
[14:32:21] 📱 [Monitor 2] Iniciando en región: (1920, 0, 1920, 1080)
[14:32:21] 📱 [Monitor 3] Iniciando en región: (3840, 0, 1920, 1080)
[14:32:25] 🎯 [Monitor 2] DETECTADA 'boton_play.png' (confianza: 0.95) → Click en (2850, 540)
[14:32:25] 🖱️ Cursor movido a (2900, 590) [Monitor 2]
```

## ⚙️ Configuración Avanzada

### Parámetros Modificables en el Código:

```python
THRESHOLD = 0.9        # Precisión requerida (90%)
INTERVAL = 2           # Segundos entre escaneos
CURSOR_OFFSET = 50     # Píxeles para mover cursor
```

### Medidas de Seguridad:
- **FAILSAFE**: Mover cursor a esquina superior izquierda detiene el programa
- **PAUSE**: Pausa de 0.1 segundos entre acciones de pyautogui

## 🔧 Consejos de Uso

1. **Imágenes de Calidad**: Usa imágenes nítidas y claras
2. **Tamaño Adecuado**: Ni muy grandes ni muy pequeñas
3. **Contraste**: Imágenes con buen contraste se detectan mejor
4. **Modo Multi-Pantalla**: Deja activado "Todas las pantallas" para máxima cobertura
5. **Monitoreo de Logs**: Observa los logs para entender el comportamiento del sistema
6. **Prueba Primero**: Usa imágenes de prueba antes de automatizar tareas importantes

## 🐛 Solución de Problemas

### Si no detecta imágenes:
- Verifica que la imagen sea exactamente igual a la pantalla
- Reduce el THRESHOLD a 0.8 o 0.7 en el código
- Asegúrate de que la imagen esté visible en alguna pantalla
- Revisa los logs para ver si hay errores de captura

### Si hace clicks erróneos:
- Aumenta el THRESHOLD a 0.95
- Verifica que no haya elementos similares en otras pantallas
- Usa imágenes más específicas y únicas

### Si el programa usa mucha CPU:
- Aumenta el INTERVAL a 3 o 4 segundos
- Usa menos imágenes simultáneamente
- Considera usar modo "Pantalla específica" en lugar de "Todas las pantallas"

### Si los hilos no se detienen:
- El sistema espera 3 segundos por cada hilo
- Si persiste, cierra el programa completamente
- Mueve el cursor a la esquina superior izquierda (FAILSAFE)
