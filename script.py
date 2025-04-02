import requests

feed_url = "https://feeds.whatjobs.com/sinerj/sinerj_pt_BR.xml.gz"
response = requests.get(feed_url)

if response.status_code == 200:
    print("Download bem-sucedido! Tamanho do arquivo:", len(response.content), "bytes")
else:
    print("Erro ao baixar o feed:", response.status_code)
import gzip
import io

with gzip.open(io.BytesIO(response.content), "rt", encoding="utf-8") as f:
    xml_data = f.read()

print(xml_data[:1000])  # Exibir os primeiros 1000 caracteres para verificar se o XML foi extraído corretamente

import xmltodict

try:
    feed_dict = xmltodict.parse(xml_data)
    print("Conversão bem-sucedida!")
except Exception as e:
    print("Erro ao converter XML para JSON:", e)
