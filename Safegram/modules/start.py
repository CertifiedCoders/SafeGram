from pyrogram import filters
from pyrogram.enums import ParseMode
import time, platform, psutil
from pyrogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    CallbackQuery,
)
from config import LOGGER_ID
from Safegram import Safegram, BOT_USERNAME
from Safegram.modules.utils import time_formatter, size_formatter
from Safegram.mongo.usersdb import add_user, get_all_users
from Safegram.mongo.chatsdb import get_all_chats

# ── Constants ──
START_TEXT = """<b>🤖 ᴄᴏᴘʏʀɪɢʜᴛ & ᴄᴘ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ ʙᴏᴛ 🛡️</b>

ʜᴇʏ ᴛʜᴇʀᴇ! ɪ'ᴍ ʏᴏᴜʀ ɢʀᴏᴜᴘ'ꜱ ᴇɴғᴏʀᴄᴇʀ ʀᴏʙᴏᴛ 🤖  
ᴍʏ ᴍɪssɪᴏɴ ɪs ᴛᴏ ᴘʀᴏᴛᴇᴄᴛ ʏᴏᴜʀ ᴄᴏᴍᴍᴜɴɪᴛʏ ғʀᴏᴍ:

• ғᴀᴋᴇ ᴄᴏᴘʏʀɪɢʜᴛ ʀᴇᴘᴏʀᴛs 🚫  
• ᴄʜɪʟᴅ ᴇxᴘʟᴏɪᴛᴀᴛɪᴏɴ ᴄᴏɴᴛᴇɴᴛ ❌  
• ʟᴏɴɢ ᴀɴᴅ sᴜsᴘɪᴄɪᴏᴜs ᴇᴅɪᴛᴇᴅ ᴍᴇssᴀɢᴇs 📝  
• ɢʀᴏᴜᴘ sᴘᴀᴍ & ɪɴᴛʀᴜsɪᴏɴ 🔐

➥ ʜᴏᴡ ᴛᴏ ᴇɴᴀʙʟᴇ ᴘʀᴏᴛᴇᴄᴛɪᴏɴ:
1. ➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ  
2. 🛡️ ɢʀᴀɴᴛ ᴍᴇ ᴀᴅᴍɪɴ ᴘᴇʀᴍɪssɪᴏɴs

ᴏɴᴄᴇ ᴇɴᴀʙʟᴇᴅ, ɪ'ʟʟ ᴄᴏɴᴛɪɴᴜᴏᴜsʟʏ ᴍᴏɴɪᴛᴏʀ ᴀɴᴅ ᴀᴄᴛ ᴛᴏ ᴋᴇᴇᴘ ʏᴏᴜʀ ɢʀᴏᴜᴘ sᴀғᴇ ✅

<b><a href="https://t.me/SafeGramRobot">ꜱᴀꜰᴇɢʀᴀᴍʀᴏʙᴏᴛ</a> — ʏᴏᴜʀ ᴅɪɢɪᴛᴀʟ ꜰɪʀᴇᴡᴀʟʟ 🔒</b>
"""

HELP_TEXT = """<b>🔖 ʜᴇʟᴘ ᴍᴇɴᴜ</b>

/auth <user_id> - ᴀᴜᴛʜᴏʀɪᴢᴇ ᴀ ᴍᴇᴍʙᴇʀ ɪɴ ᴛʜɪꜱ ᴄʜᴀᴛ  
/unauth <user_id> - ʀᴇᴍᴏᴠᴇ ᴀᴜᴛʜ ᴘʀɪᴠɪʟᴇɢᴇ  
/listauth - sʜᴏᴡ ᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴍᴇᴍʙᴇʀꜱ  
/broadcast - ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴛᴏ ɢʀᴏᴜᴘs  
/ping - ᴄʜᴇᴄᴋ ʙᴏᴛ sᴛᴀᴛᴜꜱ  
/stats - ʙᴏᴛ ᴜꜱᴀɢᴇ ᴅᴀᴛᴀ
"""

start_time = time.time()

@Safegram.on_message(filters.command("start"))
async def start_command_handler(_, msg: Message):
    if msg.chat.type == "private":
        await add_user(msg.from_user.id)
        try:
            await Safegram.send_message(
                LOGGER_ID,
                f"👤 **New User Started Bot**\n\n🆔: `{msg.from_user.id}`\n👤: [{msg.from_user.first_name}](tg://user?id={msg.from_user.id})",
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            pass

    buttons = [
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("🧩 ʜᴇʟᴘ", callback_data="show_help")]
    ]
    await msg.reply_photo(
        photo="https://telegra.ph/file/8f6b2cc26b522a252b16a.jpg",
        caption=START_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.HTML
    )

@Safegram.on_callback_query(filters.regex("show_help"))
async def help_panel(_, query: CallbackQuery):
    buttons = [
        [InlineKeyboardButton("◀️ ʙᴀᴄᴋ", callback_data="back_to_start")],
    ]
    await query.message.edit_text(
        HELP_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.HTML
    )

@Safegram.on_callback_query(filters.regex("back_to_start"))
async def back_to_start(_, query: CallbackQuery):
    buttons = [
        [InlineKeyboardButton("➕ ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("🧩 ʜᴇʟᴘ", callback_data="show_help")]
    ]
    await query.message.edit_text(
        START_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode=ParseMode.HTML
    )

@Safegram.on_message(filters.command("ping"))
async def activevc(_, message: Message):
    uptime = time_formatter((time.time() - start_time) * 1000)
    cpu = psutil.cpu_percent()
    storage = psutil.disk_usage('/')
    python_version = platform.python_version()

    await message.reply_text(
        f"🏓 **ᴘᴏɴɢ ʀᴇꜱᴘᴏɴꜱᴇ!**\n\n"
        f"➪ ᴜᴘᴛɪᴍᴇ: `{uptime}`\n"
        f"➪ ᴄᴘᴜ: `{cpu}%`\n"
        f"➪ ᴅɪꜱᴋ: `{size_formatter(storage.used)} / {size_formatter(storage.total)}`\n"
        f"➪ ꜰʀᴇᴇ: `{size_formatter(storage.free)}`\n"
        f"➪ ᴘʏᴛʜᴏɴ: `{python_version}`",
        parse_mode=ParseMode.MARKDOWN,
    )

@Safegram.on_message(filters.command("stats"))
async def stats_command(_, message: Message):
    users = await get_all_users()
    chats = await get_all_chats()
    uptime = time_formatter((time.time() - start_time) * 1000)
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/')

    await message.reply_text(
        f"📊 **ʙᴏᴛ ꜱᴛᴀᴛɪꜱᴛɪᴄꜱ**\n\n"
        f"👥 ᴜꜱᴇʀꜱ: `{len(users)}`\n"
        f"👨‍👩‍👧‍👦 ɢʀᴏᴜᴘꜱ: `{len(chats)}`\n"
        f"⏱️ ᴜᴘᴛɪᴍᴇ: `{uptime}`\n\n"
        f"🧠 ᴄᴘᴜ: `{cpu}%`\n"
        f"💾 ʀᴀᴍ: `{ram}%`\n"
        f"🗃️ ᴅɪꜱᴋ: `{size_formatter(disk.used)} / {size_formatter(disk.total)}`\n"
        f"📂 ꜰʀᴇᴇ: `{size_formatter(disk.free)}`",
        parse_mode=ParseMode.MARKDOWN,
    )
