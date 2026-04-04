import os
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler
import random
import uuid
import time

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        if res.returncode != 0:
            print("FFMPEG ERROR:\n", res.stderr)
            return False
        return True
    except subprocess.TimeoutExpired:
        print("FFMPEG TIMEOUT")
        return False

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
    "⚡ Veloce\n"
    "🎯 Ottimizzato\n"
    "🔒 Uso Privato\n\n" 
    "📤 Manda un video per generarne 3 diversi, all'istante.\n\n"
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

    await msg.reply_text("Genero 3 versioni differenti...⚡⌛")

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
            f"scale=720:-2,"
            f"eq=contrast={contrast}:brightness={brightness},"
            f"hue=s={saturation}"
        )

        cmd = [
            FFMPEG, "-y",
            "-loglevel", "error",
            "-ss", str(start),
            "-i", input_path,
            "-vf", vf,
            "-af", f"volume={rand(0.98,1.02)}",
            "-r", "30",
            "-metadata", f"title={uuid.uuid4()}",
            "-metadata", f"encoder={random.randint(1000,9999)}",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", str(crf),

            "-c:a", "aac",
            "-b:a", "128k",

            out
        ]

        print("START", i)
        ok = run_cmd(cmd)
        print("END", i, ok)
        if ok:
            outputs.append(out)
        else:
            print("Qualcosa è andato storto, Riprova")
        
        try:
            os.remove(input_path)
        except:
            pass

        for out in outputs:
            try:
                os.remove(out)
            except:
                pass
        for out in outputs:
            try:
                with open(out, "rb") as f:
                    await msg.reply_video(video=f)
            except Exception as e:
                print("Errore invio:", e) 
            
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_video))

print("BOT PARTITO")
app.run_polling()
