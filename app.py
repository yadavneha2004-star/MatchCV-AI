import os
import re
import pandas as pd
import pdfplumber
from docx import Document
from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB limit

# Ensure extraction directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def clean_text(text):
    """Normalize text by removing special characters and extra whitespace."""
    if not text: return ""
    text = text.lower()
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return text.strip()

def extract_skills(text, skill_list):
    """Check for presence of specific skills in the text."""
    found_skills = []
    for skill in skill_list:
        skill = skill.strip()
        if not skill: continue
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text.lower()):
            found_skills.append(skill)
    return found_skills

def extract_text(filepath, filename):
    """Extract text from PDF, DOCX, or TXT formats."""
    ext = filename.rsplit('.', 1)[1].lower()
    try:
        if ext == 'pdf':
            with pdfplumber.open(filepath) as pdf:
                text = "\n".join(page.extract_text() or "" for page in pdf.pages)
            return text
        elif ext == 'docx':
            doc = Document(filepath)
            return "\n".join([para.text for para in doc.paragraphs])
        elif ext == 'txt':
            with open(filepath, 'r', encoding='utf-8') as f:
                return f.read()
        return ""
    except Exception as e:
        print(f"Error parsing {filename}: {e}")
        return ""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rank', methods=['POST'])
def rank():
    job_description = request.form.get('job_description', '')
    skills_input = request.form.get('skills', '')
    skill_list = [s.strip() for s in skills_input.split(',')] if skills_input else []
    
    files = request.files.getlist('resumes')
    
    if not files or not job_description:
        return jsonify({"error": "Missing files or job description"}), 400

    resumes_data = []
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            text = extract_text(filepath, filename)
            cleaned = clean_text(text)
            
            if cleaned:
                found_skills = extract_skills(text, skill_list)
                resumes_data.append({
                    "filename": filename,
                    "cleaned_text": cleaned,
                    "skills": found_skills
                })
            
            # Clean up file after processing
            os.remove(filepath)

    if not resumes_data:
        return jsonify({"error": "No valid text could be extracted from resumes"}), 400

    # TF-IDF Ranking
    texts = [clean_text(job_description)] + [r['cleaned_text'] for r in resumes_data]
    vectorizer = TfidfVectorizer(stop_words='english')
    vectors = vectorizer.fit_transform(texts)
    
    job_vector = vectors[0]
    resume_vectors = vectors[1:]
    
    scores = cosine_similarity(job_vector, resume_vectors).flatten() * 100
    
    results = []
    for i, r in enumerate(resumes_data):
        results.append({
            "name": r['filename'],
            "score": round(float(scores[i]), 2),
            "skills": ", ".join(r['skills']) if r['skills'] else "None"
        })

    # Sort by score
    results = sorted(results, key=lambda x: x['score'], reverse=True)
    
    # Add rank
    for idx, res in enumerate(results):
        res['rank'] = idx + 1

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True, port=int(os.environ.get('PORT', 5000)))
