from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
import io
import base64

app = Flask(__name__)

@app.route('/extract-pdf', methods=['POST'])
def extract_pdf():
    try:
        # Get base64 PDF from request
        data = request.get_json()
        pdf_base64 = data.get('pdf_base64')
        
        if not pdf_base64:
            return jsonify({'error': 'No PDF provided'}), 400
        
        # Decode base64 to bytes
        pdf_bytes = base64.b64decode(pdf_base64)
        
        # Read PDF
        pdf_file = io.BytesIO(pdf_bytes)
        reader = PdfReader(pdf_file)
        
        # Extract text from all pages
        text = ''
        for page in reader.pages:
            text += page.extract_text() + '\n\n'
        
        return jsonify({
            'success': True,
            'text': text.strip(),
            'page_count': len(reader.pages)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Fichier: `requirements.txt`**
```
Flask==3.0.0
PyPDF2==3.0.1
gunicorn==21.2.0
```

**Fichier: `Procfile`** (pour Heroku/Render)
```
web: gunicorn app:app
