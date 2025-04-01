import requests
import gzip
import shutil
import json
import xmltodict
import os
from github import Github

import os
from github import Github

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")  # Obtendo o token de ambiente
g = Github(GITHUB_TOKEN)

# Configurações
FEED_URL = "https://feeds.whatjobs.com/sinerj/sinerj_pt_BR.xml.gz"
LOCAL_GZ_FILE = "feed.xml.gz"
LOCAL_XML_FILE = "feed.xml"
LOCAL_JSON_FILE = "feed.json"
COMPRESSED_JSON_FILE = "feed.json.gz"
GITHUB_REPO = "Dulcimar-Vieira/vagas-json-drive"
GITHUB_FILE_PATH = "feed.json.gz"
CHUNK_SIZE = 50 * 1024 * 1024  # 50MB por parte

def download_feed():
    print("Baixando feed...")
    response = requests.get(FEED_URL, stream=True)
    if response.status_code == 200:
        with open(LOCAL_GZ_FILE, 'wb') as f:
            shutil.copyfileobj(response.raw, f)
        print("Download concluído.")
    else:
        print("Erro ao baixar o feed.")
        exit(1)

def extract_gz():
    print("Extraindo arquivo XML...")
    with gzip.open(LOCAL_GZ_FILE, 'rb') as f_in, open(LOCAL_XML_FILE, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print("Extração concluída.")

def convert_to_json():
    print("Convertendo XML para JSON...")
    with open(LOCAL_XML_FILE, "r", encoding="utf-8") as xml_file:
        data_dict = xmltodict.parse(xml_file.read())
    
    with open(LOCAL_JSON_FILE, "w", encoding="utf-8") as json_file:
        json.dump(data_dict, json_file, indent=4, ensure_ascii=False)
    print("Conversão concluída.")

def compress_json():
    print("Comprimindo JSON...")
    with open(LOCAL_JSON_FILE, 'rb') as f_in, gzip.open(COMPRESSED_JSON_FILE, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
    print("Compressão concluída.")

def upload_to_github():
    print("Fazendo upload para o GitHub...")
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(GITHUB_REPO)
    
    with open(COMPRESSED_JSON_FILE, "rb") as f:
        content = f.read()
    
    try:
        contents = repo.get_contents(GITHUB_FILE_PATH)
        repo.update_file(contents.path, "Atualizando feed", content, contents.sha)
    except:
        repo.create_file(GITHUB_FILE_PATH, "Enviando feed", content)
    
    file_link = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/{GITHUB_FILE_PATH}"
    print(f"Arquivo enviado! Acesse: {file_link}")

def main():
    download_feed()
    extract_gz()
    convert_to_json()
    compress_json()
    upload_to_github()
    print("Processo concluído!")

if __name__ == "__main__":
    main()
