#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
from telegram import Update, Voice
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from pydub import AudioSegment
from openai import OpenAI
import httpx
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração do logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Variáveis de ambiente
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # Token do Bot Telegram
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Chave da OpenAI

if not TELEGRAM_TOKEN:
    raise ValueError("TELEGRAM_TOKEN não encontrada nas variáveis de ambiente")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY não encontrada nas variáveis de ambiente")

# Inicializa o cliente OpenAI (nova versão v1.0+)
# Clear proxy environment variables that might interfere with httpx
proxy_vars_to_clear = [
    "HTTP_PROXY",
    "HTTPS_PROXY",
    "http_proxy",
    "https_proxy",
    "ALL_PROXY",
    "all_proxy",
    "NO_PROXY",
    "no_proxy",
]

# Store original values to restore later if needed
original_proxy_values = {}
for var in proxy_vars_to_clear:
    if var in os.environ:
        original_proxy_values[var] = os.environ[var]
        del os.environ[var]

# Set the API key as environment variable
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

try:
    # Initialize OpenAI client with minimal parameters
    client = OpenAI(
        api_key=OPENAI_API_KEY, base_url="https://api.openai.com/v1", timeout=60.0
    )
    logger.info("OpenAI client initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize OpenAI client: {e}")
    raise


# Handler para o comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Olá! Envie uma mensagem de voz e eu responderei em voz. 🎤🤖"
    )


# Handler para mensagens de voz
async def voice_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        voice: Voice = update.message.voice
        chat_id = update.effective_chat.id

        # 1. Baixar o arquivo OGG enviado pelo usuário
        ogg_file = await context.bot.get_file(voice.file_id)
        ogg_path = f"temp_{chat_id}.ogg"
        await ogg_file.download_to_drive(ogg_path)

        # 2. Converter OGG para MP3 (Whisper/Transcrição só aceita MP3 ou WAV)
        mp3_path = f"temp_{chat_id}.mp3"
        audio = AudioSegment.from_file(ogg_path, format="ogg")
        audio.export(mp3_path, format="mp3")

        # 3. Transcrição com Whisper
        with open(mp3_path, "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
                model="whisper-1",  # modelo de transcrição Whisper
                file=audio_file,
            )
            texto = transcript.text
            logger.info(f"Transcrição recebida: {texto}")

        # 4. Gerar resposta de texto com ChatGPT
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",  # pode ser trocado por gpt-4, se disponível
            messages=[{"role": "user", "content": texto}],
        )
        response_text = completion.choices[0].message.content
        logger.info(f"Resposta gerada: {response_text}")

        # 5. Síntese de voz com TTS
        tts_response = client.audio.speech.create(
            model="tts-1",  # modelo de TTS
            voice="alloy",  # vozes disponíveis: alloy, echo, fable, onyx, nova, shimmer
            input=response_text,
        )

        # Salvar o áudio gerado pelo TTS em MP3
        tts_path = f"resp_{chat_id}.mp3"
        tts_response.stream_to_file(tts_path)

        # 6. Converter MP3 para OGG (formato aceito pelo Telegram para enviar mensagem de voz)
        ogg_resp_path = f"resp_{chat_id}.ogg"
        audio_resp = AudioSegment.from_file(tts_path, format="mp3")
        audio_resp.export(ogg_resp_path, format="ogg")

        # 7. Enviar resposta em voz de volta ao usuário
        with open(ogg_resp_path, "rb") as resp:
            await context.bot.send_voice(chat_id=chat_id, voice=resp)

        # 8. Limpeza de arquivos temporários
        for path in [ogg_path, mp3_path, tts_path, ogg_resp_path]:
            try:
                os.remove(path)
            except OSError as e:
                logger.warning(f"Falha ao remover arquivo {path}: {e}")

    except Exception as e:
        logger.error(f"Erro no processamento de voz: {e}")
        await update.message.reply_text(
            "Desculpe, ocorreu um erro ao processar seu áudio."
        )


# Handler para erros em geral
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Update {update} causou erro {context.error}")


# Função principal que cria e roda o bot
def main():
    # Cria a aplicação do bot usando ApplicationBuilder (v20+ do python-telegram-bot)
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Registra handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.VOICE, voice_handler))
    application.add_error_handler(error_handler)

    # Inicia o bot (Polling)
    application.run_polling()


if __name__ == "__main__":
    main()
