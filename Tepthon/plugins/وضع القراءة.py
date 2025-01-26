import asyncio
from telethon import events
from Tepthon import zedub

# تعريف المتغيرات الجديدة
custom_enabled = False
custom_timer_enabled = False
OWNER_ID = {}

@zedub.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def mark_as_read(event):
    global custom_timer_enabled, OWNER_ID
    sender_id = event.sender_id
    if custom_timer_enabled and sender_id in OWNER_ID:
        custom_time = OWNER_ID[sender_id]
        if custom_time > 0:
            await asyncio.sleep(custom_time)
        await event.mark_read()

@zedub.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل التخصيص$'))
async def disable_custom(event):
    global custom_timer_enabled
    custom_timer_enabled = False
    await event.edit('᯽︙ تم تعطيل أمر التخصيص بنجاح ✅')

@zedub.on(events.NewMessage(outgoing=True, pattern=r'^\.تخصيص (\d+) (\d+)$'))
async def enable_custom(event):
    global custom_timer_enabled, OWNER_ID
    custom_time = int(event.pattern_match.group(1))
    user_id = int(event.pattern_match.group(2)) 
    OWNER_ID[user_id] = custom_time
    custom_timer_enabled = True
    await event.edit(f'᯽︙ تم تفعيل أمر التخصيص بنجاح مع {custom_time} ثانية للمستخدم {user_id}')

@zedub.on(events.NewMessage(outgoing=True, pattern=r'^\.تعطيل تخصيص الجميع$'))
async def disable_global_custom(event):
    global custom_enabled
    custom_enabled = False
    await event.edit('᯽︙ تم تعطيل أمر التخصيص للجميع بنجاح ✅')

@zedub.on(admin_cmd(pattern=f"تخصيص عام (\d+)"))
async def enable_global_custom(event):
    global custom_enabled, custom_global_time
    custom_global_time = int(event.pattern_match.group(1))
    custom_enabled = True
    await event.edit(f'᯽︙ تم تفعيل أمر التخصيص بنجاح مع {custom_global_time} ثانية')

@zedub.on(events.NewMessage(incoming=True, func=lambda e: e.is_private))
async def handle_global_custom(event):
    global custom_enabled, custom_global_time
    if custom_enabled:
        await asyncio.sleep(custom_global_time)
        await event.mark_read()
