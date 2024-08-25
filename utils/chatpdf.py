import json
import re

import requests
from django.conf import settings


class ChatPDF():
    def __init__(self):
        self.headers = {
            'x-api-key': settings.CHATPDF_API_KEY,
            'Content-Type': 'application/json'
        }
        
    def upload_pdf(self, url):
        data = {
            'url': url
        }

        response = requests.post(
            'https://api.chatpdf.com/v1/sources/add-url', headers=self.headers, json=data)

        if response.status_code == 200:
            return response.json()['sourceId']
        print(response.text)
        return None
    
    def _extract_dict(self, body):
        json_string = re.search(r"```json(.*)```", body, re.DOTALL).group(1) 
        json_data = json.loads(json_string)
        return json_data

    def message(self, src_id, message):
        data = {
            'sourceId': src_id,
            'messages': [
                {
                    'role': "assistant",
                    'content': "Aku adalah ahli pemberi feedback terhadap modul ajar dalam bahasa Indonesia.",
                },
                {
                    'role': "user",
                    'content': message,
                }
            ]
        }
        
        response = requests.post(
            'https://api.chatpdf.com/v1/chats/message', headers=self.headers, json=data)

        if response.status_code == 200:
            print('Result:', response.json()['content'])
            res = response.json()['content']
            return json.loads(res.strip().replace('Result: ```json','').replace('```',''))
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)
            return response.text
            
    def check_must_have_components(self, src_id):
        data = {
            'sourceId': src_id,
            'messages': [
                {
                    'role': "user",
                    'content': """apakah modul ini memiliki komponen wajib dari modul ajar:
1. Tujuan Pembelajaran
2. Langkah-langkah Pembelajaran atau Kegiatan Pembelajaran 
3. Asesmen Pembelajaran. 

Tandai komponen wajib yang tidak tertera. Respon dalam format JSON: {"Tujuan Pembelajaran": true, ...}""",
                }
            ]
        }
        
        response = requests.post(
            'https://api.chatpdf.com/v1/chats/message', headers=self.headers, json=data)

        if response.status_code == 200:
            res = response.json()['content']
            print(res)
            return self._extract_dict(res)
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)
            return response.text
            
    def provide_assessment(self, src_id):
        data = {
            'sourceId': src_id,
            'messages': [
                {
                    'role': "user",
                    'content': """Berikan penilaian terhadap beberapa hal berikut: 
(1) kesesuaian Tujuan Pembelajaran dengan Capaian Pembelajaran; 
(2) kesesuaian metode dan media yang digunakan dengan tujuan, karakteristik siswa secara umum pada tahap usianya dan kompetensi yang ingin dicapainya; 
(3) kesesuaian penilaian dengan Tujuan Pembelajaran dan Karakteristik siswa serta kompetensi dan konteksnya.

Respon dalam format JSON: {"1": {"penilaian": <penilaian>, "alasan": <alasan>}, "2": {"penilaian": <penilaian>, "alasan": <alasan>}, "3": {"penilaian": <penilaian>, "alasan": <alasan>}}""",
                }
            ]
        }
        
        response = requests.post(
            'https://api.chatpdf.com/v1/chats/message', headers=self.headers, json=data)

        if response.status_code == 200:
            res = response.json()['content']
            print(res)
            return self._extract_dict(res)
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)
            return response.text
            
    def get_suggestion(self, src_id):
        data = {
            'sourceId': src_id,
            'messages': [
                {
                    'role': "user",
                    'content': "Berikan saran atau alternatif pada media dan metode pembelajaran yang digunakan dalam modul ajar ini. Respon dalam format markdown."
                }
            ]
        }
        
        response = requests.post(
            'https://api.chatpdf.com/v1/chats/message', headers=self.headers, json=data)

        if response.status_code == 200:
            return response.json()['content']
        else:
            print('Status:', response.status_code)
            print('Error:', response.text)
        return response.text