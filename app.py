from flask import Flask, request, send_file
from flask_cors import CORS
import pypandoc
import os
import tempfile

# সার্ভার চালু হওয়ার সময় Pandoc না থাকলে এটি নিজে থেকেই ডাউনলোড করে নেবে (কোনো পারমিশন লাগবে না)
try:
    pypandoc.get_pandoc_version()
except OSError:
    pypandoc.download_pandoc()

app = Flask(__name__)
CORS(app)

@app.route('/convert', methods=['POST'])
def convert_to_word():
    data = request.json
    markdown_text = data.get('markdown', '')

    if not markdown_text:
        return {"error": "Text nai"}, 400

    fd, path = tempfile.mkstemp(suffix='.docx')
    try:
        pypandoc.convert_text(markdown_text, 'docx', format='markdown', outputfile=path)
        return send_file(path, as_attachment=True, download_name='Smart_Notes.docx')
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        os.close(fd)
        try:
            os.remove(path)
        except:
            pass

if __name__ == '__main__':
    app.run()
