import sys
import threading
from tkinter import filedialog
from Ecualizador import Ecualizador
from PyQt6.QtWidgets import QMainWindow, QApplication
import sounddevice as sd
import soundfile as sf

from VentanaEcualizador import Ui_MainWindow

class Controlador:

    ui = Ui_MainWindow()

    def __init__(self):
        self.iniciarVentana()
        self.activarListeners()

    def iniciarVentana(self):
        self.ventana = QMainWindow()
        self.ui.setupUi(self.ventana)
        self.ventana.show()

    def activarListeners(self):
        self.ui.btnAbrirCancion.clicked.connect(self.abrirCancion)
        self.ui.btnPlay.clicked.connect(self.reproducir_en_hilo)
        self.ui.btnStop.clicked.connect(self.stop)
        self.ui.btnEcualizar.clicked.connect(self.ecualizar)

    def abrirCancion(self):
        ruta = filedialog.askopenfilename(defaultextension=".wav",
                                               filetypes=[("Wave Files", "*.wav")])
        self.ecualizador = Ecualizador(ruta)
        self.ecualizador.calcularEspectroFrecuencias()
        print("Audio cargado")

    def obtenerGanancias(self):
        g1 = self.ui.sld1.value()
        g2 = self.ui.sld2.value()
        g3 = self.ui.sld3.value()
        g4 = self.ui.sld4.value()
        g5 = self.ui.sld5.value()
        g6 = self.ui.sld6.value()
        self.ecualizador.ganancias = [g1, g2, g3, g4, g5, g6]

    def play(self):
        print(self.ecualizador.ganancias)
        print("Reproduciendo")
        sd.play(self.ecualizador.audioEcualizado, self.ecualizador.fmuestreo)

    def stop(self):
        sd.stop()

    def ecualizar(self):
        self.ecualizador.decimacion(self.ecualizador.fmuestreo, self.ecualizador.muestras, self.ui.sldDecimacion.value())
        print("error")
        self.obtenerGanancias()
        self.ecualizador.actualizarBandas()
        self.ecualizador.ecualizarEspectro()
        self.ecualizador.obtenerAudioEcualizado()
        #sf.write('audio_ecualizado.wav', self.ecualizador.audioEcualizado, self.ecualizador.fmuestreo)
        print("Audio ecualizado")

    def reproducir_en_hilo(self):
        hilo = threading.Thread(target=self.play)
        hilo.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ctrl = Controlador()
    sys.exit(app.exec())