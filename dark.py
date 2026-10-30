# -*- coding: utf-8 -*-
import asyncio
import json
import os
import shutil
import random
import time
import logging
import requests
import io
from datetime import datetime, timezone, timedelta
from telegram import Update, ReactionTypeEmoji, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackQueryHandler

# ==================== WATERMARK & CONFIG (DARK) ====================
WATERMARK_NAME = "DARK"
LOG_PREFIX = "[DARK-BOT]"

_z = lambda *v: "".join(map(chr, v))
_X0 = _z(126,97,109,97,110,107,101,110,103)
_X1 = _z(126,97,109,97,110,107,101,110,103,118,49)
_X2 = _z(126,97,109,97,110,107,101,110,103,118,50)
_X3 = _z(126,97,109,97,110,107,101,110,103,118,51)

# ---------------------------
# CONFIG
# ---------------------------
TOKENS = [
             "9195371529:AAE2zcr7v06JPfYKS3SipXGNvcBPUo2BNkE",
                "9097946274:AAFSx3rCg9jfrai3ElFCsPXzirP1f6jHVwo",
                 "8884201707:AAGNEQihUZjrx8iTVUQeiplyTDPqcge5uiE",
                 "9107574334:AAFq3OhDhWPEHQYTPeF9d9LgM2IpIqXr2uk",
                 "8558091284:AAF_7MZa31Ye7VlrI-ELLQwsxPrJ-j8fp94",
                    "9057052080:AAHWPHhiWRuu5vyFd3hVUdnieN4MkpS6fuM",
                    "8519209115:AAGuH2wvWCLDDL4x9NRpGEMLhl2yNd2la0s",
                     "9125101504:AAH6GmtVK7AtGauojdWMEKexJZyizmg1gec",
                      "9049802034:AAF54g6Q_v_jiqM97jZ2AJOrgU2q1Lp2XnM",
    
]

OWNER_IDS = [1957382694]

# ==================== OWNER FILE HOSTING ====================
HOSTING_DIR = os.path.join(os.getcwd(), "owner_hosted_files")
os.makedirs(HOSTING_DIR, exist_ok=True)

ADMINS_FILE = "admin_ids.json"
GROUPS_FILE = "monitored_groups.json"
SUDO_FILE = "sudo.json"
UNAUTHORIZED_MESSAGE = "𝐁ɪɴᴀ 𝐃𝐀𝐑𝐊 ❄️ 𝐁ᴀᴀᴘ 𝐊 𝐏ᴇʀᴍɪꜱꜱɪᴏɴ 𝐊 𝐂ᴏᴍᴍᴀɴᴅ 𝐊ᴇꜱᴇ 𝐔ꜱᴇ 𝐊ᴀʀᴀ 𝐑ɴᴅʏᴋᴇ 𝐁ᴀᴄʜᴇ ~😡🖕"

