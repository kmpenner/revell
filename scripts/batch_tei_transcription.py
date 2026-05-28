
import os
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

ROOT_DIR = r"g:\My Drive\Research\Revell"
ARTICLES_DIR = os.path.join(ROOT_DIR, "07a Articles")
SCRIPT_PATH = os.path.join(ROOT_DIR, "skills", "pdf_to_tei", "scripts", "pdf_to_tei.py")
KEY_PATH = os.path.join(ROOT_DIR, "metadata", "openrouter_api_key.txt")

def get_api_key():
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH, 'r') as f:
            return f.read().strip()
    return os.environ.get("OPENROUTER_API_KEY")

def main():
    api_key = get_api_key()
    if not api_key:
        logging.error("No API key found.")
        return

    # Set up environment for the subprocess
    env = os.environ.copy()
    env["OPENROUTER_API_KEY"] = api_key

    folders = [f for f in os.listdir(ARTICLES_DIR) if os.path.isdir(os.path.join(ARTICLES_DIR, f))]

    for folder in sorted(folders):
        folder_path = os.path.join(ARTICLES_DIR, folder)

        # Check if transcription already exists
        xml_files = [f for f in os.listdir(folder_path) if f.endswith(".xml")]
        # Match 'transcription.xml' or 'transcription_tei.xml' or 'transcription_enriched.xml'
        tei_exists = any("transcription" in f.lower() for f in xml_files)

        if tei_exists:
            logging.info(f"Skipping {folder}: TEI transcription already exists.")
            continue

        # Find PDF
        pdfs = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
        if not pdfs:
            logging.warning(f"No PDF found in {folder}. Skipping.")
            continue

        pdf_to_process = pdfs[0] # Just the first one for now
        output_name = "transcription_tei.xml"
        output_path = os.path.join(folder_path, output_name)
        pdf_path = os.path.join(folder_path, pdf_to_process)

        logging.info(f"Processing {folder} -> {pdf_to_process}...")

        cmd = [
            "python",
            SCRIPT_PATH,
            "--input", pdf_path,
            "--output", output_path
        ]

        try:
            # Run the transcription script
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            if result.returncode == 0:
                logging.info(f"Successfully transcribed {folder}.")
            else:
                logging.error(f"Failed to transcribe {folder}: {result.stderr}")
        except Exception as e:
            logging.error(f"Error running transcription for {folder}: {e}")

if __name__ == "__main__":
    main()
