import os
import time
from telethon import events
from instaloader import Instaloader, Post
from Tepthon import zedub
from ..Config import Config

plugin_category = "البوت"

# تهيئة Instaloader
loader = Instaloader()

# تسجيل الدخول
loader.login("asg1.1gs", "asemsmeer")  # استبدل هذا باسم المستخدم وكلمة المرور

@zedub.on(events.NewMessage(pattern='.انستا (.*)'))
async def download_instagram_video(event):
    if event.sender_id != Config.OWNER_ID:
        return

    post_url = event.pattern_match.group(1)
    await event.reply(f"جاري تحميل الفيديو من الرابط: {post_url}...")

    try:
        shortcode = post_url.split("/")[-2]
        post = Post.from_shortcode(loader.context, shortcode)

        if post.is_video:
            filename = f"{shortcode}.mp4"
            loader.download_post(post, target=filename)

            await event.reply(f"تم تحميل الفيديو بنجاح: {post.title}\n⇜ جاري إرسال الملف...")
            await zedub.send_file(event.chat_id, filename)
            os.remove(filename)
        else:
            await event.reply("❌ هذا المنشور ليس فيديو.")
    except Exception as e:
        await event.reply(f"خطأ ❌: {e}")
        time.sleep(30)  # انتظر 30 ثانية قبل المحاولة مرة أخرى
