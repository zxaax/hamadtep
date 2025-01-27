from telethon import TelegramClient, events
from Tepthon import zedub
from ..Config import Config
import asyncio

async def send_message_to_bot(bot_username, message):
    bot = await zedub.get_input_entity(bot_username)
    await zedub.send_message(bot, message)

@zedub.on(events.NewMessage(pattern='\.انستا (.+)'))
async def download_video(event):
    url = event.pattern_match.group(1)

    try:
        # إرسال الرابط إلى البوت مباشرة
        await send_message_to_bot('@instasavegrambot', url)
        
        # الانتظار للرد من البوت
        await asyncio.sleep(3)  # الانتظار لبضعة ثوانٍ قبل قراءة الرد

        # الانتظار للرد من البوت
        async for response in zedub.iter_messages('@instasavegrambot', limit=1):
            # تحقق من أن البوت أرسل فيديو
            if response.video:
                # إرسال الفيديو مع الوصف إلى المستخدم
                await event.respond(file=response.video, caption='تم التحميل بواسطة @Tepthon')
            else:
                await event.respond('لم يتم العثور على فيديو. يرجى تجربة رابط آخر.')
                
    except Exception as e:
        if "Forbidden" in str(e):  # إذا كان البوت محظورًا من قبل المستخدم
            await event.respond('مرحبًا، يجب عليك التأكد من أنك لم تقم بحظر البوت @instasavegrambot')
        else:
            await event.respond(f'حدث خطأ: {str(e)}')

async def main():
    await zedub.start()
    print("البوت جاهز!")
    await zedub.run_until_disconnected()

if __name__ == "__main__":  # التأكد من استخدام __name__ بشكل صحيح
    asyncio.run(main())  # استخدم asyncio.run لتشغيل الدالة الرئيسية
