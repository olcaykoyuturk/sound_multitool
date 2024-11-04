import wave
import numpy as np


def read_data(file_name):
    with wave.open(file_name, mode="rb") as wave_file:
        wave_file_data = wave_file.readframes(wave_file.getnframes())
        data = np.frombuffer(wave_file_data, dtype=np.int16)

        channels = wave_file.getnchannels()
        sample_width = wave_file.getsampwidth()
        sample_rate = wave_file.getframerate()
        n_frames = wave_file.getnframes()

        if wave_file.getnchannels() > 1:
            data = data.reshape(-1, wave_file.getnchannels())
            data = data.mean(axis=-1)

        time = np.linspace(0, (wave_file.getnframes() / wave_file.getframerate()), num=wave_file.getnframes())

    return data, time, channels, sample_width, sample_rate, n_frames
