import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
import sounddevice as sd
from scipy import signal

class Ecualizador:

    bandas = [(16,60), (60,250), (250,2000), (2000,4000), (4000,6000), (6000,16000)]
    ganancias = [1, 1, 1, 1, 1, 1]

    def __init__(self, audioRuta):
        self.ruta = audioRuta
        self.obtenerAudio()
        self.crearFiltrosBandas()

    def graficarSenal(self, x, senal, titulo, xlabel, ylabel):
        plt.figure(figsize=(10, 5))
        plt.plot(x, senal)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(titulo)
        plt.show()

    def obtenerAudio(self):#PASO 1
        self.muestras, self.fmuestreo = sf.read(self.ruta)
        self.segundos = np.arange(0, len(self.muestras) / self.fmuestreo, 1 / self.fmuestreo)

    def crearBandas(self):
        self.indiceBandas = []#Los índices dónde empieza cada banda de frecuencias en las muestras
        banderas_bandas = [True, True, True, True, True, True]
        frec_xmuestra = (self.fmuestreo/2) / len(self.muestras)
        for i in range(0, len(self.muestras)):
            frecuencia = i * frec_xmuestra
            if frecuencia >= 16 and banderas_bandas[0]:
                self.indiceBandas.append(i)
                banderas_bandas[0] = False
            if frecuencia >= 60 and banderas_bandas[1]:
                self.indiceBandas.append(i)
                banderas_bandas[1] = False
            if frecuencia >= 250 and banderas_bandas[2]:
                self.indiceBandas.append(i)
                banderas_bandas[2] = False
            if frecuencia >= 2000 and banderas_bandas[3]:
                self.indiceBandas.append(i)
                banderas_bandas[3] = False
            if frecuencia >= 4000 and banderas_bandas[4]:
                self.indiceBandas.append(i)
                banderas_bandas[4] = False
            if frecuencia >= 6000 and banderas_bandas[5]:
                self.indiceBandas.append(i)
                banderas_bandas[5] = False
            if frecuencia >= 16000:
                self.indiceBandas.append(i) #El ultimo indice indica dónde termina la banda de frecuencias
                break

    def crearFiltrosBandas(self):
        self.b_coeffs = []
        self.a_coeffs = []
        for i, banda in enumerate(self.bandas):
            fbaja, falta = banda
            nyquist = 0.5 * self.fmuestreo
            baja = fbaja / nyquist
            alta = falta / nyquist
            b, a = signal.butter(4, [baja, alta], btype='bandpass', fs=self.fmuestreo, analog=False)
            self.b_coeffs.append(b * self.ganancias[i])#Aplica la ganancia al filtro
            self.a_coeffs.append(a)

    def calcularEspectroFrecuencias(self):#PASO 2
        self.ftmuestras = np.fft.fft(self.muestras)[:len(self.muestras)//2]
        self.freqs = np.arange(0, self.fmuestreo / 2, (self.fmuestreo / 2) / len(
            self.muestras))  # Las frecuencia máxima que puede tener la fft es igual a la frecuencia de muestreo/2

    def modificarMagnitudBanda(self, banda, magnitud):#PASO 3
        self.ganancias[banda] = magnitud

    def ecualizarEspectro(self):#PASO 4
        self.espectroEcualizado = np.zeros_like(self.ftmuestras)
        self.espectroEcualizado = self.ftmuestras * self.bandas[:len(self.bandas)//2]

    def ecualizarAudio(self):#PASO 4
        self.audioEcualizado = np.zeros_like(self.muestras, dtype=np.float64)
        for b, a in zip(self.b_coeffs, self.a_coeffs):
            self.audioEcualizado += signal.lfilter(b, a, self.muestras)
        self.audioEcualizado /= np.max(np.abs(self.audioEcualizado))

    def construirAudioEcualizado(self):#PASO 5
        self.audioEcualizado = np.array(np.real(np.fft.ifft(self.espectroEcualizado)))

    def reproducirAudioEcualizado(self):#PASO 6
        sd.play(self.audioEcualizado, self.fmuestreo)
        sd.wait()