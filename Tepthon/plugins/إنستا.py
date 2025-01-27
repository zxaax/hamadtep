from telethon import TelegramClient, events
from ..Config import Config

client = TelegramClient('my_session', Config.APP_ID, Config.API_HASH)

async def send_message_to_bot(bot_username, message):
    bot = await client.get_input_entity(bot_username)
    await client.send_message(bot, message)

@client.on(events.NewMessage(pattern='\.انستا (.+)'))
async def download_video(event):
    url = event.pattern_match.group(1)

    try:
        # إرسال الرابط إلى البوت مباشرة
        await send_message_to_bot('@instasavegrambot', url)

        # انتظر رد البوت
        response = await client.get_messages('@instasavegrambot', limit=1)

        # تحقق من أن البوت أرسل الفيديو
        if response and response[0].video:
            # إرسال الفيديو مع الوصف إلى المستخدم
            await event.respond(response[0].video)
            await event.respond('تم التحميل بواسطة @Tepthon')
        else:
            await event.respond('لم يتم العثور على فيديو. يرجى تجربة رابط آخر.')

    except Exception as e:
        if "Forbidden" in str(e):  # إذا كان البوت محظورًا من قبل المستخدم
            await event.respond('مرحبًا، يجب عليك التأكد من أنك لم تقم بحظر البوت @instasavegrambot')
        else:
            await event.respond(f'حدث خطأ: {str(e)}')

async def main():
    await client.start()
    print("البوت جاهز!")
    await client.run_until_disconnected()

if __name__ == "__main__":
    # استخدم async with هنا
    with client: 
        client.loop.run_until_complete(main())
