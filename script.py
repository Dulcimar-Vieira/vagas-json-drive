import requests
import xmltodict
import json
import os

# URL do feed XML
FEED_URL = "https://feeds.whatjobs.com/sinerj/sinerj_pt_BR.xml.gz"

# Pasta onde os arquivos JSON serão salvos
OUTPUT_DIR = "json_parts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Baixar o XML
response = requests.get(FEED_URL)
xml_data = response.content

# Converter XML para dicionário
feed_dict = xmltodict.parse(xml_data)

# Extrair os empregos
jobs = feed_dict.get("jobs", {}).get("job", [])

# Filtrar apenas as informações necessárias
job_list = []
for job in jobs:
    job_info = {
        "title": job.get("title", ""),
        "description": job.get("description", ""),
        "url": job.get("urlDeeplink", ""),
        "company": job.get("company", {}).get("name", ""),
        "location": job.get("locations", {}).get("location", {}).get("state", ""),
    }
    job_list.append(job_info)

# Dividir em arquivos de 50MB
PART_SIZE = 50 * 1024 * 1024  # 50MB
json_str = json.dumps(job_list, indent=2, ensure_ascii=False)
part_number = 1

while json_str:
    part = json_str[:PART_SIZE]
    json_str = json_str[PART_SIZE:]

    with open(f"{OUTPUT_DIR}/vagas{part_number}.json", "w", encoding="utf-8") as f:
        f.write(part)

    part_number += 1

print(f"Processamento concluído! {part_number-1} arquivos gerados.")
