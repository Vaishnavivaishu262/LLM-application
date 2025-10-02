# Problem Statement:
# Preprocess unstructured text data for LLM applications: clean, normalize, chunk, and save output.

import re
from typing import List
from flask import Flask, request, render_template_string, send_file
import io

# Sample unstructured text (can be replaced with your own data)
raw_text = """
Deep learning is revolutionizing AI. However, unstructured data (text, images, audio) requires preprocessing before LLMs can use it effectively! 

Preprocessing steps include cleaning, normalization, and chunking. This enables better context management and retrieval for downstream tasks.

Let's see how to do this in Python.
"""

def clean_text(text: str) -> str:
    """Remove special characters, extra spaces, and lowercase the text."""
    text = re.sub(r'[^\w\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text)      # Remove extra spaces
    return text.strip().lower()

def chunk_text(text: str, chunk_size: int = 50) -> List[str]:
    """Split text into chunks of specified size (words)."""
    words = text.split()
    return [' '.join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Clean and chunk the text
tidy_text = clean_text(raw_text)
chunks = chunk_text(tidy_text, chunk_size=10)

# Save processed chunks to a file
with open('processed_chunks.txt', 'w', encoding='utf-8') as f:
    for i, chunk in enumerate(chunks):
        f.write(f"Chunk {i+1}: {chunk}\n")

# Show results
print("Processed Chunks:")
for i, chunk in enumerate(chunks):
    print(f"Chunk {i+1}: {chunk}")

app = Flask(__name__)

HTML_FORM = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Text Preprocessing App</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="bg-light">
<div class="container py-4">
  <h1 class="mb-4 text-primary">Text Preprocessing App</h1>
  <form method="post" class="mb-3">
    <div class="mb-3">
      <label for="text" class="form-label">Paste your text below:</label>
      <textarea name="text" id="text" rows="8" class="form-control">{{ original_text }}</textarea>
    </div>
    <div class="mb-3">
      <label for="chunk_size" class="form-label">Chunk Size (words):</label>
      <input type="number" name="chunk_size" id="chunk_size" value="{{ chunk_size }}" min="1" max="100" class="form-control" style="width:120px;">
    </div>
    <button type="submit" class="btn btn-success">Preprocess</button>
    <a href="/" class="btn btn-secondary ms-2">Reset</a>
  </form>
  {% if chunks %}
    <div class="alert alert-info">
      <strong>Word Count:</strong> {{ word_count }}<br>
      <strong>Chunk Count:</strong> {{ chunk_count }}
    </div>
    <h3 class="mt-4">Processed Chunks:</h3>
    <table class="table table-bordered table-striped">
      <thead class="table-primary"><tr><th>Chunk #</th><th>Text</th></tr></thead>
      <tbody>
        {% for chunk in chunks %}
          <tr><td>{{ loop.index }}</td><td>{{ chunk }}</td></tr>
        {% endfor %}
      </tbody>
    </table>
    <form method="post" action="/download">
      <input type="hidden" name="text" value="{{ original_text }}">
      <input type="hidden" name="chunk_size" value="{{ chunk_size }}">
      <button type="submit" class="btn btn-primary">Download Processed Chunks</button>
    </form>
  {% endif %}
</div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    chunks = None
    original_text = ''
    chunk_size = 10
    word_count = 0
    chunk_count = 0
    if request.method == 'POST':
        original_text = request.form.get('text', '')
        try:
            chunk_size = int(request.form.get('chunk_size', 10))
            if chunk_size < 1:
                chunk_size = 10
        except ValueError:
            chunk_size = 10
        tidy_text = clean_text(original_text)
        chunks = chunk_text(tidy_text, chunk_size=chunk_size)
        word_count = len(tidy_text.split())
        chunk_count = len(chunks)
    return render_template_string(HTML_FORM, chunks=chunks, original_text=original_text, chunk_size=chunk_size, word_count=word_count, chunk_count=chunk_count)

@app.route('/download', methods=['POST'])
def download():
    original_text = request.form['text']
    chunk_size = int(request.form.get('chunk_size', 10))
    tidy_text = clean_text(original_text)
    chunks = chunk_text(tidy_text, chunk_size=chunk_size)
    output = io.StringIO()
    for i, chunk in enumerate(chunks):
        output.write(f"Chunk {i+1}: {chunk}\n")
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/plain', as_attachment=True, download_name='processed_chunks.txt')

if __name__ == '__main__':
    app.run(debug=True)

# Deployment Instructions:
# 1. Install Flask: pip install flask
# 2. Run this script: python Untitled-1.py
# 3. Open http://127.0.0.1:5000/ in your browser.
# 4. Paste text, preprocess, and download results.