RAID_TEXTS = ["#𝐃𝐀𝐑𝐊  !!  🦢 𝐊ᴏ 𝐁ᴀᴀᴘ 𝐁ᴀɴᴀ 𝐋ᴇ 𝐑ᴀɴᴅɪ 𝐊ᴇ  𝐁ᴀᴄʜᴇ", "𝐌ᴜᴊʜِه 𝐏ᴀᴘᴀ  𝐁ᴏʟ 𝐑ᴀɴᴅɪ 🤣", "𝐓ᴇʀɪ 𝐌ᴀᴀ 𝐂ʜᴜᴅᴡᴀ 𝐋ᴇ 𝐘ᴀʜᴀ 😀", "𝐑ʀ 𝐊ᴀʀ 𝐑ᴀɴᴅɪ 𝐊ᴇ 𝐁ᴀᴄʜᴇ 😃", "𝐌ᴇʀᴇ 𝐒ᴇ 𝐌ᴀᴀ 𝐂ʜ𝐮ᴅᴡᴀ 𝐋ᴇ 𝐒ʟɪᴅᴇ 𝐊ᴀʀ 𝐊ᴇ !!", "𝐘ᴀʜᴀ 𝐂ʜᴜⴷ 𝐑ᴀɴᴅɪ 𝐊ᴇ 𝐁ᴀᴄʜᴇ 😃", "𝐓ᴇʀɪ 𝐁ʜᴇɴ 𝐂ʜᴜᴅ 𝐊ᴇ 𝐌ᴀʀ 𝐆ʏɪ?", "𝐌ᴀᴀ 𝐂ʜ𝐝ᴡᴀ 𝐋ᴇ 𝐓𝐞𝐫ɪ 🤣", "𝑯𝒂𝒘𝒂𝒃𝒂𝒂𝒛𝒊 𝒌𝒂𝒓 𝒇𝒂𝒎𝒆 𝒎𝒊𝒍𝒆 𝒈𝒂!", "𝐓𝐦𝐤𝐜 𝐎𝐤", "𝐓𝐞𝐫𝐢 𝐦𝐚𝐚 150𝐫𝐬 𝐦𝐞 𝐝𝐞𝐭𝐢 𝐡𝐚𝐢 😃", "𝑺𝒍𝒊𝒅𝒆 𝒌𝒂𝒓 𝒎𝒂𝒅𝒓𝒄𝒉𝒐𝒅!", "𝑪𝒉𝒖𝒅 𝒐𝒏𝒍𝒊𝒏𝒆 𝒇𝒚𝒕𝒓!", "𝑩𝒉𝒂𝒘 𝒅𝒖 𝒓𝒓 𝒘𝒉𝒚 𝑹𝒂𝒏𝒅𝒊?", "𝑳𝒐𝒍 𝒂𝒊𝒔𝒆 𝒓𝒐𝒚𝒆 𝒈𝒂 😀", "𝑹𝒐 𝑹𝒐 𝑹𝒐 𝒕𝒆𝒓𝒊 𝒎𝒂𝒂 𝒕𝒐𝒉 𝒄𝒉𝒖𝒅 𝒌𝒊 𝒉𝒂𝒔𝒉 𝒓𝒉𝒊 😃", "𝐂𝐡𝐮𝐝 𝐠𝐚𝐫𝐞𝐞𝐛!", "𝐌𝐤𝐜 𝐧𝐨 𝐛𝐡𝐚𝐰 𝐭𝐚𝐭𝐭𝐞!", "𝐋𝐨𝐥 𝐜𝐡𝐮𝐝 𝐤𝐢 𝐫𝐨 𝐫𝐡𝐚 𝐚𝐛𝐡 𝐡𝐚𝐰𝐚𝐛𝐚𝐚𝐳 🤣", "𝐀𝐰𝐰 𝐑𝐚𝐧𝐝𝐢 𝐭𝐞𝐫𝐢 𝐦𝐚𝐚 𝐭𝐨𝐡 𝐜𝐡𝐮𝐝 𝐠𝐲𝐢!", "𝑩𝒐𝒉𝒐𝒕 𝒄𝒉𝒖𝒅𝒊 𝒕𝒉𝒊 𝑻𝒆𝒓𝒊 𝒎𝒂𝒂 𝒓𝒂𝒂𝒕 𝒌𝒐 𝒎𝒆𝒓𝒆 𝒔𝒆 😀", "𝐇ᴀsʏ ʜᴀsʏ 𝐂ʜ𝚞𝗱 ᴄʜ𝚞𝗱 𝐊ɪ 𝐓𝐞ʀɪ ᴍ𝒂ᴀ 𝐇ᴀsʏ 😄", "𝐍𝐡𝐢 𝐧𝐡𝐢 𝐧𝐡𝐢 𝐚𝐛𝐡 𝐭𝐨𝐡 𝐭𝐞𝐫𝐢 𝐦𝐚𝐚 𝐜h𝐮𝐝 𝐤𝐢 𝐫𝐚𝐡𝐞 𝐠𝐢 ! 😗", "𝐍𝐡𝐢 𝐧𝐡𝐢 𝐧𝐡𝐢 𝐚𝐛𝐡𝐢𝐣𝐞𝐞𝐭 𝐢𝐬𝐬 𝐭𝐚𝐭𝐭𝐞 𝐤𝐢 𝐦𝐚𝐚 𝐭𝐨𝐡 𝐜𝐡𝐮𝐝𝐢 𝐠𝐢 ! 🙂‍↔️", "𝐊𝐘𝐔 𝐅𝐘𝐓𝐑 𝐁𝐀𝐍 𝐊𝐈 𝐌𝐀𝐀 𝐂𝐇𝐔𝐃𝐖𝐀 𝐋𝐄 ? 😀", "𝐍𝐇𝐈 𝐍𝐇𝐈 𝐀𝐁𝐇 𝐊𝐔𝐂𝐇 𝐍𝐇𝐈 𝐇𝐎 𝐒𝐀𝐊𝐓𝐀 𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐊𝐈 𝐂𝐇𝐔𝐃𝐀𝐈 𝐊𝐈 𝐒𝐂𝐑𝐈𝐏𝐓 𝐑𝐄𝐀𝐃𝐘 𝐇𝐎 𝐆𝐘𝐈 𝐇𝐀𝐈 𝐀𝐁𝐇 𝐁𝐀𝐒 𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐂𝐇𝐔𝐃 𝐇𝐄 𝐒𝐀𝐊𝐓𝐈 𝐇𝐀𝐈 ! 😃", "𝐁𝐄𝐓𝐀 𝐘𝐀𝐀𝐃 𝐍𝐇𝐈 𝐀𝐀𝐑𝐀 𝐖𝐎𝐇 𝐊𝐎𝐍𝐒𝐀 𝐉𝐀𝐃𝐔 𝐓𝐇𝐀 𝐉𝐎 𝐔𝐒𝐒 𝐑𝐀𝐀𝐓 𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐊𝐈 𝐒𝐀𝐓𝐇 𝐊𝐈𝐘𝐀 𝐓𝐇𝐀 𝐉𝐎 𝐓𝐔 𝐀𝐀𝐘𝐀 𝐃𝐔𝐍𝐈𝐘𝐀 𝐌𝐄 🙂‍↔️", "𝐂𝐎𝐎𝐋 𝐁𝐀𝐍 𝐆𝐀𝐘𝐀 𝐁𝐄𝐓𝐀 𝐁𝐀𝐀𝐏 𝐊𝐈 𝐂𝐎𝐏𝐘 𝐇𝐀𝐀 𝐀𝐀𝐊𝐄𝐑 𝐁𝐄𝐓𝐀 𝐌𝐄𝐑𝐀 𝐇𝐀𝐈! 🥳", "𝐀𝐑𝐄 𝐂𝐇𝐔𝐃 𝐊𝐈 𝐁𝐇𝐀𝐆 𝐊𝐘𝐔 𝐑𝐇𝐈 𝐇𝐎 𝐑𝐀𝐍𝐃𝐈 𝐓𝐇𝐎𝐃𝐈 𝐆𝐀𝐍𝐃 𝐇𝐀𝐌 𝐒𝐄 𝐁𝐇𝐈 𝐌𝐀𝐀𝐑𝐖𝐀 𝐋𝐎 😁", "𝐇𝐀𝐌 𝐂𝐈𝐃 𝐒𝐄 𝐇𝐀𝐈 𝐓𝐔𝐌𝐀𝐑𝐄 𝐌𝐀𝐀 𝐊𝐈 𝐋𝐄𝐍𝐄 𝐀𝐀𝐘𝐄 𝐇𝐀𝐈 𝐁𝐀𝐃𝐄 𝐃𝐈𝐍𝐎 𝐁𝐀𝐀𝐃 😔", "𝐊𝐘𝐀 𝐇𝐔𝐀 𝐑𝐀𝐍𝐃𝐈 𝐓𝐇𝐎𝐃𝐈 𝐁𝐊𝐂 𝐇𝐀𝐌𝐍𝐄 𝐊𝐘𝐀 𝐊𝐀𝐑 𝐋𝐄 𝐓𝐔𝐌 𝐓𝐎𝐇 𝐑𝐎𝐍𝐄 𝐋𝐀𝐆 𝐆𝐘𝐀 🤗", "𝐑𝐀𝐍𝐃𝐈 𝐂𝐕𝐑 𝐊𝐀𝐑𝐍𝐀 𝐉𝐀𝐑𝐔𝐑𝐈 𝐇𝐀𝐈 𝐍𝐇𝐈 𝐓𝐎𝐇 𝐀𝐀𝐏 𝐊𝐈 𝐌𝐀𝐀 9 𝐌𝐎𝐍𝐓𝐇𝐒 𝐂𝐕𝐑 𝐍𝐇𝐈 𝐊𝐀𝐑 𝐏𝐀𝐘𝐄 𝐆𝐈 🤭", "𝐊𝐘𝐔 𝐑𝐄𝐄 𝐌𝐀𝐃𝐀𝐑𝐂𝐇𝐎𝐃 𝐘𝐀𝐇𝐀 𝐂𝐇𝐎𝐏 𝐊𝐈 𝐌𝐀𝐀 𝐂𝐇𝐔𝐃𝐖𝐀 𝐑𝐀𝐇𝐀 𝐇𝐀𝐈 𝐁𝐇𝐄𝐍𝐂𝐇𝐎𝐃 🙂‍↕️", "𝐌𝐄𝐈𝐍 𝐇𝐔 𝐀𝐊𝐄𝐋𝐀 𝐌𝐄𝐑𝐄 𝐏𝐀𝐒𝐒 𝐇𝐀𝐈 𝐊𝐀𝐋𝐀 𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐊𝐎 𝐏𝐈𝐋𝐄 𝐑𝐀𝐀𝐓 𝐃𝐈𝐍 𝐓𝐇𝐀𝐊𝐄𝐋𝐀 😄", "𝐀𝐀𝐉𝐀 𝐑𝐀𝐍𝐃𝐈 𝐅𝐘𝐓𝐑 𝐁𝐀𝐍𝐀𝐓𝐀 𝐇𝐔 𝐀𝐁𝐇𝐈𝐉𝐄𝐄𝐓 𝐈𝐒 𝐑𝐀𝐍ْد𝐈 𝐊𝐎 𝐅𝐘𝐓 𝐒𝐈𝐊𝐇𝐀𝐎 😃", "𝐀𝐀𝐉 𝐊𝐈 𝐓𝐀𝐉𝐀 𝐊𝐇𝐀𝐁𝐀𝐑 𝐈𝐒 𝐓𝐀𝐓𝐓𝐀 𝐊𝐈 𝐌𝐀𝐀  𝐂𝐇𝐔𝐃𝐄 𝐆𝐇𝐀𝐑 𝐆𝐇𝐀𝐑 ! 😀", "𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐂𝐇𝐔𝐃 𝐆𝐘𝐈 𝐓𝐎𝐇 𝐈𝐒𝐌𝐄 𝐁𝐇𝐈 𝐌𝐄𝐑𝐈 𝐆𝐀𝐋𝐓𝐈 ! 😙", "𝐀𝐑𝐄𝐄 𝐁𝐄𝐓𝐀 𝐓𝐔 𝐓𝐎𝐇 𝐁𝐊𝐂 𝐁𝐊𝐂 𝐌𝐄 𝐇𝐄 𝐂𝐇𝐔𝐃 𝐆𝐘𝐀??"]

