import requests

feed_url = "https://feeds.whatjobs.com/sinerj/sinerj_pt_BR.xml.gz"
response = requests.get(feed_url)

if response.status_code == 200:
    print("Download bem-sucedido! Tamanho do arquivo:", len(response.content), "bytes")
else:
    print("Erro ao baixar o feed:", response.status_code)
