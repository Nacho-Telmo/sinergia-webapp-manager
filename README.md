# Sinergia WebApp Manager 🌐🐧

![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)
![Platform: Linux](https://img.shields.io/badge/Platform-Linux-lightgrey.svg)
![AUR: Available](https://img.shields.io/aur/version/sinergia-webapp-manager)

**Sinergia WebApp Manager** es una herramienta gráfica ligera y nativa para Linux, diseñada para crear y gestionar aplicaciones web (WebApps) independientes. 

Olvídate de abrir pestañas y perder tus sitios favoritos en el navegador. Con esta herramienta, puedes convertir cualquier sitio web (WhatsApp, YouTube, Netflix, herramientas de trabajo) en una aplicación de escritorio con su propia ventana, su propio ícono en el menú del sistema y su propio proceso, aislando la experiencia del resto de tu navegación diaria.

## ✨ Características Principales

*   **Independencia Total:** Las WebApps se ejecutan en ventanas limpias, sin barras de navegación, extensiones ni pestañas distractoras.
*   **Auto-Detección de Motores:** El gestor detecta automáticamente qué navegadores tienes instalados y te permite elegir cuál usar como "motor" para cada WebApp.
*   **Generación Automática de Íconos:** Descarga automáticamente el favicon de la URL que proporciones en alta calidad (128px) para usarlo en el menú de aplicaciones.
*   **Integración de Escritorio:** Crea archivos `.desktop` estándar de Linux, asegurando que tus WebApps aparezcan en tu lanzador de aplicaciones (KDE, GNOME, XFCE, etc.) y se comporten como software nativo.
*   **Ligero y Rápido:** Escrito íntegramente en Python 3 utilizando la robustez de PyQt6.

## 🚀 Navegadores Compatibles (Motores)

Sinergia WebApp Manager soporta y detecta de manera inteligente los siguientes navegadores instalados en tu sistema para renderizar las WebApps:

*   Google Chrome
*   Brave Browser
*   Vivaldi
*   Chromium
*   Microsoft Edge
*   Zen Browser
*   LibreWolf
*   Firefox

---

## 📦 Instalación

### Arch Linux / Manjaro / EndeavourOS (Recomendado)

Sinergia WebApp Manager está disponible oficialmente en el **Arch User Repository (AUR)**. Puedes instalarlo fácilmente usando tu helper favorito (como `yay` o `paru`):

> `yay -S sinergia-webapp-manager`

### Instalación Manual (Otras distribuciones)

Si no usas una distribución basada en Arch, puedes ejecutar el programa directamente clonando el repositorio. Asegúrate de tener Python 3 y PyQt6 instalados en tu sistema.

1. Clona este repositorio:
   > `git clone [https://github.com/Nacho-Telmo/sinergia-webapp-manager.git](https://github.com/Nacho-Telmo/sinergia-webapp-manager.git)`

2. Entra al directorio:
   > `cd sinergia-webapp-manager/sinergia-webapps`

3. Instala las dependencias y ejecuta el script principal:
   > `pip install -r ../requirements.txt`
   > 
   > `python main.py`

---

## 🛠️ ¿Cómo se usa?

1. Abre **Sinergia WebApp Manager** desde el menú de tu sistema.
2. En la pestaña **Crear WebApp**, ingresa un nombre (Ej. "WhatsApp Web").
3. Pega la URL directa al servicio (Ej. `[https://web.whatsapp.com](https://web.whatsapp.com)`).
4. Selecciona tu navegador favorito en la lista desplegable.
5. Haz clic en **Crear y Añadir al Menú**. 
6. ¡Listo! Busca la aplicación en el menú de tu escritorio; tendrá el ícono oficial del sitio web.

Para desinstalar una WebApp, simplemente ve a la pestaña **Mis WebApps**, selecciona la aplicación y haz clic en eliminar. El gestor se encargará de borrar los accesos directos y limpiar los íconos sobrantes.

---

## 🤝 Contribuciones y Problemas

Las contribuciones son bienvenidas. Si encuentras un error o tienes una idea para mejorar la aplicación, por favor abre un _Issue_ o envía un _Pull Request_.

Desarrollado por **Sinergia Comunidad Linuxera** para la comunidad Linux.
