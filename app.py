import tornado.ioloop
import tornado.web
import json



def katakana_to_hiragana(phonetic):
    """Convert Katakana in the phonetic to Hiragana."""
    return ''.join(chr(ord(char) - 0x60) if 'ァ' <= char <= 'ヴ' else char for char in phonetic)

def is_hiragana(s):
    """Check if the string contains only Hiragana characters."""
    return all('ぁ' <= char <= 'ん' for char in s)

def optimize_japanese(json_data):
    """Optimize Japanese phonetics in the JSON data."""
    ja_data = json_data.get("ja", {}).get("pairs", [])
    for item in ja_data:
        # Convert Katakana to Hiragana in phonetics
        item['phonetic'] = katakana_to_hiragana(item['phonetic'])
        # Remove phonetic if part is only Hiragana and matches phonetic
        if is_hiragana(item['part']) and item['part'] == item['phonetic']:
            item['phonetic'] = ""  # or `del item['phonetic']` to remove the key


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", translations=translations)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ], debug=True, template_path="templates")

if __name__ == "__main__":

        # Load translations from the JSON file
    with open("translations.json") as f:
        translations = json.load(f)

    # Run optimization on the sample data
    optimize_japanese(translations)

    app = make_app()
    app.listen(7788)
    print("Server started at http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
