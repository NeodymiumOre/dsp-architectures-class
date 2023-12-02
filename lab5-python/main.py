import matplotlib.pyplot as plt
import numpy as np
import wave


def plot_waveform(signal, sample_rate):
    time = np.arange(0, len(signal)) / sample_rate
    plt.plot(time, signal)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Waveform in Time Domain')
    plt.show()

def read_wav_file(file_path):
    with wave.open(file_path, 'rb') as wave_file:
        # get the audio signal
        signal = np.frombuffer(wave_file.readframes(-1), dtype=np.int16)
        # get the sample rate
        sample_rate = wave_file.getframerate()
    return signal, sample_rate

def plot_frequency_spectrum(freq, fft_result):
    plt.plot(freq, fft_result)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude Spectrum')
    plt.title('Frequency Spectrum')
    plt.show()


if __name__ == "__main__":

    file_path = "LAB5_500HzFHR.wav"

    # read the wav file
    signal, sample_rate = read_wav_file(file_path)

    # plot the waveform
    plot_waveform(signal, sample_rate)

    # perform fft
    n = len(signal)
    # print(sample_rate)
    freq = np.fft.fftfreq(n, d=1/sample_rate)
    fft_result = np.fft.fft(signal)

    # plot the fft
    plot_frequency_spectrum(freq, fft_result)

    # do the filtering
    cut_off_freq = 170
    fft_filtered = fft_result.copy()
    fft_filtered[np.abs(freq) < cut_off_freq] = 0

    plot_frequency_spectrum(freq, fft_filtered)

    # perform inverse fft
    signal_filtered = np.fft.ifft(fft_filtered)
    plot_waveform(signal_filtered, sample_rate)
