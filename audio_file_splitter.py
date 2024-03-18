import wave
import struct
import os


class AudioFileSplitter:
    def __init__(self, filepath):
        self.filepath = filepath
        self.output_dir = "calls"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        with wave.open(filepath, 'rb') as audio_file:
            self.sampwidth = audio_file.getsampwidth()
            self.channels = audio_file.getnchannels()
            self.framerate = audio_file.getframerate()
            self.nframes = audio_file.getnframes()
            self.samples = audio_file.readframes(self.nframes)
            self.basename = os.path.splitext(os.path.basename(filepath))[0]

    def _create_file_one_channel(self, name_suffix, values):
        filename = os.path.join(self.output_dir, f"{self.basename}_{name_suffix}.wav")
        with wave.open(filename, 'wb') as out_file:
            out_file.setframerate(self.framerate)
            out_file.setsampwidth(self.sampwidth)
            out_file.setnchannels(1)
            audio_data = struct.pack(f"<{len(values)}h", *values)
            out_file.writeframes(audio_data)

    def split(self):
        values = list(struct.unpack(f"<{self.nframes * self.channels}h", self.samples))
        left_channel = values[::2]  # Клиент
        right_channel = values[1::2]  # Оператор

        self._create_file_one_channel('client', left_channel)
        self._create_file_one_channel('operator', right_channel)
