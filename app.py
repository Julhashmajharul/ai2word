from flask import Flask, request, send_file
from flask_cors import CORS
import pypandoc
import os
import tempfile

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
        # এই লাইনটি আপনার ম্যাথকে আসল Word সমীকরণে রূপান্তর করবে
        pypandoc.convert_text(markdown_text, 'docx', format='markdown', outputfile=path)
        return send_file(path, as_attachment=True, download_name='Smart_Notes.docx')
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        os.close(fd)
        os.remove(path)

if __name__ == '__main__':
    app.run()
