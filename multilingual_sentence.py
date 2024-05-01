import csv
from openai_request import OpenAIRequestBase  # Ensure this is correctly imported

class JapaneseSentenceProcessor(OpenAIRequestBase):
    def __init__(self, csv_file_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.csv_file_path = csv_file_path

    def process_csv(self):
        with open(self.csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.process_row(row)
                break

    def process_row(self, row):
        content = row['Content']
        # prompt = f"Given this Japanese text: {content}, could you write a daily used Japanese sentence (clean or rewrite), English, Arabic, Chinese, and Cantonese? The output should be in JSON format."
        prompt = (
            "Given this Japanese text: " + japanese_text + "\n\n"
            "Could you write a daily used Japanese sentence (clean or rewrite), English, Arabic, Chinese, and Cantonese? "
            "The output should be in JSON format with sentences and phonetic pairs for each language.\n\n"
            "**JSON Format**:\n"
            "```json\n"
            "{\n"
            "  \"japanese\": {\n"
            "    \"sentence\": \"\",\n"
            "    \"phonetics_pairs\": [\n"
            "      {\n"
            "        \"part\": \"\",\n"
            "        \"furigana\": \"\"\n"
            "      }\n"
            "    ]\n"
            "  },\n"
            "  \"english\": {\n"
            "    \"sentence\": \"\",\n"
            "    \"phonetics_pairs\": [\n"
            "      {\n"
            "        \"part\": \"\",\n"
            "        \"phonetics\": \"\"\n"
            "      }\n"
            "    ]\n"
            "  },\n"
            "  \"arabic\": {\n"
            "    \"sentence\": \"\",\n"
            "    \"phonetics_pairs\": [\n"
            "      {\n"
            "        \"part\": \"\",\n"
            "        \"phonetics\": \"\"\n"
            "      }\n"
            "    ]\n"
            "  },\n"
            "  \"chinese\": {\n"
            "    \"sentence\": \"\",\n"
            "    \"phonetics_pairs\": [\n"
            "      {\n"
            "        \"part\": \"\",\n"
            "        \"pinyin\": \"\"\n"
            "      }\n"
            "    ]\n"
            "  },\n"
            "  \"cantonese\": {\n"
            "    \"sentence\": \"\",\n"
            "    \"phonetics_pairs\": [\n"
            "      {\n"
            "        \"part\": \"\",\n"
            "        \"jyutping\": \"\"\n"
            "      }\n"
            "    ]\n"
            "  }\n"
            "}\n"
            "```"
        )
        system_content = "You are a multilingual translator capable of understanding and rewriting sentences in Japanese, English, Arabic, Chinese, and Cantonese with phonetic pairs."
        
        response = self.send_request_with_retry(prompt, system_content=system_content)
        print(response)  # Or handle the response as needed

# Assuming your OpenAIRequestBase class is defined in openai_request_base.py
if __name__ == "__main__":
    csv_file_path = 'japanese_language_data.csv'  # Update this path to your CSV file
    processor = JapaneseSentenceProcessor(csv_file_path, use_cache=True)
    processor.process_csv()
