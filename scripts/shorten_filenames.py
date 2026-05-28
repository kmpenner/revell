
import os

ARTICLES_DIR = r"g:\My Drive\Research\Revell\07a Articles"

def main():
    if not os.path.exists(ARTICLES_DIR):
        print("Articles directory not found.")
        return

    count = 0
    for folder_name in os.listdir(ARTICLES_DIR):
        folder_path = os.path.join(ARTICLES_DIR, folder_name)
        if not os.path.isdir(folder_path):
            continue

        # Extract article ID (e.g., "07a.01")
        if " - " in folder_name:
            article_id = folder_name.split(" - ")[0]
        else:
            # Fallback if no separator, assume first part is ID
            article_id = folder_name.split(" ")[0]

        files = os.listdir(folder_path)

        # Renaissance of simple names
        for file in files:
            file_lower = file.lower()
            ext = os.path.splitext(file)[1]

            # Skip files that don't look like our PDFs or MDs or XMLs (or are already short)
            if not (file_lower.endswith(".pdf") or file_lower.endswith(".md") or file_lower.endswith(".xml")):
                continue

            # If standard naming scheme detected (starts with ID)
            if file.startswith(article_id):

                # Determine new name
                # Keep "transcription" if it's there
                if "transcription" in file_lower:
                    # e.g., transcription_tei.xml -> transcription_tei.xml (leave as is?)
                    # Or maybe rename to 07a.01_transcription.xml
                    if file_lower == "transcription.xml" or file_lower == "transcription_tei.xml":
                        new_name = f"{article_id}_{file}"
                    elif file.startswith(article_id) and "transcription" in file_lower:
                        # e.g. 07a.01_transcription.xml
                        new_name = file # Keep it? Or shorten if it has title
                        pass
                    else:
                        new_name = file
                elif "_part" in file_lower:
                    # e.g. 07a.01_Very_Long_Title_part1.pdf -> 07a.01_part1.pdf
                    import re
                    match = re.search(r"(.*)(_part\d+)(.*)", file)
                    if match:
                        suffix = match.group(2) # _part1
                        new_name = f"{article_id}{suffix}{ext}"
                    else:
                         new_name = f"{article_id}{ext}" # Should not happen if _part check passes

                else:
                    # e.g. 07a.01_Very_Long_Title.pdf -> 07a.01.pdf
                    new_name = f"{article_id}{ext}"

                old_path = os.path.join(folder_path, file)
                new_path = os.path.join(folder_path, new_name)

                if old_path != new_path:
                    # Check collision
                    if os.path.exists(new_path):
                         print(f"Skipping {file} -> {new_name} (Standard name exists)")
                         continue

                    print(f"Renaming {file} -> {new_name}")
                    try:
                        os.rename(old_path, new_path)
                        count += 1
                    except Exception as e:
                        print(f"  Error: {e}")

    print(f"\nRenamed {count} files.")

if __name__ == "__main__":
    main()
