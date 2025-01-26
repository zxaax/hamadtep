import time
import asyncio
from Tepthon import zedub
from telethon import events
from ..Config import Config

plugin_category = "البوت"

active_readers = {}

@zedub.on(events.NewMessage(pattern=r'\.القراءة تلقائيا (\d+) (\d+)'))
async def read_messages(event):
    try:
        seconds = int(event.message.text.split()[1])
        user_id = int(event.message.text.split()[2])

        if user_id not in active_readers:
            active_readers[user_id] = True
            
            await event.reply(f"📖 بدء القراءة تلقائيًا من المستخدم {user_id} كل {seconds} ثانية.")
            
            while active_readers[user_id]:
                await asyncio.sleep(seconds)
                message = await zedub.get_message(event.chat_id, sender=user_id)
                if message:
                    await event.reply(f"🔍 رسالة من {user_id}: {message.text}")
                else:
                    await event.reply(f"❗ لم يتم العثور على رسائل جديدة من {user_id}.")
        
        else:
            await event.reply("❌ القراءة تلقائيًا لهذا المستخدم قيد التنفيذ بالفعل.")
    
    except (IndexError, ValueError):
        await event.reply("❌ يرجى التأكد من استخدام الأمر بشكل صحيح: `.القراءة تلقائيا <عدد الثواني> <أيدي المستخدم>`")

@zedub.on(events.NewMessage(pattern=r'\.القراءة تلقائيا للجميع (\d+)'))
async def read_messages_all(event):
    try:
        seconds = int(event.message.text.split()[2])
        
        await event.reply(f"📖 بدء القراءة تلقائيًا من جميع المستخدمين كل {seconds} ثانية.")
        
        while True:
            await asyncio.sleep(seconds)
            async for user in zedub.iter_participants(event.chat_id):
                message = await zedub.get_message(event.chat_id, sender=user.id)
                if message:
                    await event.reply(f"🔍 رسالة من {user.id}: {message.text}")
                else:
                    await event.reply(f"❗ لم يتم العثور على رسائل جديدة من {user.id}.")
    
    except (IndexError, ValueError):
        await event.reply("❌ يرجى التأكد من استخدام الأمر بشكل صحيح: `.القراءة تلقائيا للجميع <عدد الثواني>`")

@zedub.on(events.NewMessage(pattern=r'\.ايقاف القراءة تلقائيا'))
async def stop_reading(event):
    if active_readers:
        active_readers.clear()
        await event.reply("⏹️ تم إيقاف القراءة تلقائيًا.")
    else:
        await event.reply("❌ لا توجد عملية قراءة قيد التنفيذ.")
