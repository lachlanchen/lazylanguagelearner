import os
import re
from PyPDF2 import PdfReader
import csv

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

    def extract_sections(self, pdf_path):
        reader = PdfReader(pdf_path)
        toc_page = reader.pages[4]  # Assuming ToC is on page 5
        toc_text = toc_page.extract_text()
        sections = re.findall(r'(\d\.\d)\s+(.*?)\s+(\d+)', toc_text)
        return sections

    # def extract_text_by_sentence(self, text):
    #     pattern = re.compile(r'(\d{2})\s+(.*?)\s+(?=\d{2}\s+|$)', re.DOTALL)
    #     matches = pattern.findall(text)
    #     # Replace newlines within the captured text with \\n to keep each sentence's content correctly formatted
    #     return [(match[0], match[1].replace('\n', '\\\\n')) for match in matches]

    def extract_text_by_sentence(self, text):
        pattern = re.compile(r'(\d{2})\s+(.*?)\s+(?=\d{2}\s+|$)', re.DOTALL)
        matches = pattern.findall(text)
        # Replace newlines within the captured text with \\n and filter out sentences with three or more consecutive periods
        filtered_matches = []
        for match in matches:
            sentence_no, sentence_content = match
            sentence_content = sentence_content.replace('\n', '\\\\n').strip()
            # Check for three or more consecutive periods
            if '...' not in sentence_content:
                filtered_matches.append((sentence_no, sentence_content))
        return filtered_matches


    def process_and_save(self, filename='language_data.csv'):
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Level', 'Unit', 'Section', 'Sentence No.', 'Content'])

            for pdf_file in self.pdf_files:
                level = re.search(r'_([0-9]+)-[0-9]+\.pdf', pdf_file).group(1)
                sections = self.extract_sections(pdf_file)
                
                for section_info in sections:
                    section_number, _, start_page_str = section_info
                    unit, section = section_number.split('.')
                    start_page = int(start_page_str) + 4  # Adjust based on actual content start

                    try:
                        reader = PdfReader(pdf_file)
                        for i in range(start_page - 1, len(reader.pages)):
                            page_text = reader.pages[i].extract_text() or ""
                            sentences = self.extract_text_by_sentence(page_text)
                            for sentence_no, sentence_content in sentences:
                                # Ensure \n is replaced with \\n in the sentence content
                                formatted_sentence_content = sentence_content.replace('\n', '\\\\n').strip()
                                writer.writerow([level, unit, section, sentence_no, formatted_sentence_content])
                    except Exception as e:
                        print(f"Error processing {pdf_file}, section {section_number}: {e}")

# Example usage
if __name__ == "__main__":
    extractor = PDFLanguageExtractor('Japanese')
    extractor.process_and_save('japanese_language_data.csv')
