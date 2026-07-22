with open("/Users/lamar/Library/CloudStorage/GoogleDrive-demarquismoss@gmail.com/.shortcut-targets-by-id/1tMF8XwUebaTKFF1MkZH1ZGEvysAOQI4s/Revell/docs/tei/07a.02/transcription_tei.xml", "r", encoding="utf-8") as f:
    lines = f.readlines()

for idx in range(1270, 1310):
    if idx < len(lines):
        print(f"{idx+1}: {lines[idx]}", end="")
