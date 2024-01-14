import matplotlib.pyplot as plt
import numpy as np
import wave
import heartpy as hp
import os

file_path = "LAB5_500HzFHR.wav"
pictures_dir = "pictures"
data_save = "data_target.csv"

def plot_waveform(signal, sample_rate, pic_name):
    """Create plot in time domain"""
    time = np.arange(0, len(signal)) / sample_rate
    plt.plot(time, signal)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.title('Waveform in Time Domain')
    plt.savefig(os.path.join(os.path.curdir, pictures_dir, pic_name))
    plt.show()

def read_wav_file(file_path):
    """Get data from wav file"""
    with wave.open(file_path, 'rb') as wave_file:
        # get the audio signal
        signal = np.frombuffer(wave_file.readframes(-1), dtype=np.int16)
        # get the sample rate
        sample_rate = wave_file.getframerate()
    return signal, sample_rate

def plot_frequency_spectrum(freq, fft_result, pic_name):
    """Create plot in frequency domain"""

    # discard complex parts of fft
    real_part = [x.real for x in fft_result]

    plt.plot(freq, real_part)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Amplitude Spectrum')
    plt.title('Frequency Spectrum')
    plt.savefig(os.path.join(os.path.curdir, pictures_dir, pic_name))
    plt.show()


if __name__ == "__main__":

    # read the wav file
    signal, sample_rate = read_wav_file(file_path)

    # plot the initial time waveform
    plot_waveform(signal, sample_rate, "time_no_filter.png")

    # perform fft
    n = len(signal)
    # check what the sample rate is
    # print(sample_rate)
    freq = np.fft.fftfreq(n, d=1/sample_rate)
    fft_result = np.fft.fft(signal)

    # plot the fft (signal in freq domain)
    plot_frequency_spectrum(freq, fft_result, "freq_no_filter.png")

    # do the filtering manually (sample rate is 500, so cut_off_freq < 250)
    cut_off_freq = 170
    fft_filtered = fft_result.copy()
    fft_filtered[np.abs(freq) < cut_off_freq] = 0

    # plot the fft (signal in freq domain) after filtering
    plot_frequency_spectrum(freq, fft_filtered, "freq_with_filter.png")

    # perform inverse fft and plot signal in time domain
    signal_filtered = np.real(np.fft.ifft(fft_filtered))
    plot_waveform(signal_filtered, sample_rate, "time_with_filter.png")

    # shifting datapoints above 0 (if not shifted BPM becomes "nan")
    signal_filtered = [int(i)+21000 for i in signal_filtered]

    # heartpy package needs its own format of data, which is not well specified
    # apparently it works if it gets data from csv file, feeding them directly doesn't work
    np.savetxt(data_save, signal_filtered, delimiter='\n', fmt='%d')
    data = hp.get_data(data_save)

    # estimate BPM value
    working_data, measures = hp.process(data, sample_rate)
    print(f"Estimated BPM: {measures['bpm']}")
