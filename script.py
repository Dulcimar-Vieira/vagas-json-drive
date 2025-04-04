import os
import json

# Pasta onde estão os arquivos
json_folder = "json_parts"
merged_file = "merged.json"

# Lista para armazenar todos os dados
all_jobs = []

# Pegar e ordenar os arquivos JSON
json_files = sorted(
    [f for f in os.listdir(json_folder) if f.endswith(".json")],
    key=lambda x: int(x.split("_")[1].split(".")[0])
)

# Carregar cada arquivo e juntar os dados
for filename in json_files:
    file_path = os.path.join(json_folder, filename)
    with open(file_path, "r", encoding="utf-8") as f:
        jobs = json.load(f)
        all_jobs.extend(jobs)

# Salvar tudo em um único arquivo
with open(merged_file, "w", encoding="utf-8") as f:
    json.dump(all_jobs, f, ensure_ascii=False, indent=2)

print(f"Arquivo mesclado criado: {merged_file}")
