import numpy as np
import wave


def generate_white_noise(duration, sample_rate, amplitude, pan):
    num_samples = int(duration * sample_rate)
    noise = np.random.normal(0, amplitude, num_samples)
    left_channel = noise * (1 - pan)
    right_channel = noise * pan
    stereo_noise = np.vstack((left_channel, right_channel)).T.flatten()
    return stereo_noise


def generate_pink_noise(duration, sample_rate, amplitude, pan):
    num_samples = int(duration * sample_rate)
    white_noise = np.random.normal(0, amplitude, num_samples)
    uneven = num_samples % 2
    X = np.fft.rfft(white_noise)
    S = np.sqrt(np.arange(len(X)) + 1)
    pink_noise = (np.fft.irfft(X / S)).real
    if uneven:
        pink_noise = pink_noise[:-1]
    pink_noise = pink_noise * amplitude
    left_channel = pink_noise * (1 - pan)
    right_channel = pink_noise * pan
    stereo_noise = np.vstack((left_channel, right_channel)).T.flatten()
    return stereo_noise


def generate_sweep(lower_freq, upper_freq, duration, sample_rate, amplitude, pan, repeat, swept_sine):
    num_samples = int(duration * sample_rate)
    t = np.linspace(0, duration, num_samples, endpoint=False)
    if swept_sine:
        sweep = amplitude * np.sin(2 * np.pi * (lower_freq * t + (upper_freq - lower_freq) / (2 * duration) * t**2))
    else:
        sweep = amplitude * np.linspace(lower_freq, upper_freq, num_samples)

    if repeat:
        sweep = np.tile(sweep, int(duration))

    left_channel = sweep * (1 - pan)
    right_channel = sweep * pan
    stereo_sweep = np.vstack((left_channel, right_channel)).T.flatten()
    return stereo_sweep


def generate_waveform(waveform_type, frequency, duration, sample_rate, amplitude, pan):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    if waveform_type == 'sine':
        wave = amplitude * np.sin(2 * np.pi * frequency * t)
    elif waveform_type == 'square':
        wave = amplitude * np.sign(np.sin(2 * np.pi * frequency * t))
    elif waveform_type == 'triangle':
        wave = amplitude * (2 * np.abs(2 * (t * frequency - np.floor(t * frequency + 0.5))) - 1)
    elif waveform_type == 'sawtooth':
        wave = amplitude * (2 * (t * frequency - np.floor(t * frequency + 0.5)))
    else:
        raise ValueError("Unsupported waveform type: {}".format(waveform_type))

    left_channel = wave * (1 - pan)
    right_channel = wave * pan
    stereo_wave = np.vstack((left_channel, right_channel)).T.flatten()
    return stereo_wave


def save_wave_file(filename, data, sample_rate):
    if not filename.lower().endswith('.wav'):
        filename += '.wav'

    if data.ndim == 1:
        num_channels = 1  # Mono
    elif data.ndim == 2:
        num_channels = data.shape[1]  # Stereo (veya diğer çoklu kanallar)
    else:
        raise ValueError("Data'nın boyutu 1D veya 2D olmalıdır.")

    sampwidth = 2

    # Sıkıştırma türü ve adı
    comptype = "NONE"
    compname = "not compressed"

    # Verileri 16-bit PCM formatına dönüştürün
    data = (data * 32767).astype(np.int16)

    # Kanalları interleave etme
    if num_channels == 1:  # Mono
        interleaved = data.flatten()
    else:  # Stereo
        interleaved = data.flatten()

    # Çerçeve sayısını hesaplayın
    n_frames = len(interleaved) // num_channels

    # Dosyayı yazma işlemi
    try:
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(num_channels)
            wf.setsampwidth(sampwidth)
            wf.setframerate(sample_rate)
            wf.setnframes(n_frames)
            wf.setcomptype(comptype, compname)
            wf.writeframes(interleaved.tobytes())
        print(f"Kayıt edildi: {filename}")
    except Exception as e:
        print(f"Hata: {e}")
