# Telegram Voice Bot 🎤🤖

A Telegram bot that receives voice messages, transcribes them using OpenAI's Whisper, generates intelligent responses with ChatGPT, and replies back with synthesized voice using OpenAI's Text-to-Speech API.

## Features

- 🎙️ **Voice-to-Voice Communication**: Send voice messages and receive voice responses
- 🔤 **Speech Recognition**: Uses OpenAI's Whisper model for accurate transcription
- 🤖 **AI-Powered Responses**: Leverages ChatGPT (GPT-3.5-turbo) for intelligent conversations
- 🗣️ **Text-to-Speech**: Converts responses to natural-sounding voice using OpenAI's TTS
- 🔄 **Audio Format Handling**: Automatically converts between OGG, MP3, and other formats
- 🧹 **Automatic Cleanup**: Removes temporary files after processing

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))
- OpenAI API Key (from [OpenAI Platform](https://platform.openai.com/api-keys))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/telegram-voice-bot.git
   cd telegram-voice-bot
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Configuration

### Getting a Telegram Bot Token

1. Open Telegram and search for [@BotFather](https://t.me/botfather)
2. Start a chat and send `/newbot`
3. Follow the instructions to create your bot
4. Copy the token provided by BotFather

### Getting an OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key (make sure to save it securely)

## Usage

1. **Start the bot**:
   ```bash
   python main.py
   ```

2. **Interact with your bot**:
   - Open Telegram and find your bot
   - Send `/start` to begin
   - Send a voice message and wait for the voice response

## How It Works

1. **Voice Reception**: Bot receives voice message in OGG format from Telegram
2. **Format Conversion**: Converts OGG to MP3 for compatibility with OpenAI APIs
3. **Transcription**: Uses OpenAI's Whisper model to convert speech to text
4. **AI Response**: Sends transcribed text to ChatGPT for intelligent response generation
5. **Text-to-Speech**: Converts the response text to speech using OpenAI's TTS API
6. **Voice Delivery**: Converts the generated audio back to OGG format and sends to user
7. **Cleanup**: Removes all temporary files

## Dependencies

- `python-telegram-bot` - Telegram Bot API wrapper
- `openai` - OpenAI API client
- `pydub` - Audio manipulation library
- `python-dotenv` - Environment variable management
- `httpx` - HTTP client for API requests

## Customization

### Voice Options
You can change the TTS voice by modifying line 113 in `main.py`:
```python
voice="alloy"  # Options: alloy, echo, fable, onyx, nova, shimmer
```

### AI Model
You can switch to GPT-4 by changing line 99 in `main.py`:
```python
model="gpt-4"  # Instead of "gpt-3.5-turbo"
```

## Error Handling

The bot includes comprehensive error handling for:
- Network connectivity issues
- API rate limits
- Audio format problems
- File system operations
- General exceptions

## Logging

The bot logs all important events including:
- Successful transcriptions
- Generated responses
- Error conditions
- File operations

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Troubleshooting

### Common Issues

**Bot doesn't respond to voice messages:**
- Check if your API keys are correctly set in the `.env` file
- Verify that your bot token is valid
- Ensure your OpenAI account has sufficient credits

**Audio quality issues:**
- Try different voice options in the TTS configuration
- Check your internet connection stability

**Permission errors:**
- Ensure the bot has write permissions in the working directory
- Check that temporary files can be created and deleted

## Acknowledgments

- [OpenAI](https://openai.com/) for Whisper, ChatGPT, and TTS APIs
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) for the excellent Telegram API wrapper
- [pydub](https://github.com/jiaaro/pydub) for audio processing capabilities

---

Made with ❤️ for seamless voice-to-voice AI conversations on Telegram 
