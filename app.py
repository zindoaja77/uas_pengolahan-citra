from flask import Flask, render_template, request, jsonify, send_file
import os
import base64
from datetime import datetime
from PIL import Image
import io
import json

app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['SECRET_KEY'] = 'biker-ocr-flask-2024'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB

# Buat folder uploads jika belum ada
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/')
def home():
    """Halaman utama - render HTML langsung"""
    # Baca file index.html
    try:
        with open('templates/index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        return html_content
    except:
        # Fallback jika file tidak ditemukan
        return '''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Biker OCR</title>
            <style>
                body { font-family: Arial; padding: 50px; text-align: center; }
                .error { color: red; font-size: 24px; }
            </style>
        </head>
        <body>
            <div class="error">Error: File index.html tidak ditemukan!</div>
            <p>Pastikan file index.html ada di folder templates/</p>
        </body>
        </html>
        '''

@app.route('/api/upload', methods=['POST'])
def upload_image():
    """API untuk upload gambar ke server"""
    try:
        data = request.get_json()
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'No image data provided'
            }), 400
        
        # Decode base64 image
        image_data = data['image']
        if ',' in image_data:
            image_data = image_data.split(',')[1]
        
        image_bytes = base64.b64decode(image_data)
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
        filename = f"biker_{timestamp}.jpg"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save image
        with open(filepath, 'wb') as f:
            f.write(image_bytes)
        
        # Optimize image
        try:
            img = Image.open(filepath)
            if img.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            img.save(filepath, 'JPEG', quality=85)
            img_size = os.path.getsize(filepath)
        except Exception as e:
            print(f"Image optimization error: {e}")
            img_size = os.path.getsize(filepath)
        
        return jsonify({
            'success': True,
            'message': 'Image uploaded successfully',
            'filename': filename,
            'size': img_size,
            'url': f'/uploads/{filename}'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/process', methods=['POST'])
def process_ocr():
    """API untuk proses OCR (simulasi)"""
    try:
        data = request.get_json()
        language = data.get('language', 'eng')
        mode = data.get('mode', 'balanced')
        
        # Simulasi hasil OCR
        sample_text = f"""🚀 BIKER OCR - FLASK SERVER RESULT 🚀
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

============================================
📊 OCR PROCESSING COMPLETE
============================================

🔧 CONFIGURATION:
• Language: {language.upper()}
• Mode: {mode.upper()}
• Server: Flask Localhost
• Status: SUCCESS

📝 SAMPLE EXTRACTED TEXT:
-------------------------
MOTORCYCLE REGISTRATION
PLATE: B 5678 XYZ
BRAND: YAMAHA R15 V3
YEAR: 2022
COLOR: BLUE

ENGINE NUMBER: YH3R15V3456789
CHASSIS NUMBER: MAJYR15V3123456
OWNER: ANDI PRASETYA

ADDRESS:
JL. MENTENG RAYA NO. 45
JAKARTA PUSAT 10310

INSURANCE:
• Provider: ASURANSI JIWA
• Policy: MC-2023-7890
• Valid Until: 2024-12-31

MAINTENANCE HISTORY:
1. First Service: 1,000 km (2022-05-10)
2. Regular Service: 5,000 km (2022-11-15)
3. Major Service: 10,000 km (2023-05-20)

============================================
📈 STATISTICS:
• Characters: 625
• Words: 98
• Lines: 32
• Confidence: 96.2%
• Processing Time: 0.8s
============================================

💡 NOTE:
This is a demo result from Flask server.
For real OCR, install Tesseract OCR.
"""

        return jsonify({
            'success': True,
            'text': sample_text,
            'confidence': 96.2,
            'stats': {
                'characters': 625,
                'words': 98,
                'lines': 32,
                'processing_time': '0.8s'
            },
            'language': language,
            'timestamp': datetime.now().isoformat(),
            'server': 'Flask Localhost'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/translate', methods=['POST'])
def translate_text():
    """API untuk translate teks"""
    try:
        data = request.get_json()
        text = data.get('text', '')
        source = data.get('from', 'auto')
        target = data.get('to', 'id')
        
        # Simulasi terjemahan
        translations = {
            'id': f"""🇮🇩 HASIL TERJEMAHAN (INDONESIA):
{text}

📅 Tanggal: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔤 Bahasa Sumber: {source}
🎯 Bahasa Target: {target}

💬 Catatan:
Ini adalah hasil terjemahan simulasi dari server Flask.
Untuk terjemahan real-time, gunakan API seperti Google Translate.""",
            
            'en': f"""🇺🇸 TRANSLATION RESULT (ENGLISH):
{text}

📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔤 Source Language: {source}
🎯 Target Language: {target}

💬 Note:
This is a simulated translation from Flask server.
For real-time translation, use API like Google Translate.""",
            
            'ja': f"""🇯🇵 翻訳結果 (日本語):
{text}

📅 日付: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
🔤 ソース言語: {source}
🎯 ターゲット言語: {target}

💬 注記:
これはFlaskサーバーからのシミュレーション翻訳です。
リアルタイム翻訳にはGoogle Translate APIなどを使用してください。"""
        }
        
        translated = translations.get(target, f"Translation to {target}:\n\n{text}")
        
        return jsonify({
            'success': True,
            'translated': translated,
            'original': text,
            'from': source,
            'to': target,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/download', methods=['POST'])
def download_text():
    """API untuk download hasil OCR"""
    try:
        data = request.get_json()
        text = data.get('text', 'No text available')
        filename = data.get('filename', f'biker_ocr_{datetime.now().strftime("%Y%m%d_%H%M%S")}.txt')
        
        # Create in-memory text file
        from io import BytesIO
        bio = BytesIO()
        bio.write(text.encode('utf-8'))
        bio.seek(0)
        
        return send_file(
            bio,
            as_attachment=True,
            download_name=filename,
            mimetype='text/plain'
        )
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'Biker OCR Flask API',
        'version': '2.0.0',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'GET /': 'Home page',
            'POST /api/upload': 'Upload image',
            'POST /api/process': 'Process OCR',
            'POST /api/translate': 'Translate text',
            'POST /api/download': 'Download text',
            'GET /api/health': 'Health check'
        }
    })

@app.route('/uploads/<filename>')
def serve_uploaded_file(filename):
    """Serve uploaded files"""
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            mimetype='image/jpeg'
        )
    except:
        return jsonify({'error': 'File not found'}), 404

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

@app.errorhandler(413)
def too_large(error):
    return jsonify({'success': False, 'error': 'File too large. Maximum size is 16MB'}), 413

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏍️  BIKER OCR FLASK SERVER")
    print("="*60)
    print(f"📂 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"🌐 Server URL: http://localhost:5000")
    print(f"🔧 API Health: http://localhost:5000/api/health")
    print("\n📋 Available API endpoints:")
    print("  GET  /                 - Home page")
    print("  POST /api/upload       - Upload image")
    print("  POST /api/process      - Process OCR")
    print("  POST /api/translate    - Translate text")
    print("  POST /api/download     - Download result")
    print("  GET  /api/health       - Health check")
    print("  GET  /uploads/<file>   - Get uploaded image")
    print("="*60)
    print("\n🚀 Starting server...")
    print("⚠️  Press CTRL+C to stop")
    print("="*60 + "\n")
    
    app.run(
        debug=True,
        host='0.0.0.0',
        port=5000,
        threaded=True
    )