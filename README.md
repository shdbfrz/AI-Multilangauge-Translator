# AI Multi-Language Translator

A fast and accurate AI-powered multi-language translator web application built with Flask and Hugging Face Transformers.

## Features

- 🌍 **30+ Languages Support**: Hindi, Urdu, Marathi, Bengali, Tamil, Arabic, Farsi, Russian, Turkish, French, German, Spanish, and many more
- 🤖 **Auto Language Detection**: Automatically detects the input language
- ⚡ **Fast & Local**: Models are cached in memory for ultra-fast translations
- 🎤 **Voice Input**: Speech-to-text using SpeechRecognition
- 🔊 **Voice Output**: Text-to-speech using gTTS
- 🔒 **Privacy First**: All translations run locally, no external APIs
- 📱 **Responsive Design**: Beautiful, mobile-friendly interface
- 🔄 **Language Swapping**: Easy language pair swapping
- 📋 **Copy & Clear**: Quick copy and clear functionality

## Supported Languages

- **Indian Languages**: Hindi, Urdu, Marathi, Bengali, Tamil, Telugu, Gujarati, Kannada, Malayalam, Punjabi, Odia, Assamese
- **International**: English, Arabic, Persian/Farsi, Russian, Turkish, French, German, Spanish, Portuguese, Italian, Japanese, Korean, Chinese, Thai, Vietnamese, Dutch, Swedish, Norwegian

## Installation & Setup

1. **Clone or Download** this project to your computer

2. **Install Python Dependencies**:
   ```bash
   pip install flask transformers torch langdetect speechrecognition gtts pyaudio
   ```

3. **For Voice Input (Optional)**:
   - Windows: `pip install pyaudio`
   - macOS: `brew install portaudio && pip install pyaudio`
   - Linux: `sudo apt-get install python3-pyaudio`

## Quick Start

1. **Run the Application**:
   ```bash
   python app.py
   ```

2. **Open Your Browser**:
   - Go to `http://localhost:5000`
   - Start translating!

## How It Works

### Translation Engine
- Uses **Helsinki-NLP models** from Hugging Face
- Models are loaded once and cached in memory for speed
- Supports direct language pairs and English as intermediate language
- No external APIs required - everything runs locally

### Voice Features
- **Voice Input**: Uses `SpeechRecognition` library with Google's speech service
- **Voice Output**: Uses `gTTS` (Google Text-to-Speech) for audio generation
- Supports multiple languages for both input and output

### Auto Language Detection
- Uses `langdetect` library to automatically identify input language
- Falls back to English if detection fails
- Displays detected language to user

## Usage Tips

1. **First Run**: The app will download and cache translation models automatically
2. **Fast Translation**: After first use, translations are nearly instant
3. **Voice Input**: Click the microphone button and speak clearly
4. **Voice Output**: Click the speaker button to hear the translation
5. **Auto-Translate**: The app automatically translates as you type (with 1-second delay)
6. **Language Swap**: Use the swap button to quickly reverse translation direction

## Technical Details

### Model Caching
The application intelligently caches models in memory:
- Models are loaded only once per language pair
- Common models (EN-HI, EN-ES, EN-FR) are pre-loaded for speed
- Memory usage is optimized for production use

### Translation Strategy
1. **Direct Translation**: If a direct model exists (e.g., EN→HI)
2. **Intermediate Translation**: Uses English as bridge language
3. **Fallback**: Graceful error handling with informative messages

### File Structure
```
translator/
├── app.py              # Main Flask application
├── templates/
│   └── index.html      # Frontend interface
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Requirements

- Python 3.7+
- Flask
- Transformers (Hugging Face)
- PyTorch
- langdetect
- SpeechRecognition
- gTTS
- PyAudio (for voice input)

## Browser Compatibility

- Chrome/Chromium (Recommended)
- Firefox
- Safari
- Edge

## Performance Notes

- **First Translation**: May take 10-30 seconds (model download)
- **Subsequent Translations**: < 2 seconds
- **Memory Usage**: ~2-4GB RAM (depending on cached models)
- **Disk Space**: ~500MB-2GB (for downloaded models)

## Troubleshooting

### Voice Input Issues
- Ensure microphone permissions are granted
- Check if PyAudio is properly installed
- Try using Chrome browser for best compatibility

### Model Loading Issues
- Ensure stable internet connection for initial model download
- Check available disk space (models can be large)
- Restart the application if models fail to load

### Translation Errors
- Some language pairs may not have direct models
- The app will attempt to use English as intermediate language
- Check console logs for detailed error messages

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this translator!

## Acknowledgments

- **Hugging Face** for the amazing Transformers library
- **Helsinki-NLP** for the high-quality translation models
- **Google** for Speech Recognition and Text-to-Speech services
- **Flask** community for the excellent web framework
