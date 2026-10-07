import os
import glob
import subprocess
import shutil

ROOT_DIR = "07a Articles"
MD_TO_TEI_SCRIPT = "scripts/md_to_tei.py"

def concatenate_and_convert(folder_path, md_files, output_xml):
    print(f"Concatenating {len(md_files)} files in {folder_path}...")
    temp_md = os.path.join(folder_path, "temp_combined.md")
    
    first = True
    with open(temp_md, 'w', encoding='utf-8') as outfile:
        for md_file in sorted(md_files):
            with open(md_file, 'r', encoding='utf-8') as infile:
                content = infile.read()
                if first:
                    outfile.write(content)
                    first = False
                else:
                    # Strip frontmatter from subsequent parts
                    if content.startswith("---"):
                        parts = content.split("---", 2)
                        if len(parts) >= 3:
                            outfile.write(parts[2])
                        else:
                            outfile.write(content)
                    else:
                        outfile.write(content)
            outfile.write("\n\n\x0c") # Form feed between parts to mark page breaks
            
    # Run conversion script
    cmd = ["python3", MD_TO_TEI_SCRIPT, temp_md, output_xml]
    subprocess.run(cmd)
    
    # Remove temp file
    if os.path.exists(temp_md):
        os.remove(temp_md)

def process_all():
    # List of directories we need to convert
    dirs_to_process = [
        ("07a.39 - Articles Emendations Scribes", ["Albanese.md"]),
        ("07a.42 - Development Segol Open", ["07a.42.md"]),
        ("07a.43 - Conditional Particles Biblical", ["07a.43_trimmed.md"]),
        ("07a.44 - Concord Collectives Biblical", ["07a.44_p1.md", "07a.44_p2.md"]),
        ("07a.45 - Concord Compound Subjects", ["07a.45.md"]),
        ("07a.46 - Gentilics Geography Studies", ["07a.46.md"]),
        ("07a.47 - Reading Tradition Basis", ["07a.47.md"]),
        ("07a.48 - Ny Nky Redundancy", ["07a.48_trimmed.md"]),
        ("07a.49 - Interpretative Significance Masoretic", ["07a.49_p1.md", "07a.49_p2.md", "07a.49_p3.md"]),
        ("07a.50 - Leningrad Codex Representative", ["07a.50.md"]),
        ("07a.51 - Repetition Introductions Speech", ["07a.51.md"]),
        ("07a.52 - Thematic Continuity Conditioning", ["07a.52.md"]),
        ("07a.53 - Midian and Ishmael", ["07a.53.md"]),
    ]
    
    for dir_name, md_filenames in dirs_to_process:
        folder_path = os.path.join(ROOT_DIR, dir_name)
        if not os.path.exists(folder_path):
            print(f"Directory not found: {folder_path}. Skipping.")
            continue
            
        md_paths = [os.path.join(folder_path, name) for name in md_filenames if os.path.exists(os.path.join(folder_path, name))]
        if not md_paths:
            print(f"No source markdown files found in {folder_path}. Skipping.")
            continue
            
        output_xml = os.path.join(folder_path, "transcription_tei.xml")
        
        if len(md_paths) == 1:
            cmd = ["python3", MD_TO_TEI_SCRIPT, md_paths[0], output_xml]
            subprocess.run(cmd)
        else:
            concatenate_and_convert(folder_path, md_paths, output_xml)

if __name__ == "__main__":
    process_all()
