import numpy as np


# amplitude - time graph
def oscilloscope(time, data):
    return time, data


# fft calculator
def fft_calculator(data, sample_rate):
    fft_result = np.fft.fft(data)
    fft_freq = np.fft.fftfreq(len(data), d=1 / sample_rate)

    positive_freq_indices = np.where(fft_freq >= 0)
    fft_freq = fft_freq[positive_freq_indices]
    fft_result = fft_result[positive_freq_indices]

    fft_result = fft_result / len(data)

    return fft_freq, fft_result


# amplitude - frequency
def fft_graph(data, sample_rate, level_type):
    fft_freq, fft_result = fft_calculator(data, sample_rate)

    if level_type == 'pk':
        scaled_amplitudes = np.abs(fft_result)
    elif level_type == 'pp':
        scaled_amplitudes = 2 * np.abs(fft_result)
    elif level_type == 'rms':
        rms_values = np.sqrt(np.mean(np.abs(fft_result) ** 2))
        epsilon = 1e-10
        rms_values = np.where(rms_values == 0, epsilon, rms_values)
        scaled_amplitudes = np.abs(fft_result) / rms_values

    return fft_freq, fft_result, scaled_amplitudes


# octave calculator
def octave_calculator(data, sample_rate):
    octave_band_limits = [
        (31.5, 22.4, 44.8),
        (63, 44.8, 89.6),
        (125, 89.6, 178),
        (250, 178, 355),
        (500, 355, 710),
        (1000, 710, 1420),
        (2000, 1420, 2840),
        (4000, 2840, 5680),
        (8000, 5680, 11360),
        (16000, 11360, 22720)
    ]

    fft_freq, fft_result = fft_calculator(data, sample_rate)
    octave_levels = []
    octave_centers = []
    center_freqs = []

    power_spectrum = np.abs(fft_result) ** 2

    for center_freq, lower_freq, upper_freq in octave_band_limits:
        band_indices = np.where((fft_freq >= lower_freq) & (fft_freq <= upper_freq))
        band_power = np.sum(power_spectrum[band_indices])

        if band_power > 0:
            band_level = 10 * np.log10(band_power)
        else:
            band_level = 0  # Use 0 dB for bands with no power

        # Convert negative levels to 0 dB
        band_level = max(band_level, 0)

        octave_levels.append(band_level)
        octave_centers.append(center_freq)
        center_freqs.append(center_freq)

    return octave_centers, octave_levels, center_freqs


# spectrogram calculator
def spectrogram_calculator(data, window_size, overlap, sample_rate):
    step_size = window_size - overlap
    shape = (data.size - window_size + 1, window_size)
    strides = (data.strides[0], data.strides[0])
    windows = np.lib.stride_tricks.as_strided(data, shape=shape, strides=strides)[::step_size]
    windowed_data = windows * np.hanning(window_size)
    spectrogram = np.abs(np.fft.rfft(windowed_data, axis=1)) ** 2
    spectrogram = spectrogram.T

    spectrogram[spectrogram == 0] = 1e-10
    frequencies = np.fft.rfftfreq(window_size, d=1 / sample_rate)
    time = np.arange(spectrogram.shape[1]) * (window_size - overlap) / sample_rate

    return time, frequencies, spectrogram



