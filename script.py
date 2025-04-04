import requests
import gzip
import xml.etree.ElementTree as ET
import io
import json
import os

# URL do feed
feed_url = "https://feeds.whatjobs.com/sinerj/sinerj_pt_BR.xml.gz"

# Criar pasta para os arquivos JSON
json_folder = "json_parts"
os.makedirs(json_folder, exist_ok=True)

# Contador de arquivos
file_count = 1

# Baixar o feed XML comprimido
response = requests.get(feed_url, stream=True)

if response.status_code == 200:
    with gzip.open(io.BytesIO(response.content), "rt", encoding="utf-8") as f:
        jobs = []
        for event, elem in ET.iterparse(f, events=("end",)):
            if elem.tag == "job":
                job_data = {
                    "title": elem.findtext("title", ""),
                    "description": elem.findtext("description", ""),
                    "company": elem.findtext("company", ""),
                    "location": elem.findtext("location", ""),
                    "url": elem.findtext("url", ""),
                }
                jobs.append(job_data)
                elem.clear()

                if len(jobs) >= 1000:
                    json_path = os.path.join(json_folder, f"part_{file_count}.json")
                    with open(json_path, "w", encoding="utf-8") as json_file:
                        json.dump(jobs, json_file, ensure_ascii=False, indent=2)
                    print(f"Arquivo salvo: {json_path}")
                    jobs = []
                    file_count += 1

        if jobs:
            json_path = os.path.join(json_folder, f"part_{file_count}.json")
            with open(json_path, "w", encoding="utf-8") as json_file:
                json.dump(jobs, json_file, ensure_ascii=False, indent=2)
            print(f"Arquivo final salvo: {json_path}")

    print(f"JSONs gerados: {os.listdir(json_folder)}")

else:
    print("Erro ao baixar o feed:", response.status_code)
