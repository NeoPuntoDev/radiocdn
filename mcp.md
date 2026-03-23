# Instrucciones para el Asistente de Inteligencia Artificial (MCP)

Hola, IA. El propietario de este repositorio (NeoPunto) lo gestiona principalmente desde un dispositivo móvil Android usando la interfaz web. Por lo tanto, no puede ejecutar scripts o comandos de terminal localmente. Tu trabajo como asistente técnico es realizar estas tareas por él cada vez que lo solicite.

Este repositorio es una base de datos/directorio para una aplicación de radio cristiana. Los datos se sirven desde `stream.json` y las imágenes desde la carpeta `img/` utilizando el CDN jsdelivr.

## Cómo agregar o eliminar emisoras de radio

**IMPORTANTE:** Nunca edites `stream.json` ni proceses las imágenes a mano. **Siempre debes usar el script `manage_radio.py`** que ya está preparado en la raíz del repositorio. Este script se encarga de todo el flujo (optimización de imagen a WebP, formateo de nombres a slug, borrado del archivo original, subida con URL jsdelivr, y reordenamiento de IDs de las radios 1, 2, 3...).

### Requisitos previos

Antes de ejecutar el script, asegúrate de que las dependencias están instaladas:
```bash
pip install -r requirements.txt
```

### 1. Añadir una nueva emisora

Cuando el usuario suba una imagen a la raíz del repositorio y te diga: *"toma la imagen, ponle este nombre, enlace y descríbela (opcional) y ponla en la emisora"*.
**IMPORTANTE:** Siempre corrige la ortografía si el usuario comete errores al escribir el título (nombre) de la radio o su descripción.

**Tu tarea:**
1. Identifica el nombre de la imagen recién subida en la raíz (ej. `mifoto.jpg`).
2. Identifica el nombre de la radio, la URL del streaming y el idioma que te proporcionó el usuario en su mensaje. Corrige la ortografía del nombre y la descripción si es necesario.
   * Si el usuario dice "español", el idioma es `es`.
   * Si el usuario dice "inglés", el idioma es `en`.
   * Pasa el idioma usando el argumento `--lang`.
3. Ejecuta el script `manage_radio.py` pasando estos datos como argumentos.

**Comando de ejemplo (con idioma):**
```bash
python3 manage_radio.py add --name "Nombre de la Radio" --url "http://url-del-stream.com" --image "mifoto.jpg" --lang "es"
```

**Con descripción (opcional):**
```bash
python3 manage_radio.py add --name "Nombre de la Radio" --url "http://url-del-stream.com" --image "mifoto.jpg" --desc "Emisora con la mejor música cristiana." --lang "en"
```
*Nota: Si el usuario no proporciona una descripción, el script automáticamente colocará "Alabanza y adoración". El script también se encargará de convertir la imagen a WebP, guardarla en `img/` con formato slug, generar la URL de CDN correcta y reordenar los IDs.*

### 2. Borrar una emisora

Cuando el usuario te diga *"borra esta emisora"* y te dé un ID o un nombre.

**Tu tarea:**
Ejecuta el script `manage_radio.py` con el argumento `delete` seguido del ID de la emisora o el nombre.

**Comandos de ejemplo:**

Por ID:
```bash
python3 manage_radio.py delete --id 5
```

Por Nombre:
```bash
python3 manage_radio.py delete --name "Nombre de la Radio"
```

*Nota: El script se encargará de buscar en `stream.json`, eliminar la entrada, borrar la imagen `.webp` asociada en la carpeta `img/` y reordenar los IDs restantes (1, 2, 3...) para que queden de forma secuencial.*

### Pasos finales obligatorios
1. **Verificar:** Una vez que ejecutes el comando exitosamente con `run_in_bash_session`, usa `cat stream.json` o revisa el archivo JSON para asegurarte de que se ha modificado correctamente y usa `ls -la img/` para asegurar que las imágenes se han procesado.
2. **Commit y Push:** Confirma los cambios como lo harías normalmente.
