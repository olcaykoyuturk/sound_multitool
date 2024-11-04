class DataContainer:
    def __init__(self):
        self._data = None
        self._time = None
        self._channels = None
        self._sample_width = None
        self._sample_rate = None
        self._n_frames = None
        self._file_path = None

    def set_data(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def set_time(self, time):
        self._time = time

    def get_time(self):
        return self._time

    def set_channels(self, channels):
        self._channels = channels

    def get_channels(self):
        return self._channels

    def set_sample_width(self, sample_width):
        self._sample_width = sample_width

    def get_sample_width(self):
        return self._sample_width

    def set_sample_rate(self, sample_rate):
        self._sample_rate = sample_rate

    def get_sample_rate(self):
        return self._sample_rate

    def set_n_frames(self, n_frames):
        self._n_frames = n_frames

    def get_n_frames(self):
        return self._n_frames

    def set_file_path(self, file_path):
        self._file_path = file_path

    def get_file_path(self):
        return self._file_path