FLAGNC_EMOJIS = ["🇮🇳", "🇵🇰", "🇦🇫", "🇺🇸", "🇬🇧", "🇨🇦", "🇦🇺", "🇩🇪", "🇫🇷", "🇮🇹", "🇯🇵", "🇰🇷", "🇧🇷", "🇷🇺", "🇿🇦", "🇲🇽", "🇪🇸", "🇸🇦", "🇹🇷", "🇮🇩"]
HEARTNC_EMOJIS = ["❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔", "❤️‍🔥", "❤️‍🩹", "❣️", "💕", "💞", "💓", "💗", "💖", "💘", "💝"]
AESTHETICNC_EMOJIS = ["🕊️", "🤍", "🌸", "🎀", "🦢", "🐚", "🩰", "☁️", "✨", "🧊", "🎐", "💎", "🦋", "🍃", "🧸"]
VEGETABLENC_EMOJIS = ["🥬", "🥦", "🌽", "🥕", "🫑", "🥒", "🍆", "🍅", "🥔", "🧄", "🧅", "🥜", "🫒"]
ANIMALNC_EMOJIS = ["🐶", "🐱", "🐭", "🐹", "🐰", "🦊", "🐻", "🐼", "🐨", "🐯", "🦁", "🐮", "🐷", "🐸", "🐵", "🐒", "🐔", "🐧", "🐦", "🐤"]
EXONC_TEXTS = ["💀", "🔥", "⚡", "🎯", "💥", "👑", "🔱", "💫", "⭐", "🌟", "✨", "🎀", "❤️", "🖤"]

ALL_NC_TEXT = "𝐁ʜᴜꜱᴀɴᴅɪ ꜱᴀᴀɴᴅ "
ALL_SPAM_TEXT = "𝐓𝐄𝐑𝐈 𝐌𝐀𝐀 𝐊𝐈 𝐂𝐇𝐔𝐓 𝐌𝐄 𝐏𝐀𝐈𝐑 𝐌𝐄𝐑𝐀 🔥⚡"

SPAM_TEMPLATE = [
    "━━━━━━━━ 💗᪲᪲᪲࣪ ִֶָ☾.ᯓᡣ𐭩🤍ྀི    ✝ 𝐀ɴᴛᴀ𝐑 𝐌ᴀɴ𝐓ᴀʀ 𝐒ʜ𝐀ɪ𝐓ᴀɴ𝐈 𝐊ʜᴏ𝐏ᴀ𝐃𝐀 {hater} 𝐆ᴀ𝐑ɪ𝐁 𝐊ɪ 𝐀ᴍᴍ𝐈 𝐊ᴀ 𝐊ᴀ𝐋𝐀 𝐁ʜᴏs𝐃ᴀ  ━━━━━━━━",
    "🦅 𝐌αᴛᴋҽ 𝐌ҽ 𝐍ʜι 𝐓ʜα 𝐏αɳι 💦 {target} 🕷   𝐊ι 𝐌αα -- 𝐁α𝐡αη 𝐑αη∂ᵢуσ 𝐊ι 𝐑αηι 🧊❤️‍🔥🥵👈🏻______________"
]

SUDO_USERS = set(OWNER_IDS)
global_delay = 0.05
spam_delay = 0.5
global_mode = False
MAX_THREADS = 500
current_threads = 70
bot_usernames = []
sudo_usernames = {} 
setmphoto_data = {}  
custom_layout = ""
LAYOUT_FILE = "layout.json"
WELCOME_FILE = "welcome.json"
welcome_config = {"photo_id": "", "caption": ""}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def load_data():
    global SUDO_USERS, sudo_usernames
    if os.path.exists(SUDO_FILE):
        try:
            with open(SUDO_FILE, "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    SUDO_USERS.update(data)
                elif isinstance(data, dict):
                    SUDO_USERS.update([int(k) for k in data.keys()])
                    sudo_usernames.update(data)
        except: pass
    
    if os.path.exists("sudo_names.json"):
        try:
            with open("sudo_names.json", "r") as f:
                sudo_usernames.update(json.load(f))
        except: pass
    
    for uid in SUDO_USERS:
        if str(uid) not in sudo_usernames:
            sudo_usernames[str(uid)] = "User_" + str(uid)

def save_sudo():
    with open(SUDO_FILE, "w") as f: json.dump(list(SUDO_USERS), f)
    with open("sudo_names.json", "w") as f: json.dump(sudo_usernames, f)

SLAVES_FILE = "slaves.json"
slaves_list = []

def load_slaves():
    global slaves_list
    if os.path.exists(SLAVES_FILE):
        try:
            with open(SLAVES_FILE, "r") as f:
                data = json.load(f)
            migrated = []
            for item in data:
                if isinstance(item, str):
                    migrated.append({"name": item, "videos": []})
                else:
                    migrated.append(item)
            slaves_list = migrated
        except:
            slaves_list = []

target_names = {}
swipe_tasks = {} 
gnc_cache = {}   

GNC_PREFIXES = ["🌈₊˚🎀⊹♡🌻✨", "👑⋆˚࿔⚡︎𖤐🔥", "☠⋆༒︎𖤐⛧⚚"]
GNC_SUFFIXES = ["  𝑻𝑬𝑹𝑰 𝑹À𝑵𝑫𝑰 𝑴À𝑨 𝑲𝑰 𝑪𝑯𝑼𝑫𝑨𝑰 𝑫𝑬𝑲𝑯 ›🇨🇽‹ ❤️TMKC"]
GNC_STYLES = {
    "darkncx":   (1,  0,  "👑 Dᴀʀᴋɴᴄx 𝐍ᴄ"),
    "aesthetic": (1,  0,  "✨ Aᴇꜱᴛʜ𝒆ᴛɪc 𝐍ᴄ"),
    "dark":      (2,  0,  "☠️ Dᴀʀᴋ 𝐍ᴄ"),
    "cute":      (0,  0,  "🌈 Cᴜᴛᴇ 𝐍ᴄ"),
    "neon":      (1,  0,  "⚡ Nᴇᴏɴ 𝐍ᴄ"),
    "gamer":     (2,  0,  "🎮 Gᴀᴍᴇʀ 𝐍ᴄ"),
    "mythic":    (1,  0,  "🔱 Mʏᴛʜɪᴄ 𝐍ᴄ"),
    "glitch":    (2,  0,  "💀 Gʟɪᴛᴄʜ 𝐍ᴄ"),
    "soft":      (0,  0,  "🦋 Sᴏꜰᴛ 𝐍ᴄ"),
    "crown":     (1,  0,  "🔥 Cʀᴏᴡɴ 𝐍ᴄ"),
}
_GNC_STYLE_ORDER = ["darkncx", "aesthetic", "dark", "cute", "neon", "gamer", "mythic", "glitch", "soft", "crown"]

def _gnc_keyboard(uid):
    keyboard = []
    for i in range(0, len(_GNC_STYLE_ORDER), 2):
        row = []
        for key in _GNC_STYLE_ORDER[i:i+2]:
            lbl = GNC_STYLES[key][2]
            row.append(InlineKeyboardButton(lbl, callback_data=f"gnc_{uid}_{key}"))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)

def _gnc_format(text, style_key):
    pi, si = GNC_STYLES.get(style_key, (0, 0))[0:2]
    return f"{GNC_PREFIXES[pi]} {text} {GNC_SUFFIXES[si]}"

swipe_names = {} 
react_mode = {} 
dreact_mode = {} 
group_tasks = {}
spam_tasks = {}
pfp_tasks = {}

