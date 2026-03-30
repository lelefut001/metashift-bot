import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
import random
import uuid

def run_cmd(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFMPEG ERROR:\n", res.stderr)
        raise RuntimeError("ffmpeg failed")

def rand(a, b):
    return round(random.uniform(a, b), 3)

TOKEN = "8236374381:AAFTWoQO-5UbDMm01X2RieToXJ5Z9jnoliQ"

ALLOWED_USERS = {6528488774}

FFMPEG = "ffmpeg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    "🚀 MetaShiftGG\n\n"
    "Generate 3 unique, ready-to-post video versions instantly.\n\n"
    "⚡ Fast\n"
    "🎯 Optimized\n"
    "🔒 Private"
)

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ALLOWED_USERS:
        print("ACCESSO NEGATO:", update.effective_user.id)
        return

    print("VIDEO RICEVUTO")

    msg = update.message

    if not msg.video and not msg.document:
        return

    file = await (msg.video or msg.document).get_file()

    uid = str(uuid.uuid4())[:8]
    input_path = f"input_{uid}.mp4"
    await file.download_to_drive(input_path)

    await msg.reply_text("⚡ Generating 3 versions...")

    outputs = []

    for i in range(3):
        out = f"out_{uid}_{i}.mp4"

        zoom = rand(1.01, 1.05)
        contrast = rand(0.95, 1.08)
        brightness = rand(-0.02, 0.02)
        saturation = rand(0.95, 1.08)
        crf = random.randint(22, 28)
        start = rand(0.0, 0.8)

        vf = (
            f"scale=iw*{zoom}:ih*{zoom},crop=iw:ih,"
            f"eq=contrast={contrast}:brightness={brightness},"
            f"hue=s={saturation}"
        )

        cmd = [
            FFMPEG, "-y",
            "-ss", str(start),
            "-i", input_path,
            "-vf", vf,
            "-c:v", "libx264",
            "-crf", str(crf),
            "-c:a", "aac",
            out
        ]

        run_cmd(cmd)
        outputs.append(out)

    for out in outputs:
        await msg.reply_video(video=open(out, "rb"))

    os.remove(input_path)
    for out in outputs:
        os.remove(out)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_video))

print("BOT PARTITO")
app.run_polling()
