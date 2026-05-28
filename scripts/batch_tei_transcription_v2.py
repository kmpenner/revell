
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

    env = os.environ.copy()
    env["OPENROUTER_API_KEY"] = api_key

    folders = [f for f in os.listdir(ARTICLES_DIR) if os.path.isdir(os.path.join(ARTICLES_DIR, f))]

    for folder in sorted(folders):
        folder_path = os.path.join(ARTICLES_DIR, folder)

        # Find PDFs
        pdfs = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")])
        if not pdfs:
            # logging.warning(f"No PDF found in {folder}. Skipping.")
            continue

        for i, pdf_file in enumerate(pdfs):
            # Check if transcription for THIS specific PDF (or part) exists
            if len(pdfs) == 1:
                output_name = "transcription_tei.xml"
            else:
                output_name = f"transcription_p{i+1}_tei.xml"

            output_path = os.path.join(folder_path, output_name)

            if os.path.exists(output_path):
                logging.info(f"Skipping {pdf_file} in {folder}: Transcription exists.")
                continue

            pdf_path = os.path.join(folder_path, pdf_file)
            logging.info(f"Processing {folder} / {pdf_file}...")

            cmd = [
                "python",
                SCRIPT_PATH,
                "--input", pdf_path,
                "--output", output_path
            ]

            try:
                result = subprocess.run(cmd, env=env, capture_output=True, text=True)
                if result.returncode == 0:
                    logging.info(f"Successfully transcribed {pdf_file}.")
                else:
                    logging.error(f"Failed to transcribe {pdf_file}: {result.stderr}")
            except Exception as e:
                logging.error(f"Error running transcription for {pdf_file}: {e}")

if __name__ == "__main__":
    main()
