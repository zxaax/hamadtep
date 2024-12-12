"""
❃ `{i}تحميل صوتي` <(رابط يوتيوب/او اي رابط)>
   لـ تحميل الملف بشكل ملف صوتي في التليجرام، يمكنك وضع رابط اي منصة


❃ `{i}تحميل فيد` <(رابط يوتيوب/او اي رابط)>
   لـ تحميل الملف بشكل فيديو في التليجرام، يمكنك وضع رابط اي منصة


❃ `{i}صوتي` (عنوان)>
   لـ تحميل الملف بشكل ملف صوتي في التليجرام من خلال العنوان فقط بدون رابط

 By:@RR0R7 ~ @Zxaax
"""

import asyncio
import yt_dlp
from asyncio import sleep
from youtubesearchpython import Playlist
from yt_dlp import YoutubeDL
from Tepthon import zedub
from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..Config import Config
from ..helpers.functions.youtube import download_yt, get_yt_link
from ..helpers.functions.functionsr import is_url_work

plugin_category = "البحث"
LOGS = logging.getLogger(__name__)

ytd = {
        "prefer_ffmpeg": True,
        "addmetadata": True,
        "geo-bypass": True,
        "nocheckcertificate": True,
        "postprocessors": [{"key": "FFmpegMetadata"}],
    }

@zedub.zed_cmd(pattern="تحميل صوتي (.*)")
async def down_voic(event):
    bot = await event.edit_or_reply("⌔∮ جاري التحميل يرجى الانتظار قليلًا")
    ytd["format"] = "bestaudio"
    ytd["outtmpl"] = "%(id)s.m4a"
    ytd["postprocessors"].insert(
            0,
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
                "preferredquality": "128",
            },
        )
    url = event.pattern_match.group(1)
    if not url:
        return await bot.edit_or_reply("⌔∮ يجب عليك وضع رابط للتحميل الصوتي")
    try:
        await is_url_work(url)
    except BaseException:
        return await bot.edit_or_reply("⌔∮ يرجى وضع الرابط بشكل صحيح")
    await download_yt(bot, url, ytd)

@zedub.zed_cmd(pattern="تحميل فيد (.*)")
async def vidown(event):
    bot = await event.edit_or_reply("⌔∮ جاري التحميل يرجى الانتظار قليلًا")
    ytd["format"] = "best"
    ytd["outtmpl"] = "%(id)s.mp4"
    ytd["postprocessors"].insert(
        0, {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
        )
    url = event.pattern_match.group(1)
    print(url)
    if not url:
        return await bot.edit_or_reply("⌔∮ يجب عليك وضع رابط لتحميل الفيد")
    try:
        await is_url_work(url)
    except BaseException:
        return await bot.edit_or_reply("⌔∮ يرجى وضع الرابط بشكل صحيح")
    await download_yt(bot, url, ytd)


@zedub.zed_cmd(pattern="بحث( (.*)|$)")
async def sotea(event):
    bot = await event.edit_or_reply("⌔∮ جاري التحميل يرجى الانتظار قليلًا")
    ytd["format"] = "bestaudio"
    ytd["outtmpl"] = "%(id)s.m4a"
    ytd["postprocessors"].insert(
        0,
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "m4a",
            "preferredquality": "128",
        },
    )
    query = event.pattern_match.group(2) if event.pattern_match.group(1) else None
    if not query:
        return await bot.edit_or_reply("**⌔∮ يجب عليك تحديد ما تريد تحميله اكتب عنوان مع الأمر**")
    url = get_yt_link(query, ytd)
    if not url:
        return await bot.edit_or_reply("**⌔∮ لم يتم العثور على الفيديو اكتب عنوان مفصل بشكل صحيح**")
    await bot.eor("**⌔∮ جاري تحميل الملف الصوتي انتظر قليلًا**")
    await download_yt(bot, url, ytd)
