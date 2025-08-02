from flask import Flask, render_template, request, jsonify, send_file
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import speech_recognition as sr
from gtts import gTTS
import io
import os
import tempfile
from langdetect import detect
import warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Language mapping for detection and translation
LANGUAGE_MAP = {
    'en': 'English',
    'hi': 'Hindi', 
    'ur': 'Urdu',
    'mr': 'Marathi',
    'bn': 'Bengali',
    'ta': 'Tamil',
    'te': 'Telugu',
    'gu': 'Gujarati',
    'kn': 'Kannada',
    'ml': 'Malayalam',
    'pa': 'Punjabi',
    'or': 'Odia',
    'as': 'Assamese',
    'ar': 'Arabic',
    'fa': 'Persian/Farsi',
    'ru': 'Russian',
    'tr': 'Turkish',
    'fr': 'French',
    'de': 'German',
    'es': 'Spanish',
    'pt': 'Portuguese',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese',
    'th': 'Thai',
    'vi': 'Vietnamese',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'no': 'Norwegian'
}

# Translation model mapping with faster, smaller models
TRANSLATION_MODELS = {
    'en': {
        'hi': 'Helsinki-NLP/opus-mt-en-hi',
        'ur': 'Helsinki-NLP/opus-mt-en-ur',
        'bn': 'Helsinki-NLP/opus-mt-en-bn',
        'ta': 'Helsinki-NLP/opus-mt-en-ta',
        'ar': 'Helsinki-NLP/opus-mt-en-ar',
        'fa': 'Helsinki-NLP/opus-mt-en-fa',
        'ru': 'Helsinki-NLP/opus-mt-en-ru',
        'tr': 'Helsinki-NLP/opus-mt-en-tr',
        'fr': 'Helsinki-NLP/opus-mt-en-fr',
        'de': 'Helsinki-NLP/opus-mt-en-de',
        'es': 'Helsinki-NLP/opus-mt-en-es',
        'pt': 'Helsinki-NLP/opus-mt-en-pt',
        'it': 'Helsinki-NLP/opus-mt-en-it',
        'ja': 'Helsinki-NLP/opus-mt-en-jap',
        'ko': 'Helsinki-NLP/opus-mt-en-ko',
        'zh': 'Helsinki-NLP/opus-mt-en-zh',
        'nl': 'Helsinki-NLP/opus-mt-en-nl',
        'sv': 'Helsinki-NLP/opus-mt-en-sv'
    },
    'reverse': {
        'hi': 'Helsinki-NLP/opus-mt-hi-en',
        'ur': 'Helsinki-NLP/opus-mt-ur-en',
        'bn': 'Helsinki-NLP/opus-mt-bn-en',
        'ta': 'Helsinki-NLP/opus-mt-ta-en',
        'ar': 'Helsinki-NLP/opus-mt-ar-en',
        'fa': 'Helsinki-NLP/opus-mt-fa-en',
        'ru': 'Helsinki-NLP/opus-mt-ru-en',
        'tr': 'Helsinki-NLP/opus-mt-tr-en',
        'fr': 'Helsinki-NLP/opus-mt-fr-en',
        'de': 'Helsinki-NLP/opus-mt-de-en',
        'es': 'Helsinki-NLP/opus-mt-es-en',
        'pt': 'Helsinki-NLP/opus-mt-pt-en',
        'it': 'Helsinki-NLP/opus-mt-it-en',
        'ja': 'Helsinki-NLP/opus-mt-jap-en',
        'ko': 'Helsinki-NLP/opus-mt-ko-en',
        'zh': 'Helsinki-NLP/opus-mt-zh-en',
        'nl': 'Helsinki-NLP/opus-mt-nl-en',
        'sv': 'Helsinki-NLP/opus-mt-sv-en'
    }
}

# Google Translate API alternative - faster translation using deep-translator
try:
    from deep_translator import GoogleTranslator
    USE_GOOGLE_TRANSLATE = True
    print("Google Translate library loaded - using for fast translations")
except ImportError:
    USE_GOOGLE_TRANSLATE = False
    print("Google Translate not available - using Helsinki models")

# Global model cache to keep models in memory
model_cache = {}

def load_translation_model(source_lang, target_lang):
    """Load and cache translation models for speed"""
    model_key = f"{source_lang}-{target_lang}"
    
    if model_key in model_cache:
        return model_cache[model_key]
    
    try:
        # Try direct model first
        if source_lang == 'en' and target_lang in TRANSLATION_MODELS['en']:
            model_name = TRANSLATION_MODELS['en'][target_lang]
        elif target_lang == 'en' and source_lang in TRANSLATION_MODELS['reverse']:
            model_name = TRANSLATION_MODELS['reverse'][source_lang]
        else:
            # Model not available, use Google Translate as fallback
            return None
        
        print(f"Loading Helsinki model: {model_name}")
        
        # Try to load with protobuf tokenizer first
        try:
            tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            translator = pipeline("translation", model=model, tokenizer=tokenizer)
        except Exception as tokenizer_error:
            print(f"Helsinki model failed: {tokenizer_error}")
            return None
        
        model_cache[model_key] = translator
        print(f"Helsinki model {model_name} loaded and cached successfully")
        return translator
        
    except Exception as e:
        print(f"Error loading Helsinki model: {str(e)}")
        return None

