import time
import asyncio
from telethon import events
from Tepthon import zedub
from ..Config import Config

plugin_category = "البوت"

active_readers = {}

@zedub.on(events.NewMessage(pattern=r'\.القراءة تلقائيا (\d+) (\d+)'))
async def read_messages(event):
    try:
        input_text = event.message.text.split()
        if len(input_text) != 3:
            await event.reply("❌ يرجى استخدام الأمر بشكل صحيح: `.القراءة تلقائيا <عدد الثواني> <أيدي المستخدم>`")
            return
        
        seconds = int(input_text[1])
        user_id = int(input_text[2])

        if user_id not in active_readers:
            active_readers[user_id] = True
            
            await event.reply(f"📖 بدء القراءة تلقائيًا من المستخدم {user_id} كل {seconds} ثانية.")
            
            while active_readers[user_id]:
                await asyncio.sleep(seconds)
                try:
                    message = await zedub.get_message(event.chat_id, sender=user_id)
                    if message:
                        await event.reply(f"🔍 رسالة من {user_id}: {message.text}")
                    else:
                        await event.reply(f"❗ لم يتم العثور على رسائل جديدة من {user_id}.")
                except Exception as e:
                    await event.reply(f"❌ حدث خطأ بينما نحاول جلب رسالة: {str(e)}")
        
        else:
            await event.reply("❌ القراءة تلقائيًا لهذا المستخدم قيد التنفيذ بالفعل.")

    except ValueError:
        await event.reply("❌ يرجى التأكد من أن الأرقام صحيحة وضمن النطاق.")
    except Exception as e:
        await event.reply(f"❌ حدث خطأ غير متوقع: {str(e)}")

@zedub.on(events.NewMessage(pattern=r'\.القراءة تلقائيا للجميع (\d+)'))
async def read_messages_all(event):
    try:
        input_text = event.message.text.split()
        if len(input_text) != 3:
            await event.reply("❌ يرجى استخدام الأمر بشكل صحيح: `.القراءة تلقائيا للجميع <عدد الثواني>`")
            return
        
        seconds = int(input_text[2])

        await event.reply(f"📖 بدء القراءة تلقائيًا من جميع المستخدمين كل {seconds} ثانية.")
        
        while True:
            await asyncio.sleep(seconds)
            async for user in zedub.iter_participants(event.chat_id):
                message = await zedub.get_message(event.chat_id, sender=user.id)
                if message:
                    await event.reply(f"🔍 رسالة من {user.id}: {message.text}")
                else:
                    await event.reply(f"❗ لم يتم العثور على رسائل جديدة من {user.id}.")
    
    except ValueError:
        await event.reply("❌ يرجى التأكد من أن الأرقام صحيحة وضمن النطاق.")
    except Exception as e:
        await event.reply(f"❌ حدث خطأ غير متوقع: {str(e)}")

@zedub.on(events.NewMessage(pattern=r'\.ايقاف القراءة تلقائيا'))
async def stop_reading(event):
    if active_readers:
        active_readers.clear()
        await event.reply("⏹️ تم إيقاف القراءة تلقائيًا.")
    else:
        await event.reply("❌ لا توجد عملية قراءة قيد التنفيذ.")
