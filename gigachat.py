import uuid
import requests
import urllib3

urllib3.disable_warnings()


class Auth():
    def __init__(self):
        self.Auth = 'xxx'
        self.payload = {'scope': 'GIGACHAT_API_PERS'}
        UUID = str(uuid.uuid4())
        self.url = 'https://ngw.devices.sberbank.ru:9443/api/v2/oauth'
        self.headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'application/json',
            'RqUID': UUID,
            'Authorization': f'Basic {self.Auth}'
        }

    def get_token(self) -> str:
        response = requests.request('POST', self.url, headers=self.headers, data=self.payload, verify=False)
        json_response = response.json()
        # giga_token = json_response['access_token']
        return json_response['access_token']

class Upload_to_giga():
    def __init__(self):
        self.url = 'https://gigachat-preview.devices.sberbank.ru/api/v1/files'

    def download_giga(self, auth_token, content, image_data):
        file = {'file': ('filename.jpg', image_data, 'image/jpeg')}
        payload = {
            'model': 'GigaChat-Pro',
            'message': [
                {
                    'role': 'user',
                    'content': content
                }
            ],
            'stream': False,
            'purpose': 'general'
        }
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        }

        response = requests.request('POST', self.url, headers=headers,
                                    data=payload, files=file, verify=False)
        json_response = response.json()
        return json_response['id']

class Extract():
    def __init__(self):
        self.url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'

    def extracting(self, auth_token, file_id):
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {auth_token}'
        }

        payload = {
            'model': 'GigaChat-Pro',
            'messages': [
                {
                    'role': 'user',
                    'content': 'переведи текст с картинки',
                    'attachments': [str(file_id)]
                }
            ]
        }

        response = requests.post(self.url, headers=headers, json=payload, verify=False)
        json_response = response.json()


        try:
            extracted_text = json_response['choices'][0]['message']['content']
            return extracted_text
        except KeyError as e:
            print(f"Ошибка при извлечении текста: {e}")
            return None
