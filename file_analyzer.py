import requests


class FileAnalyzer:
    def __init__(self, api_key, api_key_password, file_path):
        self.api_key = api_key
        self.api_key_password = api_key_password
        self.file_path = file_path
        self.url = "https://cloud.emlo.cloud/analysis/analyzeFile"

    def send_file_for_analysis(self):
        params = {
            "outputType": "json",
            "sensitivity": "normal",
            "dummyResponse": "false",
            "apiKey": self.api_key,
            "apiKeyPassword": self.api_key_password,
            "consentObtainedFromDataSubject": "true",
        }

        files = {"file": open(self.file_path, "rb")}

        response = requests.post(self.url, files=files, data=params)
        if response.status_code == 200:
            response_data = response.json()
            return self.extract_emotions(response_data)
        else:
            print(f"Ошибка запроса: {response.status_code}")
            return {}

    def extract_emotions(self, response):
        # Предполагаем, что есть только один канал для анализа, так что берем первый попавшийся
        data = response.get("data", {}).get("reports", {})
        for report in data.values():
            if 'profile' in report:
                return {emotion: details['averageLevel'] for emotion, details in report['profile'].items() if
                        'averageLevel' in details}
        return {}
