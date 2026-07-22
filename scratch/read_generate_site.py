with open("/Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/scripts/generate_site.py", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(362, 615):
    print(f"{idx+1}: {lines[idx]}", end="")
