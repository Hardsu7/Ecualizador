import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, freqz

class Ecualizador:

    # Ganancias ajustadas para las bandas (para ver cambios más evidentes)
    ganancias = [2, 1.5, 1.2, 0.8, 0.5, 1.8]  # Cambié las ganancias para cada banda

    def __init__(self, audioRuta):
        self.obtenerAudio(audioRuta)
        self.crearIndicesBandas()
        self.bandas = np.ones_like(self.muestras)

    def obtenerAudio(self, ruta):  # PASO 1
        """Leer el archivo de audio."""
        self.muestras, self.fmuestreo = sf.read(ruta)
        self.segundos = np.arange(0, len(self.muestras) / self.fmuestreo, 1 / self.fmuestreo)

    def crearIndicesBandas(self):
        """Crear índices de las bandas de frecuencia."""
        self.indiceBandas = []
        banderas_bandas = [True, True, True, True, True, True]
        frec_por_muestra = (self.fmuestreo / 2) / len(self.muestras)
        for i in range(0, len(self.muestras)):
            frecuencia = i * frec_por_muestra
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
                self.indiceBandas.append(i)
                break

    def calcularEspectroFrecuencias(self):  # PASO 2
        """Calcular la FFT del audio para obtener el espectro de frecuencias."""
        self.ftmuestras = np.fft.fft(self.muestras)
        self.freqs = np.arange(0, self.fmuestreo / 2, (self.fmuestreo / 2) / len(self.muestras))

    def actualizarBandas(self):
        """Actualizar las ganancias en las bandas definidas."""
        for i in range(len(self.bandas)):
            if i in range(self.indiceBandas[0], self.indiceBandas[1]): self.bandas[i] = self.ganancias[0]
            if i in range(self.indiceBandas[1], self.indiceBandas[2]): self.bandas[i] = self.ganancias[1]
            if i in range(self.indiceBandas[2], self.indiceBandas[3]): self.bandas[i] = self.ganancias[2]
            if i in range(self.indiceBandas[3], self.indiceBandas[4]): self.bandas[i] = self.ganancias[3]
            if i in range(self.indiceBandas[4], self.indiceBandas[5]): self.bandas[i] = self.ganancias[4]
            if i in range(self.indiceBandas[5], self.indiceBandas[6]): self.bandas[i] = self.ganancias[5]

    def ecualizarEspectro(self):
        """Aplicar las ganancias al espectro."""
        self.espectroEcualizado = self.ftmuestras * self.bandas

    def obtenerAudioEcualizado(self):  # PASO 5
        """Obtener el audio ecualizado a partir del espectro modificado."""
        self.audioEcualizado = np.real(np.fft.ifft(self.espectroEcualizado))

    def graficarSenal(self, x, senal, titulo, xlabel, ylabel, nombre_archivo):
        """Graficar una señal y guardar la imagen."""
        plt.figure(figsize=(10, 5))
        plt.plot(x, senal)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(titulo)
        plt.savefig(f'{nombre_archivo}.png')  # Guardar imagen en el directorio actual
        plt.close()

    def ecualizacionDirecta(self):
        """Metodo de ecualización usando una librería directa (ejemplo con filtros)."""
        nyquist = 0.5 * self.fmuestreo
        low = 16 / nyquist
        mid = 250 / nyquist
        high = 6000 / nyquist

        # Filtros de paso de banda para cada banda
        b_low, a_low = butter(4, low, btype='low')
        b_mid, a_mid = butter(4, [low, high], btype='band')
        b_high, a_high = butter(4, high, btype='high')

        # Aplicar filtros al audio
        low_filtered = lfilter(b_low, a_low, self.muestras)
        mid_filtered = lfilter(b_mid, a_mid, self.muestras)
        high_filtered = lfilter(b_high, a_high, self.muestras)

        # Sumar las señales filtradas para simular ecualización
        audio_ecualizado_directo = low_filtered + mid_filtered + high_filtered
        return audio_ecualizado_directo

# Crear un objeto de la clase Ecualizador
ruta_audio = 'C:/Users/Pablo/Desktop/Ecualizador/British Theme - American Conquest.wav'
ecualizador = Ecualizador(ruta_audio)

# Graficar y guardar la señal de audio original
ecualizador.graficarSenal(ecualizador.segundos, ecualizador.muestras, 'Señal de Audio Original', 'Tiempo [s]', 'Amplitud', 'audio_original')

# Calcular el espectro y ecualizar
ecualizador.calcularEspectroFrecuencias()
ecualizador.actualizarBandas()
ecualizador.ecualizarEspectro()
ecualizador.obtenerAudioEcualizado()

# Graficar y guardar el audio ecualizado por tu metodo
ecualizador.graficarSenal(ecualizador.segundos, ecualizador.audioEcualizado, 'Señal Ecualizada (Método FFT)', 'Tiempo [s]', 'Amplitud', 'audio_ecualizado_metodo_FFT')

# Aplicar la ecualización directa y graficar el resultado
audio_ecualizado_directo = ecualizador.ecualizacionDirecta()
ecualizador.graficarSenal(ecualizador.segundos, audio_ecualizado_directo, 'Señal Ecualizada (Método Filtros Directos)', 'Tiempo [s]', 'Amplitud', 'audio_ecualizado_directo')
