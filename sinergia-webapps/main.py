import sys
import os
import shutil
import requests
from urllib.parse import urlparse
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLineEdit,
                             QPushButton, QLabel, QMessageBox, QComboBox,
                             QTabWidget, QListWidget, QListWidgetItem)
from PyQt6.QtCore import Qt

APPS_DIR = os.path.expanduser("~/.local/share/applications")
ICONS_DIR = os.path.expanduser("~/.local/share/icons/sinergia-webapps")
os.makedirs(ICONS_DIR, exist_ok=True)

class SinergiaWebAppManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sinergia Web App Creator")

        # FIX: Bloqueo estricto de tamaño mínimo y máximo para impedir maximización
        self.setMinimumSize(450, 380)
        self.setMaximumSize(450, 380)

        # Diccionario para almacenar solo lo que está instalado
        self.navegadores_instalados = {}
        self.detectar_navegadores()

        self.tabs = QTabWidget()
        self.tab_crear = QWidget()
        self.tab_gestionar = QWidget()

        self.tabs.addTab(self.tab_crear, "Crear WebApp")
        self.tabs.addTab(self.tab_gestionar, "Mis WebApps")

        self.setup_tab_crear()
        self.setup_tab_gestionar()

        layout_principal = QVBoxLayout()
        layout_principal.addWidget(self.tabs)
        layout_principal.setContentsMargins(10, 10, 10, 10)
        self.setLayout(layout_principal)

        self.tabs.currentChanged.connect(self.cargar_webapps)

    def detectar_navegadores(self):
        """Busca en el sistema los binarios instalados y configura sus comandos de aislamiento"""
        motores = {
            "Google Chrome": {
                "binarios": ["google-chrome-stable", "google-chrome"],
                "cmd": '{ejecutable} --app="{url}" --class="sinergia-{id}"'
            },
            "Brave": {
                "binarios": ["brave-browser", "brave"],
                "cmd": '{ejecutable} --app="{url}" --class="sinergia-{id}"'
            },
            "Vivaldi": {
                "binarios": ["vivaldi-stable", "vivaldi", "vivaldi-snapshot"],
                "cmd": '{ejecutable} --app="{url}" --class="sinergia-{id}"'
            },
            "Chromium": {
                "binarios": ["chromium"],
                "cmd": '{ejecutable} --app="{url}" --class="sinergia-{id}"'
            },
            "Microsoft Edge": {
                "binarios": ["microsoft-edge-stable", "microsoft-edge", "microsoft-edge-dev"],
                "cmd": '{ejecutable} --app="{url}" --class="sinergia-{id}"'
            },
            "Zen Browser": {
                "binarios": ["zen-browser", "zen"],
                "cmd": '{ejecutable} --new-window "{url}" --class="sinergia-{id}"'
            },
            "LibreWolf": {
                "binarios": ["librewolf"],
                "cmd": '{ejecutable} --new-window "{url}" --class="sinergia-{id}"'
            },
            "Firefox": {
                "binarios": ["firefox"],
                "cmd": '{ejecutable} --new-window "{url}" --class="sinergia-{id}"'
            }
        }

        for nombre, datos in motores.items():
            for binario in datos["binarios"]:
                ruta = shutil.which(binario)
                if ruta:
                    self.navegadores_instalados[nombre] = datos["cmd"].replace("{ejecutable}", ruta)
                    break

    def setup_tab_crear(self):
        layout = QVBoxLayout()

        self.input_nombre = QLineEdit()
        self.input_nombre.setPlaceholderText("Ej. WhatsApp, YouTube...")

        self.input_url = QLineEdit()
        self.input_url.setPlaceholderText("https://...")

        self.combo_navegador = QComboBox()

        if not self.navegadores_instalados:
            self.combo_navegador.addItem("No se detectaron navegadores")
            self.combo_navegador.setEnabled(False)
        else:
            self.combo_navegador.addItems(self.navegadores_instalados.keys())

        btn_crear = QPushButton("Crear y Añadir al Menú")
        btn_crear.clicked.connect(self.crear_webapp)

        layout.addWidget(QLabel("Nombre de la aplicación:"))
        layout.addWidget(self.input_nombre)
        layout.addSpacing(10)
        layout.addWidget(QLabel("URL:"))
        layout.addWidget(self.input_url)
        layout.addSpacing(10)
        layout.addWidget(QLabel("Navegador base (Motor):"))
        layout.addWidget(self.combo_navegador)
        layout.addSpacing(20)
        layout.addWidget(btn_crear)
        layout.addStretch()

        self.tab_crear.setLayout(layout)

    def setup_tab_gestionar(self):
        layout = QVBoxLayout()
        self.lista_apps = QListWidget()
        btn_eliminar = QPushButton("Eliminar WebApp Seleccionada")
        btn_eliminar.clicked.connect(self.eliminar_webapp)

        layout.addWidget(QLabel("WebApps instaladas en tu sistema:"))
        layout.addWidget(self.lista_apps)
        layout.addWidget(btn_eliminar)

        self.tab_gestionar.setLayout(layout)
        self.cargar_webapps()

    def descargar_icono(self, url, nombre_archivo):
        try:
            dominio = urlparse(url).netloc
            if not dominio:
                dominio = urlparse("http://" + url).netloc

            api_url = f"https://www.google.com/s2/favicons?domain={dominio}&sz=128"
            respuesta = requests.get(api_url, timeout=5)

            if respuesta.status_code == 200:
                ruta_icono = os.path.join(ICONS_DIR, f"{nombre_archivo}.png")
                with open(ruta_icono, 'wb') as f:
                    f.write(respuesta.content)
                return ruta_icono
        except Exception as e:
            print(f"No se pudo descargar el ícono: {e}")
        return ""

    def crear_webapp(self):
        nombre = self.input_nombre.text().strip()
        url = self.input_url.text().strip()
        navegador = self.combo_navegador.currentText()

        if not self.navegadores_instalados:
            QMessageBox.critical(self, "Error", "No tienes navegadores compatibles instalados.")
            return

        if not nombre or not url:
            QMessageBox.warning(self, "Error", "El nombre y la URL son obligatorios.")
            return

        if not url.startswith("http"):
            url = "https://" + url

        nombre_archivo = nombre.lower().replace(" ", "-")
        ruta_desktop = os.path.join(APPS_DIR, f"sinergia-webapp-{nombre_archivo}.desktop")
        ruta_icono = self.descargar_icono(url, nombre_archivo)

        comando_exec = self.navegadores_instalados[navegador].format(url=url, id=nombre_archivo)

        contenido = f"""[Desktop Entry]
Version=1.0
Name={nombre}
Exec={comando_exec}
Icon={ruta_icono}
Terminal=false
Type=Application
Categories=Network;WebBrowser;
StartupWMClass=sinergia-{nombre_archivo}
X-Created-By=SinergiaWebApps
"""
        try:
            with open(ruta_desktop, "w") as f:
                f.write(contenido)
            os.chmod(ruta_desktop, 0o755)
            QMessageBox.information(self, "Éxito", f"'{nombre}' se ha integrado a tu menú.")
            self.input_nombre.clear()
            self.input_url.clear()
            self.cargar_webapps()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Fallo al crear la integración: {str(e)}")

    def cargar_webapps(self):
        self.lista_apps.clear()
        if not os.path.exists(APPS_DIR):
            return

        for archivo in os.listdir(APPS_DIR):
            if archivo.endswith(".desktop") and archivo.startswith("sinergia-webapp-"):
                ruta_completa = os.path.join(APPS_DIR, archivo)
                with open(ruta_completa, "r") as f:
                    contenido = f.read()

                if "X-Created-By=SinergiaWebApps" in contenido:
                    nombre_app = archivo
                    for linea in contenido.splitlines():
                        if linea.startswith("Name="):
                            nombre_app = linea.split("=")[1].strip()
                            break

                    item = QListWidgetItem(nombre_app)
                    item.setData(Qt.ItemDataRole.UserRole, ruta_completa)
                    self.lista_apps.addItem(item)

    def eliminar_webapp(self):
        item_seleccionado = self.lista_apps.currentItem()
        if not item_seleccionado:
            return

        ruta_desktop = item_seleccionado.data(Qt.ItemDataRole.UserRole)
        nombre = item_seleccionado.text()

        confirmacion = QMessageBox.question(
            self, "Desinstalar WebApp",
            f"¿Eliminar '{nombre}' del sistema operativo?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirmacion == QMessageBox.StandardButton.Yes:
            try:
                with open(ruta_desktop, "r") as f:
                    for linea in f:
                        if linea.startswith("Icon="):
                            ruta_icono = linea.split("=")[1].strip()
                            if os.path.exists(ruta_icono) and "sinergia-webapps" in ruta_icono:
                                os.remove(ruta_icono)
                            break
                os.remove(ruta_desktop)
                self.cargar_webapps()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al limpiar los archivos: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = SinergiaWebAppManager()
    ventana.show()
    sys.exit(app.exec())
