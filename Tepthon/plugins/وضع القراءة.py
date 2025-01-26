#zxaax
from telethon import events, TelegramClient
from Tepthon import zedub 
from ..Config import Config

plugin_category = "البوت"

# لتخزين حالة عدم القراءة
read_status = {}

@zedub.on(events.NewMessage(pattern=r'\.تفعيل عدم القراءة'))
async def activate_no_read(event):
    read_status[event.sender_id] = True
    await event.reply("✅ تم تفعيل عدم القراءة. لن تظهر لك علامة القراءة بعد الآن.")

@zedub.on(events.NewMessage(pattern=r'\.تعطيل عدم القراءة'))
async def deactivate_no_read(event):
    read_status[event.sender_id] = False
    await event.reply("✅ تم تعطيل عدم القراءة. ستظهر لك علامة القراءة الآن.")
    
@zedub.on(events.NewMessage())
async def handle_read_status(event):
    # إذا كان الوضع مفعلًا، لا تظهر علامة القراءة
    if event.sender_id in read_status and read_status[event.sender_id]:
        await event.mark_read(False)  # لا تسجل الرسالة كتم قراءتها
