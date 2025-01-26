import asyncio
from telethon import TelegramClient, events
from Tepthon import zedub
from ..Config import Config

plugin_category = "البوت"

@zedub.on(events.NewMessage(pattern='.مغادرة'))
async def leave_all_channels(event):
    # تحقق مما إذا كان المرسل هو الحساب المنصب فقط
    if event.sender_id != Config.OWNER_ID:  # تأكد من استبدال Config.OWNER_ID بمعرف صاحب الحساب
        return

    await event.reply("جاري مغادرة جميع القنوات...")

    try:
        async for dialog in zedub.iter_dialogs():
            if dialog.is_channel:
                await zedub.leave_dialog(dialog)  # مغادرة القناة
                await event.reply(f"✅ مغادرة القناة: {dialog.title}")

        await event.reply("✅ تم مغادرة جميع القنوات بنجاح.")
    except Exception as e:
        await event.reply(f"خطأ ❌: {e}")
