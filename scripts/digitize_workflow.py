
import os
import argparse
import logging
from markitdown import MarkItDown

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/digitization.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Default to current directory's 07a Articles
DEFAULT_ARTICLES_DIR = os.path.join(os.getcwd(), "07a Articles")

def get_metadata(filename, folder_name):
    """Generate basic metadata from filename and folder."""
    # Try to parse title from filename if standardized
    # e.g. "07a.01_The_Order..."
    # Or fallback to folder name

    title = os.path.splitext(filename)[0].replace('_', ' ')

    # Try to extract ID from folder name "07a.01 - Title"
    article_id = ""
    if " - " in folder_name:
        article_id = folder_name.split(" - ")[0]

    return {
        "title": title,
        "article_id": article_id,
        "filename": filename,
        "status": "draft"
    }

def create_frontmatter(metadata):
    """Create YAML frontmatter string."""
    fm = "---\n"
    for key, value in metadata.items():
        fm += f"{key}: \"{value}\"\n"
    fm += "---\n\n"
    return fm

def process_file(pdf_path, dry_run=False, overwrite=False):
    """Extract text and save as Markdown."""
    try:
        markitdown = MarkItDown()

        md_filename = os.path.splitext(pdf_path)[0] + ".md"

        if os.path.exists(md_filename) and not overwrite and not dry_run:
            logging.info(f"Skipping {pdf_path}: {md_filename} already exists")
            print(f"Skipping {os.path.basename(pdf_path)} - MD exists")
            return

        logging.info(f"Processing {pdf_path}")
        print(f"Processing {os.path.basename(pdf_path)}...")

        if dry_run:
            print(f"  [Dry Run] Would extract content to {md_filename}")
            return

        result = markitdown.convert(pdf_path)
        content = result.text_content

        # Get metadata
        folder_name = os.path.basename(os.path.dirname(pdf_path))
        metadata = get_metadata(os.path.basename(pdf_path), folder_name)
        frontmatter = create_frontmatter(metadata)

        full_content = frontmatter + content

        with open(md_filename, 'w', encoding='utf-8') as f:
            f.write(full_content)

        logging.info(f"Successfully processed {pdf_path}")
        print(f"  Saved to {os.path.basename(md_filename)}")

    except Exception as e:
        logging.error(f"Error processing {pdf_path}: {e}")
        print(f"  Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Digitize PDF articles to Markdown")
    parser.add_argument("target_dir", nargs="?", default=DEFAULT_ARTICLES_DIR, help="Directory to process (default: 07a Articles)")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without writing files")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing .md files")
    args = parser.parse_args()

    if not os.path.exists(args.target_dir):
        print(f"Error: {args.target_dir} not found")
        return

    count = 0
    if os.path.isfile(args.target_dir):
        if args.target_dir.lower().endswith(".pdf"):
            process_file(args.target_dir, dry_run=args.dry_run, overwrite=args.overwrite)
            count = 1
    else:
        for root, dirs, files in os.walk(args.target_dir):
            for file in files:
                if file.lower().endswith(".pdf"):
                    process_file(os.path.join(root, file), dry_run=args.dry_run, overwrite=args.overwrite)
                    count += 1

    print(f"\nProcessed {count} files.")

if __name__ == "__main__":
    main()