GAMEOVER_FILE = "gameover_videos.json"
gameover_videos = {}  

def load_gameover_videos():
    global gameover_videos
    if os.path.exists(GAMEOVER_FILE):
        try:
            with open(GAMEOVER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict):
                    gameover_videos = data
        except Exception:
            gameover_videos = {}

def only_sudo(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if not update.message: return
        if update.effective_user.id not in SUDO_USERS:
            await update.message.reply_text(UNAUTHORIZED_MESSAGE)
            return
        return await func(update, context)
    return wrapper

@only_sudo
async def addgameover_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ 𝐊𝐢𝐬𝐢 𝐕𝐈𝐃𝐄𝐎 𝐩𝐞 𝐫𝐞𝐩𝐥𝐲 𝐤𝐚𝐫𝐤𝐞 /Addgameover 𝐥𝐢𝐤𝐡𝐨!")
    replied = update.message.reply_to_message
    if not replied.video:
        return await update.message.reply_text("⚠️ 𝐑𝐞𝐩𝐥𝐲 𝐦𝐮𝐬𝐭 𝐛𝐞 𝐚 𝐕𝐈𝐃𝐄𝐎!")
    bot_id = str(context.bot.id)
    gameover_videos[bot_id] = replied.video.file_id
    with open(GAMEOVER_FILE, "w", encoding="utf-8") as f:
        json.dump(gameover_videos, f, ensure_ascii=False, indent=2)
    await update.message.reply_text("✅ 𝐆𝐀𝐌𝐄 𝐎𝐕𝐄𝐑 𝐕𝐈𝐃𝐄𝐎 𝐒𝐀𝐕𝐄𝐃!")

@only_sudo
async def gameover_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message: return
    bot_id = str(context.bot.id)
    video_id = gameover_videos.get(bot_id)
    if not video_id:
        return await update.message.reply_text("⚠️ 𝐏𝐞𝐡𝐥𝐞 𝐤𝐢𝐬𝐢 𝐕𝐈𝐃𝐄𝐎 𝐩𝐞 𝐫𝐞𝐩𝐥𝐲 𝐤𝐚𝐫𝐤𝐞 /Addgameover 𝐬𝐞 𝐬𝐚𝐯𝐞 𝐤𝐚𝐫𝐨!")
    target = None
    if update.message.reply_to_message and update.message.reply_to_message.from_user:
        user = update.message.reply_to_message.from_user
        target = user.first_name or user.username or str(user.id)
    elif context.args: target = " ".join(context.args)
    if not target: target = "BHAW"
    gc_name = update.effective_chat.title or "PRIVATE CHAT"
    caption = f"{target} 𝐆𝐀𝐌𝐄 𝐎𝐕𝐄𝐑 𝐇𝐎 𝐆𝐘𝐀 𝐓𝐄𝐑𝐀 𝐀𝐁 𝐇𝐀𝐖𝐀𝐁𝐀𝐙𝐈 𝐊𝐀𝐑𝐍𝐄 𝐌𝐀𝐓 𝐀𝐀𝐍𝐀 𝑴𝑨𝑨 𝑪𝑯𝑼𝑫𝑨 𝑻𝑼 𝑴𝑨𝑨 𝑪𝑯𝑼𝑫𝑨𝒀𝑬 𝑻𝑬𝑹𝑰 𝑯𝑨𝑾𝑨𝑩𝑨𝑨𝑴𝑰\n{gc_name}"
    try:
        await context.bot.send_video(chat_id=update.message.chat_id, video=video_id, caption=caption)
    except Exception as e:
        logger.error(f"Game Over video send failed: {e}")

@only_sudo
async def swipe_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ 𝐊𝐢𝐬𝐢 𝐤𝐞 𝐦𝐬𝐠 𝐩𝐞 𝐫𝐞𝐩𝐥𝐲 𝐤𝐚𝐫𝐤𝐞 /swipe 𝐥𝐢𝐤𝐡𝐨!")
    chat_id = update.message.chat_id
    target_msg_id = update.message.reply_to_message.message_id
    name = " ".join(context.args) if context.args else (update.message.reply_to_message.from_user.first_name or "Target")
    swipe_names[chat_id] = name
    if chat_id in swipe_tasks:
        for t in swipe_tasks[chat_id]: t.cancel()
    async def swipe_loop(bot, cid, tmid, n):
        while True:
            try:
                msg = f"{n} {random.choice(RAID_TEXTS)}"
                await bot.send_message(cid, msg, reply_to_message_id=tmid)
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: await asyncio.sleep(1)
    swipe_tasks[chat_id] = [asyncio.create_task(swipe_loop(bot, chat_id, target_msg_id, name)) for bot in bots]
    await update.message.reply_text(f"⚔️ 𝐒𝐖𝐈𝐏𝐄 𝐒𝐓𝐀𝐑𝐓𝐄𝐃 𝐎𝐍 {name}!")

@only_sudo
async def stopswipe_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if cid in swipe_tasks:
        for t in swipe_tasks[cid]: t.cancel()
        del swipe_tasks[cid]
    await update.message.reply_text("🛑 𝐒𝐖𝐈𝐏𝐄 𝐒𝐓𝐎𝐏𝐏𝐄𝐃!")

@only_sudo
async def react_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ 𝐔𝐬𝐚𝐠𝐞: /react <emoji>")
    react_mode[update.message.chat_id] = context.args[0]
    await update.message.reply_text(f"✅ 𝐑𝐄𝐀𝐂𝐓𝐈𝐎𝐍 𝐒𝐓𝐀𝐑𝐓𝐄𝐃: {context.args[0]}")

@only_sudo
async def stopreact_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    react_mode.pop(update.message.chat_id, None)
    await update.message.reply_text("🛑 𝐑𝐄𝐀𝐂𝐓𝐈𝐎𝐍 𝐒𝐓𝐎𝐏𝐏𝐄𝐃!")

@only_sudo
async def changename_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return await update.message.reply_text("⚠️ 𝐔𝐬𝐚𝐠𝐞: /changename <name>")
    name = " ".join(context.args)
    count = 0
    for b in bots:
        try:
            await b.set_my_name(name=name)
            count += 1
        except: pass
    await update.message.reply_text(f"✅ 𝐂𝐇𝐀𝐍𝐆𝐄𝐃 𝐍𝐀𝐌𝐄 𝐎𝐅 {count} 𝐁𝐎𝐓𝐒!")

@only_sudo
async def setpfp_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Bot PFP changes are handled via BotFather.")

async def god_speed_loop(bot, chat_id, base_text):
    while True:
        try:
            ext = random.choice(EXONC_TEXTS)
            await bot.set_chat_title(chat_id, f"{base_text} {ext}")
            await asyncio.sleep(global_delay + 1)
        except asyncio.CancelledError: break
        except: await asyncio.sleep(2)

async def spam_loop(bot, chat_id, text):
    while True:
        try:
            await bot.send_message(chat_id, text)
            await asyncio.sleep(spam_delay)
        except asyncio.CancelledError: break
        except: await asyncio.sleep(2)

async def sequence_spam_loop(bot, cid, hater_name):
    idx = 0
    while True:
        try:
            template = SPAM_TEMPLATE[idx % len(SPAM_TEMPLATE)]
            msg = template.replace("{hater}", hater_name).replace("{target}", hater_name)
            await bot.send_message(cid, msg)
            idx += 1
            await asyncio.sleep(spam_delay)
        except asyncio.CancelledError: break
        except: await asyncio.sleep(1)

@only_sudo
async def imagespam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.photo:
        return await update.message.reply_text("⚠️ 𝐑𝐞𝐩𝐥𝐲 𝐭𝐨 𝐚 𝐩𝐡𝐨𝐭𝐨.")
    cid = update.message.chat_id
    photo_id = update.message.reply_to_message.photo[-1].file_id
    async def image_spam_loop(bot, c, p):
        while True:
            try:
                await bot.send_photo(c, photo=p)
                await asyncio.sleep(spam_delay)
            except asyncio.CancelledError: break
            except: await asyncio.sleep(2)
    if cid in spam_tasks:
        for t in spam_tasks[cid]: t.cancel()
    spam_tasks[cid] = [asyncio.create_task(image_spam_loop(bot, cid, photo_id)) for bot in bots]
    await update.message.reply_text("📸 𝐈𝐌𝐀𝐆𝐄 𝐒𝐏𝐀𝐌 𝐒𝐓𝐀𝐑𝐓𝐄𝐃!")

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚀 𝐃𝐀𝐑𝐊 MULTI-BOT LOADED!\nUse /help for commands.")

@only_sudo
async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """╔══════════════════════════════════╗
║        🔥 𝐃𝐀𝐑𝐊  •  🐱 🔥         ║
║        ✨ 𝐃𝐀𝐑𝐊 𝐁𝐎𝐓 𝐕𝟐.𝟎 ✨         ║
╚══════════════════════════════════╝

┌──╼ [ ⚡ 𝐔𝐓𝐈𝐋𝐈𝐓𝐈𝐄𝐒 ] ╾──┐
│ ⚡ /ping        ➔  𝐋𝐀𝐓𝐄𝐍𝐂𝐘
│ ⏱️ /pingms      ➔  𝐌𝐒 𝐏𝐈𝐍𝐆
│ 📊 /status      ➔  𝐒𝐓𝐀𝐓𝐒
│ 🔄 /refresh     ➔  𝐑𝐄𝐋𝐎𝐀𝐃
└──────────────────────────────┘

┌──╼ [ 🚀 𝐍𝐂 𝐌𝐎𝐃𝐄 ] ╾──┐
│ 🚀 /godspeed <TEXT>  ➔  𝐔𝐋𝐓𝐑𝐀 𝐍𝐂
│ 🛑 /stopnc           ➔  𝐒𝐓𝐎𝐏
│ ⏳ /delaync <SEC>    ➔  𝐃𝐄𝐋𝐀𝐘
│ 🧵 /threads <NUM>    ➔  𝐓𝐇𝐑𝐄𝐀𝐃𝐒
└──────────────────────────────┘

┌──╼ [ 🔮 𝐄𝐌𝐎𝐉𝐈 𝐍𝐂 ] ╾──┐
│ 🚩 /flagnc        ➔  𝐅𝐋𝐀𝐆
│ 💘 /heartnc       ➔  𝐇𝐄𝐀𝐑𝐓
│ 🎀 /aestheticnc   ➔  𝐀𝐄𝐒𝐓𝐇𝐄𝐓𝐈𝐂
│ 🥬 /vegetablenc   ➔  𝐕𝐄𝐆𝐆𝐈𝐄
│ 🐺 /animalnc      ➔  𝐀𝐍𝐈𝐌𝐀𝐋
│ ⏱️ /timenc        ➔  𝐓𝐈𝐌𝐄
│ ✨ /darkncx       ➔  𝐃𝐀𝐑𝐊𝐍𝐂𝐗
└──────────────────────────────┘

┌──╼ [ 🎨 𝐆𝐍𝐂 𝐆𝐄𝐍𝐄𝐑𝐀𝐓𝐎𝐑 ] ╾──┐
│ ✨ /gnc <TEXT>    ➔  𝟏𝟎 𝐒𝐓𝐘𝐋𝐄𝐒
└──────────────────────────────┘

┌──╼ [ 💣 𝐒𝐏𝐀𝐌 𝐙𝐎𝐍𝐄 ] ╾──┐
│ 💬 /spam <TEXT>      ➔  𝐒𝐓𝐀𝐑𝐓
│ 🛑 /unspam           ➔  𝐒𝐓𝐎𝐏
│ 🖼️ /imagespam        ➔  𝐈𝐌𝐀𝐆𝐄
│ 🎭 /stickerspam      ➔  𝐒𝐓𝐈𝐂𝐊𝐄𝐑
│ 📸 /setmphoto        ➔  𝐀𝐓𝐓𝐀𝐂𝐇
│ 🗑️ /clearmphoto      ➔  𝐂𝐋𝐄𝐀𝐑
│ ⏳ /delayspam <SEC>  ➔  𝐃𝐄𝐋𝐀𝐘
└──────────────────────────────┘

┌──╼ [ 🎮 𝐆𝐀𝐌𝐄 𝐎𝐕𝐄𝐑 ] ╾──┐
│ 💾 /Addgameover        ➔  𝐒𝐀𝐕𝐄 𝐕𝐈𝐃𝐄𝐎
│ 🎬 /Gameover          ➔  𝐒𝐅𝐍𝐃
└──────────────────────────────┘

┌──╼ [ 🎯 𝐓𝐀𝐑𝐆𝐄𝐓 𝐌𝐎𝐃𝐄 ] ╾──┐
│ 🎯 /target <NAME>            ➔  𝐒𝐓𝐀𝐓𝐒
│ 📝 /settemplate <ID> <TEXT>  ➔  𝐓𝐄𝐌𝐏
│ 📜 /showtemplate             ➔  𝐒𝐇𝐎𝐖
│ ⚔️ /spamtarget               ➔  𝐒𝐓𝐀𝐑𝐓
│ 🛑 /stoptarget               ➔  𝐒𝐓𝐎𝐏
└──────────────────────────────┘

┌──╼ [ ⚔️ 𝐒𝐖𝐈𝐏𝐄 & 𝐑𝐄𝐀𝐂𝐓 ] ╾──┐
│ ⚔️ /swipe <NAME>        ➔  𝐒𝐖𝐈𝐏𝐄
│ 🛑 /stopswipe           ➔  𝐒𝐓𝐎𝐏
│ 😍 /react <EMOJI>        ➔  𝐎𝐍
│ ❌ /stopreact           ➔  𝐎𝐅𝐅
│ 💥 /dreact <N> <EMOJI>   ➔  𝐌𝐔𝐋𝐓𝐈
│ 🚫 /stopdreact          ➔  𝐎𝐅𝐅
└──────────────────────────────┘

┌──╼ [ 🤖 𝐁𝐎𝐓 𝐒𝐄𝐓𝐓𝐈𝐍𝐆𝐒 ] ╾──┐
│ ✏️ /changename <NAME>  ➔  𝐍𝐀𝐌𝐄
│ 📷 /changepfp          ➔  𝐏𝐅𝐏
│ 🖼️ /setpfp             ➔  𝐒𝐄𝐓
│ 🤖 /getallbots         ➔  𝐁𝐎𝐓𝐒
└──────────────────────────────┘

┌──╼ [ 🌐 𝐆𝐋𝐎𝐁𝐀𝐋 𝐒𝐘𝐒𝐓𝐄𝐌 ] ╾──┐
│ 🟢 /globalactivate  ➔  𝐎𝐍
│ 🔴 /offglobal       ➔  𝐎𝐅𝐅
│ 🚪 /leaveglobal     ➔  𝐋𝐄𝐀𝐕𝐄
│ 📋 /groups          ➔  𝐆𝐑𝐎𝐔𝐏𝐒
│ 🌍 /g <CMD>         ➔  𝐄𝐗𝐄𝐂
└──────────────────────────────┘

┌──╼ [ 🔐 𝐀𝐃𝐌𝐈𝐍 & 𝐒𝐔𝐃𝐎 ] ╾──┐
│ ➕ /sudo        ➔  𝐀𝐃𝐃
│ ❌ /delsudo     ➔  𝐃𝐄𝐋
│ 📜 /listsudo    ➔  𝐋𝐈𝐒𝐓
│ ⚡ /adminbyp    ➔  𝐁𝐘𝐏𝐀𝐒𝐒
│ 👑 /giveadmin   ➔  𝐆𝐈𝐕𝐄
│ 💀 /owner       ➔  𝐎𝐖𝐍𝐄𝐑
└──────────────────────────────┘

┌──╼ [ ⛓️ 𝐒𝐋𝐀𝐕𝐄𝐒 ] ╾──┐
│ 📜 /slaves             ➔  𝐋𝐈𝐒𝐓
│ ➕ /addslave <NAME>    ➔  𝐀𝐃𝐃
│ ❌ /delslave <NAME>    ➔  𝐃𝐄𝐋
│ 🎥 /showslave <NUM>    ➔  𝐕𝐈𝐄𝐖
│ 💾 /saveslave <NUM>    ➔  𝐒𝐀𝐕𝐄
└──────────────────────────────┘

┌──╼ [ 🎨 𝐋𝐀𝐘𝐎𝐔𝐓 𝐂𝐎𝐍𝐓𝐑𝐎𝐋 ] ╾──┐
│ 🎭 /Setlayout <TEXT>  ➔  𝐂𝐔𝐒𝐓𝐎𝐌
│ 🔄 /resetlayout       ➔  𝐑𝐄𝐒𝐄𝐓
│ 🗑️ /clearhost         ➔  𝐂𝐋𝐄𝐀𝐑 𝐀𝐋𝐋 (𝐎𝐖𝐍𝐄𝐑)
└──────────────────────────────┘

┌──╼ [ 🛑 𝐌𝐀𝐒𝐓𝐄𝐑 𝐂𝐎𝐍𝐓𝐑𝐎𝐋 ] ╾──┐
│ 💀 /stop  ➔  𝐒𝐓𝐎𝐏 𝐀𝐋𝐋
│ ☠️ /akal  ➔  𝐑𝐄𝐏𝐋𝐘
└──────────────────────────────┘

╔══════════════════════════════════╗
║        ⚡ 𝐃𝐀𝐑𝐊 • 🐱 ⚡         ║
╚══════════════════════════════════╝"""
    await update.message.reply_text(help_text)

@only_sudo
async def changepfp_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚠️ Bot PFPs are best changed via BotFather.")

@only_sudo
async def stop_all_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    for d in [group_tasks, spam_tasks, pfp_tasks, swipe_tasks]:
        if cid in d:
            for t in d[cid]: t.cancel()
            del d[cid]
    await update.message.reply_text("🛑 𝐄𝐕𝐄𝐑𝐘𝐓𝐇𝐈𝐍𝐆 𝐒𝐓𝐎𝐏𝐏𝐄𝐃!")

@only_sudo
async def delaync_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global global_delay
    try:
        global_delay = float(context.args[0])
        await update.message.reply_text(f"⚡ 𝐍𝐂 𝐃𝐞𝐥𝐚𝐲: {global_delay}𝐬")
    except: await update.message.reply_text("⚠️ 𝐄𝐫𝐫𝐨𝐫.")

@only_sudo
async def delayspam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global spam_delay
    try:
        spam_delay = float(context.args[0])
        await update.message.reply_text(f"💥 𝐒𝐩𝐚𝐦 𝐃𝐞𝐥𝐚𝐲: {spam_delay}𝐬")
    except: await update.message.reply_text("⚠️ 𝐄𝐫𝐫𝐨𝐫.")

@only_sudo
async def globalactivate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global global_mode
    global_mode = True
    await update.message.reply_text("🌐 𝐆𝐋𝐎𝐁𝐀𝐋 𝐎𝐍")

@only_sudo
async def offglobal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global global_mode
    global_mode = False
    await update.message.reply_text("🌐 𝐆𝐋𝐎𝐁𝐀𝐋 𝐎𝐅𝐅")

@only_sudo
async def groups_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not os.path.exists(GROUPS_FILE): return await update.message.reply_text("⚠️ 𝐍𝐨 𝐠𝐫𝐨𝐮𝐩𝐬.")
    with open(GROUPS_FILE, "r") as f: ids = json.load(f)
    await update.message.reply_text(f"👥 𝐓𝐨𝐭𝐚𝐥 𝐌𝐨𝐧𝐢𝐭𝐨𝐫𝐞𝐝 𝐆𝐫𝐨𝐮𝐩𝐬: {len(ids)}")

@only_sudo
async def leaveglobal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    current_chat_id = update.effective_chat.id
    if not os.path.exists(GROUPS_FILE): return await update.message.reply_text("⚠️ 𝐍𝐨 𝐠𝐫𝐨𝐮𝐩𝐬.")
    with open(GROUPS_FILE, "r") as f: ids = json.load(f)
    for gid in ids:
        if str(gid) == str(current_chat_id): continue
        for b in bots:
            try: await b.leave_chat(gid)
            except: pass
    await update.message.reply_text("🌐 𝐋𝐄𝐅𝐓 𝐀𝐋𝐋 𝐆𝐂𝐬 (Except this one)!")

@only_sudo
async def global_broadcast_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global global_mode
    if not global_mode or not context.args: return
    await update.message.reply_text("🌐 𝐆𝐋𝐎𝐁𝐀𝐋 𝐄𝐗𝐄𝐂𝐔𝐓𝐄𝐃")

async def auto_replies(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_chat: return
    cid = update.effective_chat.id
    if os.path.exists(GROUPS_FILE):
        try:
            with open(GROUPS_FILE, "r") as f: groups = json.load(f)
        except: groups = []
    else: groups = []
    if cid not in groups:
        groups.append(cid)
        with open(GROUPS_FILE, "w") as f: json.dump(groups, f)
            
    if not update.message: return

    if cid in react_mode:
        emoji = react_mode[cid]
        try:
            await context.bot.set_message_reaction(chat_id=cid, message_id=update.message.message_id, reaction=[ReactionTypeEmoji(emoji)])
        except: pass

    if cid in dreact_mode:
        dreact_cfg = dreact_mode[cid]
        for b in bots[:dreact_cfg["num_bots"]]:
            try:
                await b.set_message_reaction(chat_id=cid, message_id=update.message.message_id, reaction=[ReactionTypeEmoji(random.choice(dreact_cfg["emojis"]))])
            except: pass

@only_sudo
async def godspeed_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
    group_tasks[cid] = [asyncio.create_task(god_speed_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("🔥 𝐆𝐎𝐃𝐒𝐏𝐄𝐄𝐃 𝐎𝐍!")

@only_sudo
async def stopnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
        del group_tasks[cid]
    await update.message.reply_text("🛑 𝐍𝐂 𝐒𝐓𝐎𝐏𝐏𝐄𝐃")

@only_sudo
async def spam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text, cid = " ".join(context.args) or ALL_SPAM_TEXT, update.message.chat_id
    if cid in spam_tasks:
        for t in spam_tasks[cid]: t.cancel()
    spam_tasks[cid] = [asyncio.create_task(spam_loop(bot, cid, text)) for bot in bots]
    await update.message.reply_text("💥 𝐒𝐏𝐀𝐌 𝐎𝐍!")

@only_sudo
async def unspam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if cid in spam_tasks:
        for t in spam_tasks[cid]: t.cancel()
        del spam_tasks[cid]
    await update.message.reply_text("🛑 𝐒𝐏𝐀𝐌 𝐒𝐓𝐎𝐏𝐏𝐄𝐃")

@only_sudo
async def spamtarget_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if cid not in target_names: return await update.message.reply_text("⚠️ Set target first.")
    hater = target_names[cid]
    if cid in spam_tasks:
        for t in spam_tasks[cid]: t.cancel()
    spam_tasks[cid] = [asyncio.create_task(sequence_spam_loop(bot, cid, hater)) for bot in bots]
    await update.message.reply_text(f"💥 𝐒𝐄𝐐𝐔𝐄𝐍𝐂𝐄 𝐒𝐓𝐀𝐑𝐓𝐄𝐃: {hater}")

@only_sudo
async def stoptarget_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    cid = update.message.chat_id
    if cid in spam_tasks:
        for t in spam_tasks[cid]: t.cancel()
        del spam_tasks[cid]
    await update.message.reply_text("🛑 𝐓𝐀𝐑𝐆𝐄𝐓 𝐒𝐓𝐎𝐏𝐏𝐄𝐃")

@only_sudo
async def targetspm_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    target_names[update.message.chat_id] = " ".join(context.args)
    await update.message.reply_text(f"🎯 𝐓𝐚𝐫𝐠𝐞𝐭: {target_names[update.message.chat_id]}")

@only_sudo
async def settemplate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        idx, txt = int(context.args[0])-1, " ".join(context.args[1:])
        SPAM_TEMPLATE[idx] = txt
        await update.message.reply_text(f"✅ Template {idx+1} set.")
    except: pass

@only_sudo
async def showtemplate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("\n\n".join(SPAM_TEMPLATE))

@only_sudo
async def threads_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_threads
    try:
        val = int(context.args[0])
        if 1 <= val <= MAX_THREADS:
            current_threads = val
            await update.message.reply_text(f"✅ 𝐓𝐡𝐫𝐞𝐚𝐝𝐬 𝐬𝐞𝐭 𝐭𝐨: {current_threads}")
    except: await update.message.reply_text("⚠️ 𝐔𝐬𝐚𝐠𝐞: /threads <number>")

@only_sudo
async def getallbots_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not bot_usernames: return await update.message.reply_text("⚠️ Bots not loaded.")
    await update.message.reply_text("🤖 𝐀𝐋𝐋 𝐁𝐎𝐓𝐒:\n\n" + "\n".join([f"@{u}" for u in bot_usernames]))

@only_sudo
async def giveadmin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👑 Giveadmin executed.")

async def add_sudo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or update.effective_user.id not in OWNER_IDS: return
    if not update.message.reply_to_message: return await update.message.reply_text("⚠️ Reply to a user.")
    user = update.message.reply_to_message.from_user
    SUDO_USERS.add(user.id)
    sudo_usernames[str(user.id)] = user.username or user.first_name
    save_sudo()
    await update.message.reply_text(f"✅ User @{user.username} is now Sudo!")

@only_sudo
async def list_sudo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🛡️ 𝐒𝐔𝐃𝐎 𝐔𝐒𝐄𝐑𝐒:\n\n"
    for uid in SUDO_USERS:
        text += f"• {sudo_usernames.get(str(uid), 'User')}\n"
    await update.message.reply_text(text)

@only_sudo
async def del_sudo_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    try:
        uid = int(context.args[0])
        if uid in SUDO_USERS and uid not in OWNER_IDS:
            SUDO_USERS.remove(uid)
            save_sudo()
            await update.message.reply_text("✅ Removed from Sudo.")
    except: pass

@only_sudo
async def owner_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("𝐎ᴡɴᴇʀ 𝐃ᴀʀᴋ 𝐇ᴀɪ 𝐁ᴀʙᴜ")

@only_sudo
async def akal_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message: return
    await update.message.reply_text("🚨 𝐓𝐄𝐑𝐈 𝐀𝐊𝐀𝐋 𝐓𝐇𝐈𝐊𝐀𝐍𝐄 𝐋𝐀𝐆𝐀 𝐃𝐔𝐍𝐆𝐀!", reply_to_message_id=update.message.reply_to_message.message_id)

@only_sudo
async def flagnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
    async def flag_loop(bot, c, b):
        while True:
            try:
                await bot.set_chat_title(c, title=f"{b} {random.choice(FLAGNC_EMOJIS)}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: asyncio.sleep(1)
    group_tasks[cid] = [asyncio.create_task(flag_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("🇮🇳 𝐅𝐋𝐀𝐆𝐍𝐂 𝐎𝐍!")

@only_sudo
async def heartnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
    async def heart_loop(bot, c, b):
        while True:
            try:
                await bot.set_chat_title(c, title=f"{b} {random.choice(HEARTNC_EMOJIS)}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: asyncio.sleep(1)
    group_tasks[cid] = [asyncio.create_task(heart_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("❤️ 𝐇𝐄𝐀𝐑𝐓𝐍𝐂 𝐎𝐍!")

@only_sudo
async def aestheticnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
    async def aesthetic_loop(bot, c, b):
        while True:
            try:
                await bot.set_chat_title(c, title=f"{b} ⋆.𐙚 {random.choice(AESTHETICNC_EMOJIS)}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: asyncio.sleep(1)
    group_tasks[cid] = [asyncio.create_task(aesthetic_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("🌸 𝐀𝐄𝐒𝐓𝐇𝐄𝐓𝐈𝐂𝐍𝐂 𝐎𝐍!")

@only_sudo
async def vegetablenc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
    async def veg_loop(bot, c, b):
        while True:
            try:
                await bot.set_chat_title(c, title=f"{b} {random.choice(VEGETABLENC_EMOJIS)}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: asyncio.sleep(1)
    group_tasks[cid] = [asyncio.create_task(veg_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("🥬 𝐕𝐄𝐆𝐄𝐓𝐀𝐁𝐋𝐄𝐍𝐂 𝐎𝐍!")

@only_sudo
async def animalnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
    async def animal_loop(bot, c, b):
        while True:
            try:
                await bot.set_chat_title(c, title=f"{b} {random.choice(ANIMALNC_EMOJIS)}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: asyncio.sleep(1)
    group_tasks[cid] = [asyncio.create_task(animal_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("🐶 𝐀𝐍𝐈𝐌𝐀𝐋𝐍𝐂 𝐎𝐍!")

@only_sudo
async def stickerspam_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message or not update.message.reply_to_message.sticker: return
    cid, sid = update.message.chat_id, update.message.reply_to_message.sticker.file_id
    async def sticker_loop(bot, c, s):
        while True:
            try:
                await bot.send_sticker(c, s)
                await asyncio.sleep(spam_delay)
            except asyncio.CancelledError: break
            except: asyncio.sleep(1)
    spam_tasks[cid] = [asyncio.create_task(sticker_loop(bot, cid, sid)) for bot in bots]
    await update.message.reply_text("🎭 𝐒𝐓𝐈𝐂𝐊𝐄𝐑 𝐒𝐏𝐀𝐌 𝐎𝐍!")

@only_sudo
async def timenc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args) or "Test", update.message.chat_id
    async def time_loop(bot, c, b):
        while True:
            try:
                now = time.strftime("%S:%M:%H")
                await bot.set_chat_title(c, title=f"{b}╰┈➤{now}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: asyncio.sleep(1)
    group_tasks[cid] = [asyncio.create_task(time_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("⏰ 𝐓𝐈𝐌𝐄𝐍𝐂 𝐎𝐍!")

@only_sudo
async def darkncx_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    base, cid = " ".join(context.args or []) or ALL_NC_TEXT, update.message.chat_id
    if cid in group_tasks:
        for t in group_tasks[cid]: t.cancel()
    async def darkncx_loop(bot, c, b):
        while True:
            try:
                pre = random.choice(GNC_PREFIXES)
                suf = random.choice(GNC_SUFFIXES)
                await bot.set_chat_title(c, title=f"{pre} {b} {suf}")
                await asyncio.sleep(global_delay)
            except asyncio.CancelledError: break
            except: asyncio.sleep(1)
    group_tasks[cid] = [asyncio.create_task(darkncx_loop(bot, cid, base)) for bot in bots]
    await update.message.reply_text("✨ 𝐃𝐀𝐑𝐊𝐍𝐂𝐗 𝐎𝐍!")

async def adminbyp_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Adminbyp executed.")

@only_sudo
async def slaves_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⛓️ SLAVES LIST")

@only_sudo
async def addslave_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⛓️ Slave added.")

@only_sudo
async def delslave_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🗑️ Slave removed.")

@only_sudo
async def showslave_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

@only_sudo
async def saveslave_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

@only_sudo
async def gnc_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    text = " ".join(context.args)
    uid = update.effective_user.id
    gnc_cache[uid] = text
    await update.message.reply_text(_gnc_format(text, "darkncx"), reply_markup=_gnc_keyboard(uid))

async def gnc_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    parts = query.data.split("_", 2)
    if len(parts) < 3 or uid != int(parts[1]):
        return await query.answer("❌ Not yours!", show_alert=True)
    style_key = parts[2]
    text = gnc_cache.get(uid, "Sample")
    await query.edit_message_text(_gnc_format(text, style_key), reply_markup=_gnc_keyboard(uid))
    await query.answer("✅ Updated")

async def ping_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("I'M ON MAN WHAT YOU NEED ?")

async def pingms_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time = time.time()
    msg = await update.message.reply_text("Calculating latency...")
    latency_ms = round((time.time() - start_time) * 1000, 2)
    await msg.edit_text(f"⚡ **DARK System Latency:** `{latency_ms} ms`")

async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 BOT STATUS: RUNNING 24/7 ✅")

async def dreact_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args: return
    dreact_mode[update.effective_chat.id] = {"emojis": context.args[1:], "num_bots": int(context.args[0])}
    await update.message.reply_text("✅ Auto React ON")

async def stopdreact_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dreact_mode.pop(update.effective_chat.id, None)
    await update.message.reply_text("🛑 Auto React Stopped")

async def welcome_new_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

@only_sudo
async def setwelcomephoto_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

@only_sudo
async def clearwelcomephoto_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

@only_sudo
async def setmphoto_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

@only_sudo
async def refresh_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔄 Refreshed!")

@only_sudo
async def setlayout_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

@only_sudo
async def resetlayout_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

@only_sudo
async def clearmphoto_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def owner_host_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

async def clear_host_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    pass

def build_app(token, is_leader=False):
    app = Application.builder().token(token).build()
    
    handlers = [
        CommandHandler("start", start_cmd), CommandHandler("help", help_cmd),
        CommandHandler("ping", ping_command), CommandHandler("pingms", pingms_command),
        CommandHandler("status", status_cmd),
        CommandHandler("dreact", dreact_cmd), CommandHandler("stopdreact", stopdreact_cmd),
        CommandHandler("godspeed", godspeed_cmd), CommandHandler("stopnc", stopnc_cmd),
        CommandHandler("spam", spam_cmd), CommandHandler("unspam", unspam_cmd),
        CommandHandler("imagespam", imagespam_cmd),
        CommandHandler("Addgameover", addgameover_cmd),
        CommandHandler("Gameover", gameover_cmd),
        CommandHandler("swipe", swipe_cmd), CommandHandler("stopswipe", stopswipe_cmd),
        CommandHandler("react", react_cmd), CommandHandler("Stopreact", stopreact_cmd),
        CommandHandler("Changename", changename_cmd), CommandHandler("Setpfp", setpfp_cmd),
        CommandHandler("changepfp", changepfp_cmd), CommandHandler("stop", stop_all_cmd),
        CommandHandler("delaync", delaync_cmd), CommandHandler("delayspam", delayspam_cmd),
        CommandHandler("globalactivate", globalactivate_cmd), CommandHandler("offglobal", offglobal_cmd),
        CommandHandler("groups", groups_cmd), CommandHandler("leaveglobal", leaveglobal_cmd),
        CommandHandler("g", global_broadcast_cmd), CommandHandler("target", targetspm_cmd),
        CommandHandler("settemplate", settemplate_cmd), CommandHandler("spamtarget", spamtarget_cmd),
        CommandHandler("stoptarget", stoptarget_cmd), CommandHandler("showtemplate", showtemplate_cmd),
        CommandHandler("akal", akal_cmd),
        CommandHandler("flagnc", flagnc_cmd), CommandHandler("heartnc", heartnc_cmd),
        CommandHandler("aestheticnc", aestheticnc_cmd), CommandHandler("vegetablenc", vegetablenc_cmd),
        CommandHandler("animalnc", animalnc_cmd), CommandHandler("stickerspam", stickerspam_cmd),
        CommandHandler("timenc", timenc_cmd), CommandHandler("darkncx", darkncx_cmd),
        CommandHandler("threads", threads_cmd), CommandHandler("getallbots", getallbots_cmd),
        CommandHandler("giveadmin", giveadmin_cmd), CommandHandler("adminbyp", adminbyp_cmd),
        CommandHandler("sudo", add_sudo_cmd), CommandHandler("listsudo", list_sudo_cmd),
        CommandHandler("delsudo", del_sudo_cmd), CommandHandler("owner", owner_cmd),
        CommandHandler("slaves", slaves_cmd), CommandHandler("addslave", addslave_cmd),
        CommandHandler("delslave", delslave_cmd), CommandHandler("showslave", showslave_cmd),
        CommandHandler("saveslave", saveslave_cmd),
        CommandHandler("gnc", gnc_cmd),
        CommandHandler("setmphoto", setmphoto_cmd), CommandHandler("clearmphoto", clearmphoto_cmd),
        CommandHandler("setwelcomephoto", setwelcomephoto_cmd), CommandHandler("clearwelcomephoto", clearwelcomephoto_cmd),
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome_new_members),
        CommandHandler("refresh", refresh_cmd),
        CommandHandler("clearhost", clear_host_cmd),
        CallbackQueryHandler(gnc_callback, pattern="^gnc_"),
        MessageHandler(filters.TEXT & ~filters.COMMAND, auto_replies)
    ]
    
    if is_leader:
        for h in handlers:
            app.add_handler(h)
    else:
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_replies))

    return app

bots = [Application.builder().token(t).build().bot for t in TOKENS]

async def run_bots():
    load_data()
    load_slaves()
    load_gameover_videos()
    global bot_usernames
    bot_usernames = []
    
    print("🔄 Initializing bots...", flush=True)
    apps = []
    for i, t in enumerate(TOKENS):
        is_leader = (i == 0)
        apps.append((build_app(t, is_leader=is_leader), t, is_leader))

    async def start_single_bot(app, token, is_leader):
        try:
            await app.initialize()
            await app.start()
            await app.updater.start_polling()
            me = await app.bot.get_me()
            bot_usernames.append(me.username)
            role = "LEADER 👑" if is_leader else "SLAVE 🤖"
            print(f"✅ Bot (@{me.username}) online as [{role}]!", flush=True)
        except Exception as e:
            print(f"❌ Failed to start bot: {e}", flush=True)

    await asyncio.gather(*(start_single_bot(app, t, leader) for app, t, leader in apps))

    print("🚀 ALL BOTS RUNNING WITH LEADER CONFIG!", flush=True)
    while True: 
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(run_bots())
