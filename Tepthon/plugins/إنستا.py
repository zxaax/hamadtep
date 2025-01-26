from instaloader import Instaloader, Post
from telethon import events
from Tepthon import zedub 
from ..Config import Config

plugin_category = "البوت"

@zedub.on(events.NewMessage(pattern='.انستا'))
async def download_instagram_video(event):
    # احصل على رابط الفيديو من الرسالة
    post_url = event.message.text.split(maxsplit=1)[1] if len(event.message.text.split()) > 1 else None
    
    if not post_url:
        await event.reply("يرجى إدخال رابط الفيديو بعد الأمر.")
        return

    loader = Instaloader()

    # محاولة تجزئة URL المنشور للحصول على shortcode
    try:
        shortcode = post_url.split("/")[-2]
        post = Post.from_shortcode(loader.context, shortcode)

        if post.is_video:
            # تحديد اسم الملف
            filename = f"{shortcode}.mp4"
            # تحميل الفيديو
            loader.download_post(post, target=shortcode)

            await event.reply(f"📥 تم تحميل الفيديو بنجاح: {post.title}")
            # إرسال الفيديو إلى الدردشة
            await zedub.send_file(event.chat_id, f"{shortcode}/{filename}")

        else:
            await event.reply("❌ هذا المنشور ليس فيديو.")
    except Exception as e:
        await event.reply(f"⚠️ خطأ: {str(e)}")
