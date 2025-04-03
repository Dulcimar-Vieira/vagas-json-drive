import requests
import gzip
import xml.etree.ElementTree as ET
import io

feed_url = "https://feeds.whatjobs.com/sinerj/sinerj_pt_BR.xml.gz"

import os

json_folder = "json_parts"
os.makedirs(json_folder, exist_ok=True)  # Garante que a pasta existe
if not os.path.exists(json_folder):
    print(f"Erro: A pasta {json_folder} não foi criada!")
elif not os.listdir(json_folder):
    print(f"Erro: A pasta {json_folder} está vazia!")
else:
    print(f"Arquivos gerados: {os.listdir(json_folder)}")

response = requests.get(feed_url, stream=True)
if response.status_code == 200:
    with gzip.open(io.BytesIO(response.content), "rt", encoding="utf-8") as f:
        for event, elem in ET.iterparse(f, events=("start", "end")):
            if event == "end" and elem.tag == "job":  # Ajuste o nome do nó conforme o XML
                print(ET.tostring(elem, encoding="utf-8").decode())  # Teste com poucas linhas
                elem.clear()  # Libera memória
else:
    print("Erro ao baixar o feed:", response.status_code)