def translate_text(text, source_lang, target_lang):
    """Translate text using fast Google Translate or cached Helsinki models"""
    if source_lang == target_lang:
        return text
    
    try:
        # Use Google Translate for speed if available
        if USE_GOOGLE_TRANSLATE:
            try:
                translator = GoogleTranslator(source=source_lang, target=target_lang)
                result = translator.translate(text)
                return result
            except Exception as google_error:
                print(f"Google Translate failed: {google_error}")
                # Fall through to Helsinki models
        
        # Try Helsinki models as fallback
        translator = load_translation_model(source_lang, target_lang)
        if translator:
            result = translator(text, max_length=512)
            return result[0]['translation_text']
        
        # Use English as intermediate if no direct model
        if source_lang != 'en' and target_lang != 'en':
            # First translate to English
            en_translator = load_translation_model(source_lang, 'en')
            if en_translator:
                en_text = en_translator(text, max_length=512)[0]['translation_text']
                # Then translate from English to target
                target_translator = load_translation_model('en', target_lang)
                if target_translator:
                    result = target_translator(en_text, max_length=512)
                    return result[0]['translation_text']
        
        return "Translation not available for this language pair"
        
    except Exception as e:
        print(f"Translation error: {str(e)}")
        return f"Error during translation: {str(e)}"

def detect_language(text):
    """Detect the language of input text"""
    try:
        detected = detect(text)
        return detected if detected in LANGUAGE_MAP else 'en'
    except:
        return 'en'

@app.route('/')
def index():
    return render_template('index.html', languages=LANGUAGE_MAP)

@app.route('/translate', methods=['POST'])
def translate():
    try:
        data = request.json
        text = data.get('text', '').strip()
        target_lang = data.get('target_lang', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'})
        
        # Auto-detect source language
        source_lang = detect_language(text)
        
        # Translate text
        translated_text = translate_text(text, source_lang, target_lang)
        
        return jsonify({
            'original_text': text,
            'translated_text': translated_text,
            'source_language': LANGUAGE_MAP.get(source_lang, 'Unknown'),
            'target_language': LANGUAGE_MAP.get(target_lang, 'Unknown'),
            'source_lang_code': source_lang,
            'target_lang_code': target_lang
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/voice_input', methods=['POST'])
def voice_input():
    """Handle voice input - this is mainly for fallback, frontend uses Web Speech API"""
    try:
        # This endpoint is kept for compatibility but frontend now uses Web Speech API
        return jsonify({
            'message': 'Please use the microphone button in the browser for voice input',
            'status': 'use_web_speech_api'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/voice_output', methods=['POST'])
def voice_output():
    try:
        data = request.json
        text = data.get('text', '')
        lang = data.get('lang', 'en')
        
        if not text:
            return jsonify({'error': 'No text provided'})
        
        # Enhanced language mapping for gTTS
        gtts_lang_map = {
            'en': 'en', 'hi': 'hi', 'ur': 'ur', 'bn': 'bn', 'ta': 'ta', 'te': 'te',
            'gu': 'gu', 'ml': 'ml', 'ar': 'ar', 'fa': 'fa', 'ru': 'ru', 'tr': 'tr',
            'fr': 'fr', 'de': 'de', 'es': 'es', 'pt': 'pt', 'it': 'it', 'ja': 'ja',
            'ko': 'ko', 'zh': 'zh', 'th': 'th', 'vi': 'vi', 'nl': 'nl', 'sv': 'sv',
            'no': 'no', 'mr': 'mr', 'pa': 'pa', 'or': 'en', 'as': 'en', 'kn': 'kn'
        }
        
        gtts_lang = gtts_lang_map.get(lang, 'en')
        
        print(f"Generating TTS for text: '{text[:50]}...' in language: {gtts_lang}")
        
        # Generate speech with error handling
        try:
            tts = gTTS(text=text, lang=gtts_lang, slow=False)
        except Exception as tts_error:
            print(f"TTS generation failed with {gtts_lang}, falling back to English")
            tts = gTTS(text=text, lang='en', slow=False)
        
        # Save to temporary file with better cleanup
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        try:
            tts.save(temp_file.name)
            temp_file.close()
            
            # Send file and schedule cleanup
            def cleanup_file():
                try:
                    os.unlink(temp_file.name)
                except:
                    pass
            
            # Return the file
            response = send_file(temp_file.name, 
                               as_attachment=False, 
                               download_name='speech.mp3',
                               mimetype='audio/mpeg')
            
            # Schedule cleanup after a delay
            import threading
            timer = threading.Timer(30.0, cleanup_file)  # Clean up after 30 seconds
            timer.start()
            
            return response
            
        except Exception as save_error:
            # Clean up temp file if saving failed
            try:
                os.unlink(temp_file.name)
            except:
                pass
            raise save_error
            
    except Exception as e:
        print(f"Voice output error: {str(e)}")
        return jsonify({'error': f'Error generating audio: {str(e)}'})

if __name__ == '__main__':
    print("Starting AI Multi-Language Translator...")
    
    if USE_GOOGLE_TRANSLATE:
        print("Using Google Translate for FAST translations!")
        print("All translations will be instant and accurate!")
    else:
        print("Loading Helsinki models (this may take a moment)...")
        # Pre-load some common models for faster initial translations
        load_translation_model('en', 'hi')  # English to Hindi
        load_translation_model('en', 'es')  # English to Spanish
    
    print("Server ready!")
    app.run(debug=True, host='0.0.0.0', port=5000)
