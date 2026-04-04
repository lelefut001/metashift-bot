import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
import random
import uuid
import time

def run_cmd(cmd):
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("FFMPEG ERROR:\n", res.stderr)
        raise RuntimeError("ffmpeg failed")

def rand(a, b):
    return round(random.uniform(a, b), 3)

import os
TOKEN = os.getenv("TOKEN")
print("TOKEN:", TOKEN)

ALLOWED_USERS = {6528488774}

FFMPEG = "ffmpeg"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
    "🚀 MetaShiftGG\n\n"
    "⚡ Fast\n"
    "🎯 Optimized\n"
    "🔒 Private\n\n" 
    "📤 Send Video for Generate 3 unique, ready-to-post video versions instantly.\n\n"
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
        prefix = random.choice(["IMG", "VID", "DSC"])
        timestamp = int(time.time())
        out = f"{prefix}_{timestamp}{random.randint(10,99)}.MP4"

        zoom = rand(1.01, 1.05)
        contrast = rand(0.95, 1.08)
        brightness = rand(-0.01, 0.01)
        saturation = rand(0.95, 1.08)
        crf = random.randint(17, 21)
        start = rand(0.0, 0.8)

        vf = (
             f"scale=1080:1920:force_original_aspect_ratio=increase,"
             f"crop=1080:1920,"
             f"eq=contrast={contrast}:brightness={brightness},"
             f"hue=s={saturation},"
             f"noise=alls={random.randint(2,5)}:allf=t,"
             f"unsharp=5:5:0.5:5:5:0.0"
        )

        cmd = [
            FFMPEG, "-y",
            "-ss", str(start),
            "-i", input_path,
            "-vf", vf,
            "-af", f"volume={rand(0.98,1.02)}",
            "-r", "30", str(random.randint(29,31)),
            "-metadata", f"title={uuid.uuid4()}",
            "-metadata", f"encoder={random.randint(1000,9999)}",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", str(crf),
            "-b:v", "3000k",
            "-maxrate", "4000k",
            "-bufsize", "8000k",

            "-c:a", "aac",
            "-b:a", "128k",

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
