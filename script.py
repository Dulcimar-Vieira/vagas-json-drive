import gzip
import requests
import xmltodict

# URL do feed
feed_url = "https://feeds.whatjobs.com/sinerj/sinerj_pt_BR.xml.gz"

# Baixar o feed comprimido
response = requests.get(feed_url)
if response.status_code == 200:
    with gzip.decompress(response.content) as f:
        xml_data = f.read().decode("utf-8")
else:
    print("Erro ao baixar o feed:", response.status_code)
    exit()

# Verificar os primeiros caracteres do XML
print(xml_data[:500])

# Converter para JSON
feed_dict = xmltodict.parse(xml_data)
