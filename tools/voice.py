import numpy as np
import pyaudio
import wave
import threading


class VoicePlayer:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.thread = None
        self.stop_flag = threading.Event()

    def play(self, file_path):
        self.stop()
        self.stop_flag.clear()
        self.thread = threading.Thread(target=self._play_audio, args=(file_path,))
        self.thread.start()

    def _play_audio(self, file_path):
        try:
            wf = wave.open(file_path, 'rb')
            self.stream = self.p.open(format=self.p.get_format_from_width(wf.getsampwidth()),
                                      channels=wf.getnchannels(),
                                      rate=wf.getframerate(),
                                      output=True)
            data = wf.readframes(1024)
            while data and not self.stop_flag.is_set():
                self.stream.write(data)
                data = wf.readframes(1024)
        except Exception as e:
            print(f"Error playing audio: {e}")
        finally:
            self._cleanup()

    def stop(self):
        self.stop_flag.set()
        if self.thread and self.thread != threading.current_thread():
            self.thread.join()
        self._cleanup()

    def _cleanup(self):
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                print(f"Error stopping stream: {e}")
            finally:
                self.stream = None
        if self.thread and self.thread != threading.current_thread():
            self.thread = None

    def terminate(self):
        self.stop()
        self.p.terminate()


class VoiceRecorder:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.stream = None
        self.thread = None
        self.frames = []
        self.stop_flag = threading.Event()
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100

    def record(self, file_path):
        self.stop()
        self.stop_flag.clear()
        self.thread = threading.Thread(target=self._record_audio, args=(file_path,))
        self.thread.start()

    def _record_audio(self, file_path):
        try:
            self.frames = []
            self.stream = self.p.open(format=self.format,
                                      channels=self.channels,
                                      rate=self.rate,
                                      input=True,
                                      frames_per_buffer=1024)
            while not self.stop_flag.is_set():
                data = self.stream.read(1024)
                self.frames.append(data)
        except Exception as e:
            print(f"Error recording audio: {e}")
        finally:
            self._cleanup()
            self._save_wave(file_path)

    def stop(self):
        self.stop_flag.set()
        if self.thread and self.thread != threading.current_thread():
            self.thread.join()
        self._cleanup()

    def _cleanup(self):
        if self.stream:
            try:
                self.stream.stop_stream()
                self.stream.close()
            except Exception as e:
                print(f"Error stopping stream: {e}")
            finally:
                self.stream = None
        if self.thread and self.thread != threading.current_thread():
            self.thread = None

    def _save_wave(self, file_path):
        if not self.frames:
            print("No audio data to save.")
            return
        try:
            if not file_path.lower().endswith('.wav'):
                file_path += '.wav'

            wf = wave.open(file_path, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            print(f"Audio recorded and saved to {file_path}")
        except Exception as e:
            print(f"Error saving wave file: {e}")

    def terminate(self):
        self.stop()
        self.p.terminate()


class RealTime:
    def __init__(self, rate=44100, chunk=1024, display_seconds=5):
        self.RATE = rate
        self.CHUNK = chunk
        self.DISPLAY_SECONDS = display_seconds
        self.BUFFER_SIZE = int(self.RATE * self.DISPLAY_SECONDS)

        self.p = pyaudio.PyAudio()
        self.stream = None
        self.audio_data = np.zeros(self.BUFFER_SIZE)

    def start(self):
        if self.stream is None:
            self.stream = self.p.open(format=pyaudio.paInt16, channels=1, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)

    def stop(self):
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None

    def update(self):
        if self.stream is not None:
            data = np.frombuffer(self.stream.read(self.CHUNK), dtype=np.int16)
            self.audio_data = np.roll(self.audio_data, -len(data))
            self.audio_data[-len(data):] = data
        return self.audio_data

    def close(self):
        self.stop()
        self.p.terminate()
