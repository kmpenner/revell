---
name: pdf_to_tei
description: Transcribes PDF documents into TEI P5 XML format using a vision model (Gemini 3 Flash via OpenRouter).
---

# PDF to TEI Transcription Skill

This skill allows you to transcribe PDF documents (scans of articles, etc.) into high-quality TEI P5 XML. It uses a vision model to accurately capture text, including complex layouts and special characters common in scholarly articles.

## How to use

1.  **Configure API Key**: Ensure you have an OpenRouter API key. Set it as an environment variable:
    ```bash
    $env:OPENROUTER_API_KEY = "your-key-here"
    ```
2.  **Run the script**:
    ```bash
    python skills/pdf_to_tei/scripts/pdf_to_tei.py --input "path/to/document.pdf" --output "path/to/output.xml"
    ```

## Scripts

### transcribe_pdf.py
The main transcription engine. It performs the following steps:
1.  Converts PDF pages to high-resolution images.
2.  Sends each image to Gemini 3 Flash via OpenRouter with a specialized prompt for TEI P5 XML.
3.  Assembles the resulting XML fragments into a valid TEI P5 document.

## Resources
- [TEI P5 Guidelines](https://tei-c.org/guidelines/p5/)
- [OpenRouter API Documentation](https://openrouter.ai/docs)
