import os
import json
from audio_file_splitter import AudioFileSplitter
from file_analyzer import FileAnalyzer


class MainProcessor:
    def __init__(self, input_dir, output_file, api_key, api_key_password):
        self.input_dir = input_dir
        self.output_file = output_file
        self.api_key = api_key
        self.api_key_password = api_key_password
        self.data = {"data": []}

    def process_files(self):
        for filename in os.listdir(self.input_dir):
            if filename.endswith(".wav"):
                dialog_name = os.path.splitext(filename)[0]
                filepath = os.path.join(self.input_dir, filename)

                splitter = AudioFileSplitter(filepath)
                splitter.split()

                client_filepath = os.path.join(splitter.output_dir, f"{dialog_name}_client.wav")
                operator_filepath = os.path.join(splitter.output_dir, f"{dialog_name}_operator.wav")

                client_emotion = self.analyze_and_remove(client_filepath)
                operator_emotion = self.analyze_and_remove(operator_filepath)

                self.data["data"].append({
                    "dialog": dialog_name,
                    "moods": {
                        "client mood": client_emotion,
                        "operator mood": operator_emotion
                    }
                })

        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def analyze_and_remove(self, filepath):
        analyzer = FileAnalyzer(self.api_key, self.api_key_password, filepath)
        emotion = analyzer.send_file_for_analysis()
        os.remove(filepath)
        return emotion


# Использование
api_key = "api_key"
api_key_password = "api_key_password"
input_dir = r"input_dir"
output_file = "results.json"
processor = MainProcessor(input_dir, output_file, api_key, api_key_password)
processor.process_files()
