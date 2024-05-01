import os
import re
from PyPDF2 import PdfReader

class PDFLanguageExtractor:
    def __init__(self, language):
        self.language = language
        self.pdf_files = []
        self.find_language_pdfs()

    def find_language_pdfs(self):
        directory = 'downloaded_pdfs/'
        for filename in os.listdir(directory):
            if filename.endswith('.pdf') and self.language in filename:
                self.pdf_files.append(os.path.join(directory, filename))
        self.pdf_files.sort(key=lambda x: int(re.search(r'_([0-9]+)-[0-9]+\.pdf', x).group(1)))
        print(f"Found PDFs for {self.language}: {self.pdf_files}")

    def extract_sections(self, pdf_path):
        reader = PdfReader(pdf_path)
        toc_page = reader.pages[4]
        toc_text = toc_page.extract_text()
        sections = re.findall(r'(\d\.\d)\s+(.*?)\s+(\d+)', toc_text)
        print(f"Extracted sections from {pdf_path}: {sections}")
        return sections

    def fetch_section_text(self, level, section, page_num=None, sentence_num=None):
        if level - 1 < len(self.pdf_files):
            pdf_path = self.pdf_files[level - 1]
        else:
            return f"Level {level} PDF not found."

        print(f"Fetching from PDF: {pdf_path}")
        sections = self.extract_sections(pdf_path)
        start_page, end_page = None, None

        for i, sec in enumerate(sections):
            if sec[0] == str(section):
                start_page = int(sec[2]) + 4
                if i + 1 < len(sections):
                    end_page = int(sections[i + 1][2]) + 4
                else:
                    end_page = len(PdfReader(pdf_path).pages)
                break

        if start_page is None:
            return "Section not found."

        reader = PdfReader(pdf_path)
        text_output = []

        if page_num:
            target_page_num = start_page + page_num - 1
            if start_page <= target_page_num < end_page:
                page_text = reader.pages[target_page_num].extract_text()
                if sentence_num:
                    sentences = self.extract_sentences_by_number(page_text, sentence_num)
                    text_output.extend(sentences)
                else:
                    text_output.append(page_text)
            else:
                return "Page number out of section range."
        else:
            for i in range(start_page, end_page):
                page_text = reader.pages[i].extract_text()
                if sentence_num:
                    sentences = self.extract_sentences_by_number(page_text, sentence_num)
                    text_output.extend(sentences)
                else:
                    text_output.append(page_text)

        return "\n".join(text_output)

    def extract_sentences_by_number(self, text, sentence_num=None):
        if sentence_num is not None:
            if isinstance(sentence_num, int):
                pattern = re.compile(rf'^0*{sentence_num}\s+(.*)', re.MULTILINE)
            elif isinstance(sentence_num, range):
                pattern = re.compile(rf'^0*({str(sentence_num.start)}|{str(sentence_num.stop)})\s+(.*)', re.MULTILINE)
            matches = pattern.findall(text)
            return [match[1] for match in matches]
        else:
            # General pattern to extract all sentences
            pattern = re.compile(r'^0*(\d+)\s+(.*)', re.MULTILINE)
            matches = pattern.findall(text)
            return [(match[0], match[1]) for match in matches]

# Example usage
language_extractor = PDFLanguageExtractor('Japanese')
level = 2
section = '2.1'
sentence_num = None  # Fetching the first sentence
# sentence_num = 1  # Fetching the first sentence
# sentence_num = range(1, 3)  # Fetching sentences 1 to 2
section_text = language_extractor.fetch_section_text(level, section, page_num=None, sentence_num=sentence_num)
print(section_text)

