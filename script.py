import requests
import gzip
import xml.etree.ElementTree as ET
import io

feed_url = "https://feeds.whatjobs.com/sinerj/sinerj_pt_BR.xml.gz"

response = requests.get(feed_url, stream=True)
if response.status_code == 200:
    with gzip.open(io.BytesIO(response.content), "rt", encoding="utf-8") as f:
        for event, elem in ET.iterparse(f, events=("start", "end")):
            if event == "end" and elem.tag == "job":  # Ajuste o nome do nó conforme o XML
                print(ET.tostring(elem, encoding="utf-8").decode())  # Teste com poucas linhas
                elem.clear()  # Libera memória
else:
    print("Erro ao baixar o feed:", response.status_code)
