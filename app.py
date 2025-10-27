import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import PyPDF2
import docx
from typing import List, Dict

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['ALLOWED_EXTENSIONS'] = {'pdf', 'txt', 'docx'}

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Simple in-memory database for disaster plans
disaster_plans_db = []


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']


def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    return text


def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text
    except Exception as e:
        print(f"Error reading DOCX: {e}")
        return ""


def extract_text_from_txt(file_path):
    """Extract text from TXT file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading TXT: {e}")
        return ""


def extract_text_from_file(file_path):
    """Extract text from various file formats"""
    extension = file_path.rsplit('.', 1)[1].lower()
    
    if extension == 'pdf':
        return extract_text_from_pdf(file_path)
    elif extension == 'docx':
        return extract_text_from_docx(file_path)
    elif extension == 'txt':
        return extract_text_from_txt(file_path)
    else:
        return ""


def extract_best_practices(text, disaster_type):
    """Extract best practices from disaster plan text for specific disaster type
    
    This is a simple keyword-based extraction. In production, you'd use NLP/AI.
    """
    disaster_type = disaster_type.lower()
    text_lower = text.lower()
    
    practices = []
    
    # Split text into sentences
    sentences = text.replace('\n', ' ').split('.')
    
    # Keywords for different disaster types
    keywords = {
        'fire': ['fire', 'smoke', 'evacuation', 'fire drill', 'fire extinguisher', 'sprinkler', 'flame', 'burning'],
        'flood': ['flood', 'water', 'drainage', 'sandbag', 'evacuation', 'water level', 'flood plain', 'inundation'],
        'hurricane': ['hurricane', 'storm', 'wind', 'evacuation', 'shelter', 'emergency supplies', 'tropical storm', 'cyclone'],
        'earthquake': ['earthquake', 'seismic', 'structure', 'drop cover hold', 'building safety', 'aftershock'],
        'tornado': ['tornado', 'shelter', 'basement', 'warning', 'funnel cloud', 'severe weather'],
    }
    
    # Action keywords that indicate best practices
    action_keywords = ['should', 'must', 'ensure', 'implement', 'establish', 'maintain', 
                      'procedure', 'protocol', 'recommendation', 'guideline', 'practice',
                      'plan', 'prepare', 'response', 'evacuate', 'shelter']
    
    disaster_keywords = keywords.get(disaster_type, [])
    
    for sentence in sentences:
        sentence_lower = sentence.lower().strip()
        
        # Check if sentence contains disaster-specific keywords and action keywords
        has_disaster_keyword = any(keyword in sentence_lower for keyword in disaster_keywords)
        has_action_keyword = any(keyword in sentence_lower for keyword in action_keywords)
        
        if has_disaster_keyword and has_action_keyword and len(sentence.strip()) > 20:
            practices.append(sentence.strip())
    
    # Remove duplicates while preserving order
    seen = set()
    unique_practices = []
    for practice in practices:
        if practice.lower() not in seen:
            seen.add(practice.lower())
            unique_practices.append(practice)
    
    return unique_practices[:10]  # Return top 10 practices


@app.route('/')
def index():
    """Render main page"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    government_name = request.form.get('government_name', 'Unknown')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Add timestamp to avoid name conflicts
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        file.save(file_path)
        
        # Extract text from file
        text = extract_text_from_file(file_path)
        
        # Store in database
        plan_entry = {
            'id': len(disaster_plans_db) + 1,
            'filename': filename,
            'original_filename': file.filename,
            'government_name': government_name,
            'upload_date': timestamp,
            'file_path': file_path,
            'text': text,
            'text_length': len(text)
        }
        
        disaster_plans_db.append(plan_entry)
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully',
            'plan_id': plan_entry['id'],
            'text_length': len(text)
        }), 200
    
    return jsonify({'error': 'Invalid file type. Allowed: PDF, TXT, DOCX'}), 400


@app.route('/api/plans', methods=['GET'])
def get_plans():
    """Get list of all uploaded disaster plans"""
    plans_summary = [
        {
            'id': plan['id'],
            'government_name': plan['government_name'],
            'original_filename': plan['original_filename'],
            'upload_date': plan['upload_date'],
            'text_length': plan['text_length']
        }
        for plan in disaster_plans_db
    ]
    
    return jsonify({'plans': plans_summary}), 200


@app.route('/api/best-practices/<disaster_type>', methods=['GET'])
def get_best_practices(disaster_type):
    """Get best practices for a specific disaster type from all uploaded plans"""
    all_practices = []
    
    for plan in disaster_plans_db:
        practices = extract_best_practices(plan['text'], disaster_type)
        
        for practice in practices:
            all_practices.append({
                'practice': practice,
                'source': plan['government_name'],
                'filename': plan['original_filename'],
                'plan_id': plan['id']
            })
    
    return jsonify({
        'disaster_type': disaster_type,
        'practices': all_practices,
        'total_count': len(all_practices)
    }), 200


@app.route('/api/search', methods=['POST'])
def search_practices():
    """Search for best practices based on disaster type and optional keyword"""
    data = request.get_json()
    disaster_type = data.get('disaster_type', '').lower()
    keyword = data.get('keyword', '').lower()
    
    if not disaster_type:
        return jsonify({'error': 'Disaster type is required'}), 400
    
    all_practices = []
    
    for plan in disaster_plans_db:
        practices = extract_best_practices(plan['text'], disaster_type)
        
        for practice in practices:
            # Filter by keyword if provided
            if keyword and keyword not in practice.lower():
                continue
                
            all_practices.append({
                'practice': practice,
                'source': plan['government_name'],
                'filename': plan['original_filename'],
                'plan_id': plan['id']
            })
    
    return jsonify({
        'disaster_type': disaster_type,
        'keyword': keyword,
        'practices': all_practices,
        'total_count': len(all_practices)
    }), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
