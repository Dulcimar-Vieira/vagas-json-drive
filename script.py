import requests
import gzip
import xml.etree.ElementTree as ET
import io
import json
import os

# URL do feed
feed_url = "https://feeds.whatjobs.com/sinerj/sinerj_pt_BR.xml.gz"

# Baixar o feed XML comprimido
response = requests.get(feed_url, stream=True)

if response.status_code == 200:
    with gzip.open(io.BytesIO(response.content), "rt", encoding="utf-8") as f:
        jobs = []
        for event, elem in ET.iterparse(f, events=("end",)):
            if elem.tag == "job":  # Ajuste conforme a estrutura do XML
                job_data = {
                    "title": elem.findtext("title", ""),
                    "description": elem.findtext("description", ""),
                    "company": elem.findtext("company", ""),
                    "location": elem.findtext("location", ""),
                    "url": elem.findtext("url", ""),
                }
                jobs.append(job_data)
                elem.clear()  # Libera memória

                # Criar um novo JSON a cada 50MB (aproximadamente)
                if len(jobs) >= 5000:  # Ajuste esse número conforme o tamanho médio dos dados
                    json_path = os.path.join(json_folder, f"part_{len(os.listdir(json_folder)) + 1}.json")
                    with open(json_path, "w", encoding="utf-8") as json_file:
                        json.dump(jobs, json_file, ensure_ascii=False, indent=2)
                    jobs = []  # Limpa a lista para o próximo lote

        # Salvar o restante dos dados em um JSON final
        if jobs:
            json_path = os.path.join(json_folder, f"part_{len(os.listdir(json_folder)) + 1}.json")
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(jobs, json_file, ensure_ascii=False, indent=2)

        print(f"JSONs gerados: {os.listdir(json_folder)}")

else:
    print("Erro ao baixar o feed:", response.status_code)
