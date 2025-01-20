import requests
import os
from telethon import TelegramClient, events
from ..Config import Config  # تعديل حسب مشروعك

# إعدادات Telethon
client = TelegramClient("session_name", Config.APP_ID, Config.API_HASH)

@client.on(events.NewMessage(outgoing=True, pattern=r'\.تشغيل (.+)'))
async def fetch_and_send_audio(event):
    query = event.pattern_match.group(1)  # الكلمة (رابط الفيديو)
    if not query.startswith("http"):
        await event.reply("**⎉╎يرجى إدخال رابط صحيح لفيديو يوتيوب.**")
        return

    # رابط API مع الكلمة المدخلة
    api_url = f"https://bk9.fun/download/youtube?url={query}"
    
    try:
        # إرسال طلب إلى API
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()

        # التحقق من استجابة الـ API
        if "link" not in data:
            await event.reply("**⎉╎حدث خطأ أثناء معالجة الرابط. تأكد من أنه صالح.**")
            return

        # استخراج رابط الصوت
        audio_link = data["link"]
        file_name = "downloaded_audio.mp3"

        # تحميل الصوت
        await event.reply("**⎉╎جاري تنزيل المقطع الصوتي...**")
        audio_response = requests.get(audio_link, stream=True)
        with open(file_name, "wb") as file:
            for chunk in audio_response.iter_content(chunk_size=1024):
                file.write(chunk)

        # إرسال الصوت كملف
        await event.reply("**⎉╎تم التنزيل بنجاح. جاري الإرسال...**")
        await event.client.send_file(event.chat_id, file_name, caption="**⎉╎تم التشغيل بنجاح 🎧**")

        # حذف الملف بعد الإرسال
        os.remove(file_name)

    except requests.exceptions.RequestException as e:
        await event.reply(f"**⎉╎حدث خطأ أثناء الوصول إلى API: {str(e)}**")
    except Exception as e:
        await event.reply(f"**⎉╎حدث خطأ: {str(e)}**")

# تشغيل العميل
client.start()
client.run_until_disconnected()
