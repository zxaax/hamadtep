from telethon import events
from Tepthon import zedub

# متغير لتتبع حالة عدم القراءة
is_read_enabled = False

@zedub.on(events.NewMessage(pattern=r'\.تفعيل عدم القراءة'))
async def activate_reading(event):
    global is_read_enabled
    is_read_enabled = True
    await event.reply("✅ تم تفعيل عدم القراءة. يمكنك قراءة الرسائل دون أن تظهر للشخص الآخر أنك قرأتها.")

@zedub.on(events.NewMessage(pattern=r'\.تعطيل عدم القراءة'))
async def deactivate_reading(event):
    global is_read_enabled
    is_read_enabled = False
    await event.reply("❌ تم تعطيل عدم القراءة. ستظهر الآن أنك قمت بقراءة الرسائل.")

@zedub.on(events.NewMessage(incoming=True))
async def read_event(event):
    global is_read_enabled
    if is_read_enabled:
        # تمت قراءتها لكنها لا تظهر 
        return
    else:
        # تظهر الرسالة على أنها مقروءة
        await event.mark_as_read()
