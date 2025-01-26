#zxaax
from telethon import events
from Tepthon import zedub
from ..Config import Config

plugin_category = "البوت"

# متغير لتخزين حالة "عدم القراءة"
read_status = {}

@zedub.on(events.NewMessage(pattern=r'\.تفعيل عدم القراءة'))
async def activate_read_status(event):
    read_status[event.sender_id] = True
    await event.reply("✅ تم تفعيل عدم القراءة. لن تظهر للمستخدمين أنك قرأت رسائلهم.")

@zedub.on(events.NewMessage(pattern=r'\.تعطيل عدم القراءة'))
async def deactivate_read_status(event):
    read_status[event.sender_id] = False
    await event.reply("✅ تم تعطيل عدم القراءة. ستظهر للمستخدمين أنك قرأت رسائلهم.")

@zedub.on(events.NewMessage())
async def handle_messages(event):
    # التحقق مما إذا كان "عدم القراءة" مفعلًا للمستخدم
    if read_status.get(event.sender_id, False):
        # إخفاء علامة القراءة
        await event.message.mark_read = False
    else:
        # السماح بعلامة القراءة الافتراضية
        await event.message.mark_read = True
