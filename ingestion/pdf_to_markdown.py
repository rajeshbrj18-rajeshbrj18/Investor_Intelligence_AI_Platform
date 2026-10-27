from pathlib import Path
import pymupdf4llm
import sys
sys.path.append(str(Path(__file__).resolve().parent.parent))

class PDFToMarkdownConverter:
    def convert_to_pdf(self, pdf_path: str, output_dir: str)-> str:
        
        pdf_file = Path(pdf_path)
        
        if not pdf_file.exists():
            raise FileNotFoundError(f"PDF file not found in {pdf_path}")
        
        output_path = Path(output_dir)
        
        output_path.mkdir(parents=True, exist_ok=True)

        markdown_content = pymupdf4llm.to_markdown(str(pdf_file))
        
        markdown_file = output_path/f"{pdf_file.stem}.md"
        
        markdown_file.write_text(
            markdown_content,
            encoding="utf-8"
        )

        return str(markdown_file)


    def convert_directory(self, input_dir: str, output_dir: str)-> list[str]:

        input_path = Path(input_dir)

        markdown_files = []

        for pdf_file in input_path.glob("*.pdf"):
            markdown_file = self.convert_to_pdf(
                pdf_file, 
                output_dir=output_dir
            )
            
            markdown_files.append(markdown_file)

        return markdown_files

if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]

    input_dir = repo_root/"data"/"raw_pdfs"
    output_dir = repo_root/"data"/"markdown"

    converter = PDFToMarkdownConverter()

    markdown_files = converter.convert_directory(str(input_dir), str(output_dir))

    print(f"successfully converted {len(markdown_files)} PDFs")

    for markdown_file in markdown_files:
        print(f"  - {markdown_file}")



