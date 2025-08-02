import logging, random, requests, json, os, re, asyncio, aiohttp, sys
from java_ques.java_responses import get_available_java_topics
from java_ques.java_responses import java_answers
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from java_ques.java_responses import handle_java_question
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters, CallbackContext
from bs4 import BeautifulSoup
from html import escape  
from telegram.ext import InlineQueryHandler
from re import IGNORECASE
from notes_bookmarks import handle_bookmark_folders
from notes_bookmarks import show_bookmarks_in_folder
from notes_bookmarks import handle_mynotes, handle_note_read
from notes_bookmarks import get_all_folders_from_file
from notes_bookmarks import (
    save_note, read_note, list_notes, handle_mynotes, delete_note, edit_note,
    rename_note, send_bullet_template,
    save_bookmark, show_bookmarks, delete_bookmark, edit_bookmark,
    export_bookmarks, export_category
)
from urllib.parse import urlparse
from keep_alive import keep_alive
from dotenv import load_dotenv
keep_alive.keep_alive()  # runs server in background


load_dotenv()
BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
CLIENT_ID = os.getenv("JD_CLIENT_ID")
CLIENT_SECRET = os.getenv("JD_CLIENT_SECRET")

# Step 1️⃣: Install Python (if not already installed) → https://www.python.org/downloads

# Step 2️⃣: Open Terminal or Command Prompt and navigate to your bot folder or go to your bot file and type cmd at top near > symbols after opening the bo main folder

# Step 4️⃣: Upgrade pip (just good practice):
# pip install --upgrade pip

# Step 5️⃣: After downloading your bot on a new device, run this in terminal to install dependencies:
# pip install python-telegram-bot

# Step 6️⃣: (Optional) If you used other packages like `python-dotenv` or `requests`, install those too:
# pip install python-dotenv requests

# Step 7️⃣: Run the bot!
# python bot.py                 # Or whatever your main script is

# === Logging Setup ===
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s | %(asctime)s | %(message)s",
    datefmt="%H:%M:%S"
)

VIDEO_DB = "video_links.json"

def load_video_links():
    if not os.path.exists(VIDEO_DB):
        with open(VIDEO_DB, "w") as f:
            json.dump({}, f)
        return {}
    with open(VIDEO_DB, "r") as f:
        return json.load(f)

def save_video_links(data):
    with open(VIDEO_DB, "w") as f:
        json.dump(data, f, indent=2)

def is_youtube_link(text):
    # Accepts YouTube URLs even with timestamps, query params, etc.
    pattern = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/[^\s]+"
    return bool(re.search(pattern, text))

def is_playlist_link(url):
    return "playlist?list=" in url or "list=" in url

NOTES_FILE = "notes.json"
BOOKMARKS_FILE = "bookmarks.json"

# === Async URL Title Fetcher ===
async def fetch_title_from_url(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                html = await resp.text()
        soup = BeautifulSoup(html, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else "No Title"
        return title
    except Exception:
        return "Untitled Link"

# === Smart Edit Helper (Safe & Robust) ===
async def safe_edit(query=None, text="", update=None, **kwargs):
    try:
        # If callback query has a valid message, edit it
        if query and query.message:
            await query.edit_message_text(text, **kwargs)
        # If query has no message but came from user (e.g. inline), reply instead
        elif query:
            await query.message.reply_text(text, **kwargs) if query.message else await query.from_user.send_message(text, **kwargs)
        # Fallback to reply via update object
        elif update and update.message:
            await update.message.reply_text(text, **kwargs)
        else:
            logging.warning("[⚠️] safe_edit() has no valid target to send to.")
    except Exception as e:
        logging.error(f"[❌] safe_edit() failed: {e}")

# === Bot Credentials ===
TELEGRAM_BOT_TOKEN = "7897147389:AAH7eUfVldPGTfbGfQjKVkf3dRN9ja7GJq8"
JD_CLIENT_ID = "10805f05f923ff4344eb61277a1c2030"
JD_CLIENT_SECRET = "3e11847dd420b77920e5cf19d3b7dfe114bf077eaf8441c2e2831caff977afde"

# === Game & Quiz Data ===
guess_data = {}
scramble_sessions = {}
emoji_sessions = {}
gk_sessions = {}

scramble_words = {
    "python": "Programming language",
    "telegram": "Messaging app",
    "india": "Country in Asia",
    "browser": "Used to surf the internet",
    "keyboard": "Typing device",
    "oxygen": "We need this to breathe",
    "teacher": "One who educates",
    "capital": "Main city of a country",
    "cookie": "Stored browser info or a snack 😋",
    "mirror": "Reflects your face",
    "microscope": "Used to view tiny objects",
    "photosynthesis": "Process plants use to make food",
}

emoji_quiz = {
    "🎬🐟🧠": "Finding Nemo",
    "🕷️🧔‍♂️🗽": "Spider Man",
    "👸❄️⛄": "Frozen",
    "🧑‍🚀🌌👨‍🚀": "Interstellar",
    "🧙‍♂️⚡🏰": "Harry Potter",
    "🦖🌴🚁": "Jurassic Park",
    "💀🏴‍☠️⛵": "Pirates of the Caribbean",
    "🚢🧊💔": "Titanic",
    "🏎️💨🔥": "Fast and Furious",
    "👑🪓⚔️": "Game of Thrones",
    "🧔📦💰": "Breaking Bad",
    "👨‍👩‍👧‍👦🏠💀": "Stranger Things",
}

gk_questions = [
    {
        "question": "Which is the smallest continent by land area?",
        "options": ["A) Africa", "B) Australia", "C) Europe", "D) Antarctica"],
        "answer": "B"
    },
    {
        "question": "Which Indian city is known as the 'Pink City'?",
        "options": ["A) Jaipur", "B) Udaipur", "C) Jodhpur", "D) Bhopal"],
        "answer": "A"
    },
    {
        "question": "What planet is known as the 'Morning Star'?",
        "options": ["A) Venus", "B) Mars", "C) Jupiter", "D) Mercury"],
        "answer": "A"
    },
    {
        "question": "Who invented the lightbulb?",
        "options": ["A) Isaac Newton", "B) Nikola Tesla", "C) Thomas Edison", "D) Albert Einstein"],
        "answer": "C"
    },
    {
        "question": "Which country gifted the Statue of Liberty to the USA?",
        "options": ["A) France", "B) England", "C) Italy", "D) Germany"],
        "answer": "A"
    },
    {
        "question": "What is the capital of Canada?",
        "options": ["A) Toronto", "B) Montreal", "C) Ottawa", "D) Vancouver"],
        "answer": "C"
    },
    {
        "question": "How many players are there in a cricket team (on field)?",
        "options": ["A) 10", "B) 11", "C) 12", "D) 9"],
        "answer": "B"
    },
    {
        "question": "Who was the first President of India?",
        "options": ["A) Rajendra Prasad", "B) S. Radhakrishnan", "C) Jawaharlal Nehru", "D) A.P.J. Abdul Kalam"],
        "answer": "A"
    },
    {
        "question": "What is the chemical formula for water?",
        "options": ["A) CO₂", "B) H₂O", "C) O₂", "D) NH₃"],
        "answer": "B"
    },
    {
        "question": "Which is the longest river in the world?",
        "options": ["A) Amazon", "B) Yangtze", "C) Nile", "D) Mississippi"],
        "answer": "C"
    },
    {
        "question": "Which organ purifies blood in the human body?",
        "options": ["A) Heart", "B) Lungs", "C) Kidney", "D) Liver"],
        "answer": "C"
    },
    {
        "question": "Which gas is most abundant in Earth's atmosphere?",
        "options": ["A) Oxygen", "B) Carbon Dioxide", "C) Nitrogen", "D) Hydrogen"],
        "answer": "C"
    },
    {
        "question": "Who wrote the Indian National Anthem?",
        "options": ["A) Rabindranath Tagore", "B) Bankim Chandra Chatterjee", "C) Aurobindo Ghosh", "D) Subhash Chandra Bose"],
        "answer": "A"
    },
    {
        "question": "Which is the hardest natural substance on Earth?",
        "options": ["A) Iron", "B) Diamond", "C) Quartz", "D) Graphite"],
        "answer": "B"
    },
    {
        "question": "How many bones does an adult human have?",
        "options": ["A) 212", "B) 206", "C) 201", "D) 208"],
        "answer": "B"
    },
    {
        "question": "Which city hosted the 2020 Summer Olympics?",
        "options": ["A) Tokyo", "B) Beijing", "C) Rio de Janeiro", "D) Paris"],
        "answer": "A"
    },
    {
        "question": "Who is known as the 'Missile Man of India'?",
        "options": ["A) Rakesh Sharma", "B) Homi Bhabha", "C) A.P.J. Abdul Kalam", "D) Vikram Sarabhai"],
        "answer": "C"
    },
    {
        "question": "In which year did India gain independence?",
        "options": ["A) 1945", "B) 1946", "C) 1947", "D) 1950"],
        "answer": "C"
    },
    {
        "question": "What is the capital of Sri Lanka?",
        "options": ["A) Colombo", "B) Kandy", "C) Jaffna", "D) Galle"],
        "answer": "A"
    }
]

# === Error Handler ===
async def error_handler(update, context):
    print(f"[🛑 ERROR]: {context.error}")

# === Start & Menu ===
THEMES = {
    "default": {
        "title": "Main Menu",
        "labels": {
            "games": "🎮 Fun Zone",
            "run": "💻 Run Code",
            "notes": "📝 Notes",
            "bookmarks": "🔖 Bookmarks",
            "settings": "⚙️ Settings"
        }
    },
    "dark": {
        "emoji": "🌒",
        "title": "Dark Mode",
        "labels": {
            "games": "🕶 GAMES",
            "run": "👨‍💻 RUN",
            "notes": "📓 NOTES",
            "bookmarks": "📍 BOOKMARKS",
            "settings": "⚙️ SETTINGS"
        }
    },
    "emoji": {
        "emoji_pool": ["😎", "🎉", "🔥", "🤩", "✨", "🎊", "💫", "🥳"],
        "title": "🎊 Emoji Fiesta",
        "labels": {
            "games": "🎮 Fun Zone",
            "run": "🤖 Code Lab",
            "notes": "📒 My Notes",
            "bookmarks": "📌 Bookmarks",
            "settings": "🛠 Settings"
        }
    }
}

async def handle_unknown_callbacks(update, context):
    data = update.callback_query.data
    print(f"🔍 [DEBUG] Unhandled callback: {data}")
    await update.callback_query.answer("Not sure what to do with that.")

async def start(update, context):
    logging.info(f"[START] User {update.effective_user.id} launched /start")
    await update.message.reply_text("👋 Welcome! Type /menu to explore the bot.")

async def show_inline_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    logging.info(f"[MENU] {uid} opened main menu")

    # Get theme and style
    theme = context.user_data.get("theme", "default")
    style = THEMES.get(theme, THEMES["default"])

    # Emoji setup
    emoji = style.get("emoji", "")
    if "emoji_pool" in style:
        emoji = random.choice(style["emoji_pool"])

    # Grab label set
    labels = style.get("labels", {})

    # 💪 Bulletproof label helper
    def label(key, fallback):
        val = labels.get(key)
        return val if isinstance(val, str) and val.strip() else f"{emoji} {fallback}"

    # 🔘 Inline Keyboard
    kb = [
        [
            InlineKeyboardButton(labels.get("games", f"{emoji} 🎮 Fun Zone"), callback_data="menu_games"),
            InlineKeyboardButton(labels.get("run", f"{emoji} 💻 Run Code"), callback_data="menu_run")
        ],
        [
            InlineKeyboardButton(labels.get("notes", f"{emoji} 📝 Notes"), callback_data="menu_notes"),
            InlineKeyboardButton(labels.get("bookmarks", f"{emoji} 🔖 Bookmarks"), callback_data="menu_bookmarks")
        ],
        [
            InlineKeyboardButton(labels.get("Handwritten Notes", f"{emoji} 📒 Resources"), callback_data="show_notes_menu"),
            InlineKeyboardButton(labels.get("videos", f"{emoji} 🎥 Youtube Videos"), callback_data="show_video_menu")
        ],
        [
            InlineKeyboardButton(labels.get("inline", f"{emoji} 🤖 Inline Bots"), callback_data="inline_bots_guide"),
            InlineKeyboardButton(labels.get("settings", f"{emoji} ⚙️ Settings"), callback_data="menu_settings")
       ]
    ]

    msg = f"{emoji or ''} *{style.get('title', '📋 Menu')}*\n📋 Choose an option:"
    markup = InlineKeyboardMarkup(kb)

    if update.callback_query:
        await update.callback_query.edit_message_text(msg, parse_mode="Markdown", reply_markup=markup)
    else:
        await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=markup)

async def handle_menu_selection(update, context):
    query = update.callback_query
    if not query:
        print("[❌] No callback_query received!")
        return

    await query.answer()
    data = query.data
    logging.info(f"[CALLBACK] {query.from_user.id} selected: {data}")

    if data == "menu_games":
        kb = [
            [InlineKeyboardButton("🔀 Word Scramble", callback_data="scramble_from_menu")],
            [InlineKeyboardButton("🎬 Emoji Quiz", callback_data="emoji_from_menu")],
            [InlineKeyboardButton("🎲 Guess the Number", callback_data="guess_from_menu")],
            [InlineKeyboardButton("🧠 Take a Quiz", callback_data="quiz_gk_from_menu")], # ✅ Moved quiz into Fun Zone
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
        ]
        await safe_edit(query, "🎮 *Welcome to the Fun Zone!*\nPick your challenge:", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_theme":
        kb = [
            [InlineKeyboardButton("🌑 Dark", callback_data="set_theme_dark"),
             InlineKeyboardButton("😎 Emoji", callback_data="set_theme_emoji")],
            [InlineKeyboardButton("🔄 Default", callback_data="set_theme_default")],
            [InlineKeyboardButton("🔙 Back to Settings", callback_data="menu_settings")]
        ]
        await safe_edit(query, "🎨 *Choose Your Theme:*", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data.startswith("set_theme_"):
        await handle_theme_selection(data, context, query, update)

    elif data == "inline_bots_guide":
        await query.message.reply_text(
            "🤖 *Inline Bots That Work Instantly!*\n\n"
            "`@gif <search>` – Find and send GIFs\n"
            "`@memingbot` – Create memes inline\n"
            "`@vid <topic>` – YouTube videos\n"
            "`@bing <query>` – Instant web results\n"
            "`@wiki <topic>` – Wikipedia summaries\n"
            "`@imdb <movie>` – Movie info fast\n"
            "`@bold <text>` – Format messages\n"
            "`@gamee` – Play games with friends\n"
            "`@sticker <emoji>` – Find stickers\n"
            "`@spotifybot` – Search Spotify tracks\n"
            "`@pic <search>` – Search images\n"
            "`@qrbot <enter something>` – Generate QR codes instantly\n"
            "`@calcubot` – Console-style calculator with inline support\n"
            "`@youtube <topic>` – YouTube search\n"
            "💡 Just type these in *any chat*, no bot install needed!",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Back to Menu", callback_data="menu_root")]
            ])
        )

    elif data == "menu_settings":
        kb = [
            [InlineKeyboardButton("🎨 Theme", callback_data="menu_theme")],
            [InlineKeyboardButton("🔙 Back to Main Menu", callback_data="menu_root")]
        ]
        await safe_edit(query, "⚙️ *Settings Menu*", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == "show_notes_menu":
        notes_folder = "notes_handwritten"
        files = sorted(os.listdir(notes_folder))
        
        if not files:
            await query.edit_message_text("📂 No handwritten notes uploaded yet.")
            return

        context.user_data["note_messages"] = []
        await query.edit_message_text("📝 Notes loaded. Choose a file below 👇")

        for f in files:
            if not f.lower().endswith(".pdf"):
                continue

            sent = await query.message.chat.send_message(
                f"📘 *{f}*",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("📥 Download", callback_data=f"download_note::{f}"),
                        InlineKeyboardButton("✏️ Rename", callback_data=f"rename_note::{f}"),
                        InlineKeyboardButton("🗑️ Delete", callback_data=f"delete_note::{f}")
                    ]
                ])
            )
            context.user_data["note_messages"].append(sent.message_id)

        await query.message.chat.send_message(
            "⬇️ Done reviewing your notes?",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
            ])
        )

    elif query.data.startswith("download_note::"):
        filename = query.data.split("::")[1]
        filepath = os.path.join("notes_handwritten", filename)
        await query.message.reply_document(document=open(filepath, "rb"), filename=filename)

    elif query.data.startswith("rename_note::"):
        filename = query.data.split("::")[1]
        context.user_data["rename_target"] = filename
        await query.edit_message_text(f"✏️ Send me the *new name* for `{filename}` (without `.pdf`):", parse_mode="Markdown")

    elif query.data.startswith("delete_note::"):
        filename = query.data.split("::")[1]
        filepath = os.path.join("notes_handwritten", filename)
        
        if os.path.exists(filepath):
            os.remove(filepath)
            await query.edit_message_text(f"🗑️ `{filename}` deleted successfully.", parse_mode="Markdown")
        else:
            await query.edit_message_text("⚠️ File not found.")

    elif data == "menu_run":
        kb = [[InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]]
        await safe_edit(
            query,
            "💻 *Code Playground Guide:*\n\n"
            "Use the `/run` command to execute code.\n Just type the language after `/run`, then add your code below.\n\n"
            "Use the `/javahelp` command - To See the List of Saved Java Programs.\n"
            "Use `/java pattern` command - To See all Pattern related Program\n"
            "Use `/java recursion` command - To See all Recursion related Programs\n"
            "Use `/java sort` command - To See all Sorting Problems\n\n"
            "*Python:*\n"
            "`/run python3`\n"
            "`print('Hi')`\n\n"
            "*Java:*\n"
            "`/run java`\n"
            "`public class Main {`\n"
            "`    public static void main(String[] args) {`\n"
            "`        System.out.println(\"Hello Java\");`\n"
            "`    }`\n"
            "`}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb)
        )

    elif data == "menu_notes":
        kb = [
            [InlineKeyboardButton("➕ Add Note", callback_data="note_how")],
            [InlineKeyboardButton("🗒️ View Notes", callback_data="mynotes")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
        ]
        await safe_edit(query, "📝 Notes Menu:", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "note_how":
        kb = [
            [InlineKeyboardButton("🔙 Back to Notes Menu", callback_data="menu_notes")]
        ]
        await safe_edit(query,
            "📓 *How to Use Notes*\n\n"
            "*➕ Add a note:*\n"
            "`/note Title\\nContent`\n\n"
            "*📖 Read:* `/read Title`\n"
            "*🗑️ Delete:* `/delete Title`\n"
            "*📋 List:* `/mynotes`\n"
            "*✏️ Edit:* `/edit Old Title\\nNew Content`\n"
            "*🔄 Rename:* `/rename Old Title\\nNew Title`\n\n"
            "*✨ Formatting Tips:*\n"
            "• Bold → `<b>text</b>`\n"
            "• Italic → `<i>text</i>`\n"
            "• Underline → `<u>text</u>`\n"
            "• Bullet → just copy this: `•`\n"
            "• Line breaks → hit Enter (don't use `<br>`, it breaks Telegram!)\n\n"
            "💡 _Bullet shortcut: press Alt + 7 (on numpad)_\n"
            "🔍 _To see a real example of note formatting with bullets, try the command:_ `/bullets`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb)
        )

    elif data.startswith("note_edit:"):
        title = data.split("note_edit:", 1)[1]
        await query.message.edit_text(
            f"✏️ Send new content for *{title}* using:\n`/edit {title}\\nNew content`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Your Notes", callback_data="mynotes")]
                ])
            )

    elif data.startswith("note_delete:"):
        title = data.split("note_delete:", 1)[1]
        await query.message.edit_text(
            f"⚠️ Are you sure you want to delete *{title}*?\n\nUse:\n`/delete {title}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Your Notes", callback_data="mynotes")]
                ])
            )

    elif data == "menu_bookmarks":
        
        user_id = str(update.effective_user.id)
        folders = get_all_folders_from_file(user_id=user_id)

        folder_buttons = [
            [InlineKeyboardButton(f"📁 {folder.title()}", callback_data=f"bk_folder:{folder}")]
            for folder in folders
        ]

        kb = [
            [InlineKeyboardButton("📝 How to Add", callback_data="bk_add_guide")],
            [InlineKeyboardButton("🧹 Edit/Delete/Export", callback_data="bk_view_guide")]
            ] + folder_buttons + [
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
        ]

        await safe_edit(query, "🔖 *Your Bookmarks Menu:*", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "bk_add_guide":
        kb = [[InlineKeyboardButton("🔙 Back to Bookmarks Menu", callback_data="menu_bookmarks")]]
        await safe_edit(query,
            "To add a bookmark, send:\n\n"
            "`/bookmark Google\\nhttps://google.com`\n"
            "`/bookmark Link ` - Also Valid if there is no Title\n" 
            "`/bookmark Folder\\nTitle\\nLink` - To Save the Bookmark in the Folder\n\n"
            "*Other Commands:*\n"
            "`/mybookmarks` – View saved links\n"
            "`/editbookmark 1\\nNew Title\\nhttps://new-url.com`\n"
            "`/deletebookmark 1` – Remove by index",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb)
            )
    
    elif data == "bk_view_guide":
        kb = [[InlineKeyboardButton("🔙 Back to Bookmarks Menu", callback_data="menu_bookmarks")]]
        await safe_edit(query,
            "🔎 *Viewing & Editing & Exporting Bookmarks:*\n\n"
            "`/mybookmarks` – List all bookmarks with indexes\n"
            "`/editbookmark 2\\nNew Title\\nhttps://...`\n"
            "`/deletebookmark 2` – Remove entry\n\n"
            "`/exportbookmarks` – Export all saved bookmarks\n"
            "`/exportcategory` – Export bookmarks grouped by category\n\n"
            "Example:\n`/editbookmark 1\\nGoogle Docs\\nhttps://docs.google.com`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup(kb)
        )
        
    elif data == "scramble_from_menu":
        query = update.callback_query
        chat_id = query.from_user.id
        # Simulate /scramble command visibly in chat
        await context.bot.send_message(chat_id=chat_id, text="/scramble")
        
    elif data == "game_scramble":
        query = update.callback_query
        chat_id = query.from_user.id

        word, clue = random.choice(list(scramble_words.items()))
        scrambled = ''.join(random.sample(word, len(word)))
        scramble_sessions[chat_id] = word

        msg = f"🔀 `{scrambled}`\n💡 Clue: {clue}"
        kb = [
            [InlineKeyboardButton("🔁 Try Another", callback_data="game_scramble")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
        ]

        await safe_edit(query, msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    elif data == "guess_from_menu":
        query = update.callback_query
        chat_id = query.from_user.id
        await context.bot.send_message(chat_id=chat_id, text="/guess_the_number")
        
    elif data == "game_guess":
        query = update.callback_query
        chat_id = query.from_user.id

        guess_data[chat_id] = random.randint(1, 100)

        msg = "🎯 I picked a number between 1 and 100. What's your guess?"
        kb = [
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
        ]
        await safe_edit(query, msg, reply_markup=InlineKeyboardMarkup(kb))

    elif data == "emoji_from_menu":
        query = update.callback_query
        chat_id = query.from_user.id
        await context.bot.send_message(chat_id=chat_id, text="/emoji")
        
    elif data == "game_emoji":
        query = update.callback_query
        cid = query.from_user.id

        emoji, answer = random.choice(list(emoji_quiz.items()))
        emoji_sessions[cid] = {
            "emoji": emoji,
            "answer": answer.lower()
        }

        msg = f"🎬 Guess the movie:\n\n{emoji}"
        kb = [
            [InlineKeyboardButton("🔁 Try Another", callback_data="game_emoji")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
        ]
        await safe_edit(query, msg, reply_markup=InlineKeyboardMarkup(kb))
  
    elif data == "quiz_gk_from_menu":
        query = update.callback_query
        chat_id = query.from_user.id

        # Only show the command — let your handler do the rest
        await context.bot.send_message(chat_id=chat_id, text="/gk_quiz")
        
    elif data == "quiz_gk":
        query = update.callback_query
        chat_id = query.from_user.id

        # Show next question directly
        if "used_questions" not in context.chat_data:
            context.chat_data["used_questions"] = []

        unused = [q for i, q in enumerate(gk_questions) if i not in context.chat_data["used_questions"]]
        if not unused:
            context.chat_data["used_questions"] = []
            unused = gk_questions[:]

        question = random.choice(unused)
        index = gk_questions.index(question)
        context.chat_data["used_questions"].append(index)
        gk_sessions[chat_id] = question["answer"]

        msg = f"🧠 {question['question']}\n" + "\n".join(question["options"])
        kb = [
            [InlineKeyboardButton("🔁 Try Another", callback_data="quiz_gk")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
        ]
        await safe_edit(query, msg, reply_markup=InlineKeyboardMarkup(kb))

    elif data == "menu_root":
        await show_inline_menu(update, context)

# === Games ===
async def start_guess(update, context):
    uid = update.effective_chat.id

    guess_data[uid] = random.randint(1, 100)

    msg = "🎯 I picked a number between 1 and 100. What's your guess?"
    kb = [
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
    ]
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb))

async def start_scramble(update, context):
    user_id = update.message.chat_id
    
    word, clue = random.choice(list(scramble_words.items()))
    scrambled = ''.join(random.sample(word, len(word)))
    scramble_sessions[user_id] = word
    
    msg = f"🔀 `{scrambled}`\n💡 Clue: {clue}"
    kb = [
        [InlineKeyboardButton("🔁 Try Another", callback_data="game_scramble")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
    ]
    await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

async def start_emoji_quiz(update, context):
    cid = update.effective_chat.id

    emoji, answer = random.choice(list(emoji_quiz.items()))
    emoji_sessions[cid] = {
        "emoji": emoji,
        "answer": answer.lower()
    }

    msg = f"🎬 Guess the movie:\n\n{emoji}"
    kb = [
        [InlineKeyboardButton("🔁 Try Another", callback_data="game_emoji")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
    ]
    await update.message.reply_text(msg, reply_markup=InlineKeyboardMarkup(kb))

async def start_gk_quiz(update, context):
    uid = update.effective_chat.id

    # Track used questions
    if "used_questions" not in context.chat_data:
        context.chat_data["used_questions"] = []

    unused = [q for i, q in enumerate(gk_questions) if i not in context.chat_data["used_questions"]]
    if not unused:
        context.chat_data["used_questions"] = []  # Reset when all used
        unused = gk_questions[:]

    # Pick a question
    question = random.choice(unused)
    index = gk_questions.index(question)
    context.chat_data["used_questions"].append(index)
    gk_sessions[uid] = question["answer"]

    # Prepare message and buttons
    msg = f"🧠 {question['question']}\n" + "\n".join(question["options"])
    kb = [
        [InlineKeyboardButton("🔁 Try Another", callback_data="quiz_gk")],
        [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
    ]

    await update.message.reply_text(
        msg,
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def handle_theme_selection(data, context, query, update):
    selected = data.split("_")[-1]
    context.user_data["theme"] = selected
    await query.answer(f"✅ Theme set to {selected.capitalize()}")
    await show_inline_menu(update, context)

async def handle_handwritten_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    doc = update.message.document
    if not doc:
        await update.message.reply_text("❌ No PDF received.")
        return
    
    if doc.file_size > 20 * 1024 * 1024:
        await update.message.reply_text("⚠️ File is too large. Please compress or split it (max 20MB).")
        return

    folder = "notes_handwritten"
    os.makedirs(folder, exist_ok=True)

    filename = doc.file_name
    file_path = os.path.join(folder, filename)

    file = await context.bot.get_file(doc.file_id)
    await file.download_to_drive(file_path)

    await update.message.reply_text(f"✅ Saved `{filename}` successfully.", parse_mode="Markdown")

# === Video Logic ===

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Optional: Handle things like raw YouTube links (if not already caught)
    if "youtube.com" in text or "youtu.be" in text:
        await handle_raw_link(update, context)
        return

    # Optional: Handle rename flow if active
    if "video_rename_target" in context.user_data:
        await rename_video_flow(update, context)
        return

    # Fallback message
    await update.message.reply_text("🤖 I didn't get that. Use /menu to explore options.")

async def handle_raw_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    import re
    text = update.message.text.strip()
    user_id = str(update.effective_user.id)

    data = load_video_links()
    data.setdefault(user_id, {})

    def is_youtube_link(s):
        pattern = r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/[^\s]+"
        return bool(re.search(pattern, s))

    def is_playlist_link(url):
        return "playlist?list=" in url or "list=" in url

    if "|" in text:
        # New Format: Folder | Title | URL
        try:
            folder, title, url = [part.strip() for part in text.split("|", 2)]
            if not is_youtube_link(url):
                raise ValueError("Invalid YouTube link")
            if is_playlist_link(url):
                title = f"[📂 Playlist] {title}"
            data[user_id].setdefault(folder, {})[title] = url
            save_video_links(data)
            await update.message.reply_text(
                f"✅ Saved to *{folder}*: *{title}*", parse_mode="Markdown"
            )
        except Exception:
            await update.message.reply_text(
                "⚠️ Format should be: `Folder | Title | YouTube URL`",
                parse_mode="Markdown"
            )

    elif is_youtube_link(text):
        # Old Format: Title + Link in same message
        parts = text.rsplit(" ", 1)
        if len(parts) == 2 and is_youtube_link(parts[1]):
            title, url = parts
        else:
            title = f"Untitled {len(data[user_id]) + 1}"
            url = text

        if is_playlist_link(url):
            title = f"[📂 Playlist] {title}"

        data[user_id][title.strip()] = url.strip()
        save_video_links(data)
        await update.message.reply_text(
            f"✅ Saved: *{title.strip()}*", parse_mode="Markdown"
        )

    else:
        await update.message.reply_text(
            "⚠️ That doesn’t look like a YouTube link.",
            parse_mode="Markdown"
        )

async def rename_video_flow(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    message = update.message
    input_text = message.text.strip()
    data = load_video_links()

    # 🔁 Folder-based rename
    if "video_rename_target" in context.user_data:
        rename_ctx = context.user_data.pop("video_rename_target")
        folder = rename_ctx.get("folder")
        old_title = rename_ctx.get("title")
        chat_id = rename_ctx.get("chat_id")
        message_id = rename_ctx.get("message_id")

        folder_data = data.get(user_id, {}).get(folder, {})
        if old_title not in folder_data:
            await message.reply_text("⚠️ Original video not found.")
            return

        url = folder_data[old_title]

        if "|" in input_text:
            # Full replace: New Title | New URL
            try:
                new_title, new_url = [part.strip() for part in input_text.split("|", 1)]
                folder_data.pop(old_title)
                folder_data[new_title] = new_url
                save_video_links(data)
                await context.bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f"🎬 *{new_title}*",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton("📺 Watch", url=new_url),
                            InlineKeyboardButton("✏️ Rename", callback_data=f"rename_video::{folder}::{new_title[:30]}"),
                            InlineKeyboardButton("🗑️ Delete", callback_data=f"delete_video::{folder}::{new_title[:30]}")
                        ]
                    ])
                )
                await message.reply_text("✅ Renamed title and URL successfully!", parse_mode="Markdown")
            except:
                await message.reply_text("⚠️ Please use format:\n`New Title | New URL`", parse_mode="Markdown")
                return
        else:
            # Only title changed
            new_title = input_text
            folder_data.pop(old_title)
            folder_data[new_title] = url
            save_video_links(data)

            await context.bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=f"🎬 *{new_title}*",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("📺 Watch", url=url),
                        InlineKeyboardButton("✏️ Rename", callback_data=f"rename_video::{folder}::{new_title[:30]}"),
                        InlineKeyboardButton("🗑️ Delete", callback_data=f"delete_video::{folder}::{new_title[:30]}")
                    ]
                ])
            )
        return

    # 📝 Pending direct save after asking for title
    if "pending_youtube" in context.user_data:
        url = context.user_data.pop("pending_youtube")
        title = input_text
        data.setdefault(user_id, {})[title] = url
        save_video_links(data)
        await message.reply_text(f"✅ Saved: *{title}*", parse_mode="Markdown")
        return

async def my_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_target = update.message or update.callback_query.message
    user_id = str(update.effective_user.id)
    data = load_video_links().get(user_id, {})

    if not data:
        await message_target.reply_text("📭 You haven't saved any videos yet.")
        return

    for key, value in data.items():
        if isinstance(value, str):
            await message_target.reply_text(
                f"🎬 *{key}*",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("📺 Watch", url=value),
                        InlineKeyboardButton("✏️ Rename", callback_data=f"rename_video::{key[:30]}"),
                        InlineKeyboardButton("🗑️ Delete", callback_data=f"delete_video::{key[:30]}")
                    ]
                ])
            )
        elif isinstance(value, dict):
            for title, url in value.items():
                safe_title = title[:30]
                safe_folder = key[:20]
                await message_target.reply_text(
                    f"📂 *{key}* → 🎬 *{title}*",
                    parse_mode="Markdown",
                    reply_markup=InlineKeyboardMarkup([
                        [
                            InlineKeyboardButton("📺 Watch", url=url),
                            InlineKeyboardButton("✏️ Rename", callback_data=f"rename_video::{safe_folder}::{safe_title}"),
                            InlineKeyboardButton("🗑️ Delete", callback_data=f"delete_video::{safe_folder}::{safe_title}")
                        ]
                    ])
                )

async def show_video_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "🎥 *Manage Your Videos:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📦 Video Actions", callback_data="video_actions_menu")],
            [InlineKeyboardButton("📂 View by Folder", callback_data="view_folders_menu")],
            [InlineKeyboardButton("🎬 View All Videos", callback_data="view_my_videos")],
            [InlineKeyboardButton("🔙 Back", callback_data="menu_root")]
        ])
    )

async def video_actions_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "📦 *Video Actions:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("➕ Add Video", callback_data="add_video")],
            [InlineKeyboardButton("✏️ Rename Video", callback_data="rename_from_menu")],
            [InlineKeyboardButton("🗑️ Delete Video", callback_data="delete_from_menu")],
            [InlineKeyboardButton("🔙 Back", callback_data="show_video_menu")]
        ])
    )

async def view_my_videos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    await my_videos(update, context)

async def add_video_mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    kb = [
        [InlineKeyboardButton("🔙 Back", callback_data="video_actions_menu")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="menu_root")]
    ]
    await update.callback_query.edit_message_text(
        "➕ *How to Add a YouTube Link:*\n\n"
        "`Folder | Title | https://youtube.com/watch?v=...`  ← for a single video to save in Folder\n"
        "`Folder | Title | https://youtube.com/playlist?list=...`  ← for a playlist\n\n"
        "_Send one of these directly in the chat to save._",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def rename_from_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    kb = [
        [InlineKeyboardButton("🔙 Back", callback_data="video_actions_menu")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="menu_root")]
    ]
    await update.callback_query.edit_message_text(
        "✏️ *How to Rename a Video or Playlist:*\n\n"
        "Tap the ✏️ Rename button in /myvideos next to a saved item, then reply with:\n\n"
        "`New Title`  ← just change name\n"
        "`New Title | New URL`  ← change name and YouTube link\n\n"
        "_Works for both flat and foldered videos._",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def delete_from_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("🔙 Back", callback_data="video_actions_menu")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="menu_root")]
    ]
    await update.callback_query.answer()
    await update.callback_query.edit_message_text(
        "🗑️ Use the 🗑️ Delete button next to any video shown in /myvideos or '🎬 View All Videos'.",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def rename_video_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()

    # 👇 Extract full folder and title from message text instead of sliced callback_data
    title_line = update.callback_query.message.text.strip()

    # Default values in case it's a flat entry
    folder = None
    title = ""

    if "→" in title_line:
        parts = title_line.split("→")
        folder = parts[0].replace("📂", "").strip()
        title = parts[1].replace("🎬", "").strip()
    else:
        title = title_line.replace("🎬", "").strip()

    context.user_data["video_rename_target"] = {
        "folder": folder,
        "title": title,
        "chat_id": update.effective_chat.id,
        "message_id": update.callback_query.message.message_id
    }

    await update.callback_query.edit_message_text(
        f"✏️ Send new name for: *{title}*\n\nFormat:\n`New Title`\nor\n`New Title | New URL`",
        parse_mode="Markdown"
    )

async def delete_video_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    title = update.callback_query.data.split("::")[1]
    user_id = str(update.callback_query.from_user.id)
    data = load_video_links()

    if title in data.get(user_id, {}):
        del data[user_id][title]
        save_video_links(data)
        await update.callback_query.edit_message_text(f"🗑️ Deleted video: *{title}*", parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text("⚠️ Video not found.")

async def view_folders_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    user_id = str(update.effective_user.id)
    data = load_video_links().get(user_id, {})

    if not data:
        await update.callback_query.edit_message_text("📭 No folders found.")
        return

    buttons = [
        [InlineKeyboardButton(f"📁 {folder}", callback_data=f"open_folder::{folder}"),
        InlineKeyboardButton("✏️", callback_data=f"rename_folder::{folder}")]
        for folder in data
    ]

    buttons.append([InlineKeyboardButton("🔙 Back", callback_data="menu_root")])

    await update.callback_query.edit_message_text(
        "📂 *Your Folders:*",
        parse_mode="Markdown",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

async def prompt_folder_rename(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    folder = update.callback_query.data.split("::")[1]
    context.user_data["folder_rename_target"] = folder
    await update.callback_query.edit_message_text(f"✏️ Send a new name for folder: *{folder}*", parse_mode="Markdown")

async def open_folder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.callback_query.answer()
    user_id = str(update.effective_user.id)
    folder = update.callback_query.data.split("::")[1]
    all_data = load_video_links()
    folder_data = all_data.get(user_id, {}).get(folder, {})

    if not isinstance(folder_data, dict):
        await update.callback_query.edit_message_text(
            f"⚠️ Folder *{folder}* is not properly structured.", parse_mode="Markdown"
        )
        return

    if not folder_data:
        await update.callback_query.edit_message_text(
            f"📭 *{folder}* is empty.", parse_mode="Markdown"
        )
        return

    await update.callback_query.edit_message_text(
        f"📂 *{folder}* videos 👇", parse_mode="Markdown"
    )

    for title, url in folder_data.items():
        safe_title = title[:30]
        safe_folder = folder[:20]
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"🎬 *{title}*",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("📺 Watch", url=url),
                    InlineKeyboardButton("✏️ Rename", callback_data=f"rename_video::{safe_folder}::{safe_title}"),
                    InlineKeyboardButton("🗑️ Delete", callback_data=f"delete_video::{safe_folder}::{safe_title}")
                ]
            ])
        )

# === Code Runner ===
async def run_jdoodle(update, context):
    try:
        parts = update.message.text.split("\n", 1)
        lang = parts[0].split()[1]
        code = parts[1]
        res = requests.post("https://api.jdoodle.com/v1/execute", json={
            "clientId": JD_CLIENT_ID,
            "clientSecret": JD_CLIENT_SECRET,
            "script": code,
            "language": lang,
            "versionIndex": "0"
        }).json()
        output = res.get("output", "❌ No output")
        await update.message.reply_text(f"🧪 Output:\n```\n{output}\n```", parse_mode="Markdown")
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {e}")

async def show_main_menu(update, context):
    await update.callback_query.message.reply_text(
        "🏠 *Main Menu:*\n\nType `/java your_topic` to get any Java program.\n\nExample:\n• `/java pattern_number_triangle`\n• `/java recursion_factorial`",
        parse_mode="Markdown"
    )

# === Java Question Handler ===
def normalize(text):
    return " ".join(text.strip().lower().split())

async def handle_java_question(update, context):
    query = ""
    source_message = None

    if update.message:
        query = update.message.text.strip()[6:].strip().lower()
        source_message = update.message

        # ✅ Only show feedback for typed commands
        display_title = query.replace("_", " ").title()
        await source_message.reply_text(
            f"✅ Received *{display_title}* program, preparing output...",
            parse_mode="Markdown"
        )

    elif update.callback_query:
        await update.callback_query.answer()
        query = update.callback_query.data[5:].strip().lower()
        source_message = update.callback_query.message
    else:
        return

    print(f"[JAVA] Requested: {query}")
    normalized = {normalize(k): v for k, v in java_answers.items()}
    answer = normalized.get(query)

    if answer:
        code_chunks = [escape(answer[i:i+3800]) for i in range(0, len(answer), 3800)]
        for i, chunk in enumerate(code_chunks):
            await source_message.reply_text(
                f"<pre><code>{chunk}</code></pre>", parse_mode="HTML"
            )
            if i < len(code_chunks) - 1:
                await asyncio.sleep(0.2)

        # Back buttons based on topic type
        nav_buttons = []

        if any(kw in query for kw in ["sort", "recursion", "pattern"]):
            nav_buttons.append([InlineKeyboardButton("🧮 View Sort Menu", callback_data="sort_menu")])

        nav_buttons.append([InlineKeyboardButton("🏠 Back to Java Menu", callback_data="show_java_help")])

        await source_message.reply_text(
            "⬅️ Navigate more Java topics:",
            reply_markup=InlineKeyboardMarkup(nav_buttons)
        )
        
    else:
        # Suggest close matches
        suggestions = [k for k in normalized if query in k]
        if suggestions:
            suggestion_buttons = [
                [InlineKeyboardButton(s.title(), callback_data=f"java:{s}")]
                for s in suggestions
            ]

            if "sort" in query:
                suggestion_buttons.append([InlineKeyboardButton("🧮 View Sort Menu", callback_data="sort_menu")])
            suggestion_buttons.append([InlineKeyboardButton("🏠 Main Menu", callback_data="show_java_help")])

            await source_message.reply_text(
                f"🤖 I didn’t find `{query}`, but maybe you meant:",
                reply_markup=InlineKeyboardMarkup(suggestion_buttons),
                parse_mode="Markdown"
            )
        else:
            await source_message.reply_text(
                f"❌ Sorry, I don't have a Java program for `{query}`.",
                parse_mode="Markdown"
            )

async def handle_sort_menu_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("📌 Sort menu triggered (command or button)")

    try:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 Bubble Sort", callback_data="java:bubble_sort")],
            [InlineKeyboardButton("🧲 Selection Sort", callback_data="java:selection_sort")],
            [InlineKeyboardButton("🗂️ Insertion Sort", callback_data="java:insertion_sort")],
            [InlineKeyboardButton("🔗 Merge Sort", callback_data="java:merge_sort")],
            [InlineKeyboardButton("⚡ Quick Sort", callback_data="java:quick_sort")],
            [InlineKeyboardButton("🔙 Back to Java Menu", callback_data="show_java_help")]
        ])

        if update.message:  # When triggered via /sort
            await update.message.reply_text(
                text="📚 *Java Sorting Techniques:*\nChoose one to view its code ⬇️",
                parse_mode="Markdown",
                reply_markup=keyboard
            )
        elif update.callback_query:  # When triggered via "Back to Sort Menu" button
            await update.callback_query.message.edit_text(
                text="📚 *Java Sorting Techniques:*\nChoose one to view its code ⬇️",
                parse_mode="Markdown",
                reply_markup=keyboard
            )

        print("📨 Sort menu sent!")

    except Exception as e:
        print(f"❌ [ERROR] Sort menu failed: {e}")

# === Java Help Command ===

async def show_java_help(update, context):
    topics = get_available_java_topics()

    buttons = []
    row = []
    for i, t in enumerate(topics, 1):
        button = InlineKeyboardButton(t.title(), callback_data=f"java:{normalize(t)}")
        row.append(button)
        if i % 2 == 0:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    buttons.append([InlineKeyboardButton("🏠 Back to Main Menu", callback_data="menu_root")])
    keyboard = InlineKeyboardMarkup(buttons)

    # ✅ Use edit_text instead of reply_text when it's a button press
    if update.message:
        await update.message.reply_text("🧠 Choose a Java program:", reply_markup=keyboard)
    elif update.callback_query:
        await update.callback_query.message.edit_text("🧠 Choose a Java program:", reply_markup=keyboard)

async def handle_java_button(update, context):
    print("📌 Java button handler activated")
    query = update.callback_query
    await query.answer()

    raw_data = query.data or ""
    topic = raw_data[5:].strip().lower()

    normalized = {normalize(k): v for k, v in java_answers.items()}
    answer = normalized.get(normalize(topic))

    if not answer:
        await query.message.reply_text(f"❌ Program not found: `{topic}`", parse_mode="Markdown")
        return
    
    await query.message.reply_text(f"✅ Received *{topic.title()}* program, preparing output...", parse_mode="Markdown")

    code = answer.strip()
    escaped = escape(code)
    chunks = [escaped[i:i+3800] for i in range(0, len(escaped), 3800)]

    for i, chunk in enumerate(chunks):
        formatted = f"<pre><code>{chunk}</code></pre>"
        print(f"[DEBUG] Chunk {i+1}/{len(chunks)} → {repr(formatted[:200])}")
        
        try:
            await query.message.reply_text(formatted, parse_mode="HTML")
            print(f"[DEBUG] Sent chunk {i+1}/{len(chunks)}")
            if i < len(chunks) - 1:
                await asyncio.sleep(0.3)
                
        except Exception as e:
            print(f"[DEBUG] Chunk {i+1} failed: {e}")

    # ✅ Smart back buttons after chunks are sent
    if topic.endswith("_sort"):
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🔙 Back to Sort Menu", callback_data="sort_menu")]
        ])
        await query.message.reply_text("⬅️ Back to sorting options:", reply_markup=keyboard)

    else:
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🏠 Back to Java Programs", callback_data="show_java_help")]
        ])
        await query.message.reply_text("⬅️ Back to Java program list:", reply_markup=keyboard)

# === Text Handling ===

async def handle_text(update, context):
    text = update.message.text.strip()
    cid = update.message.chat_id
    logging.info(f"[TEXT] {cid} sent: {text}")

    # === Game: Guess the Number ===
    if cid in guess_data:
        try:
            guess = int(text)
            target = guess_data[cid]
            if guess == target:
                del guess_data[cid]
                kb = [
                    [InlineKeyboardButton("🔁 Play Again", callback_data="game_guess")],
                    [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
                ]
                await update.message.reply_text("🎉 Bang on! You got it!", reply_markup=InlineKeyboardMarkup(kb))
            elif guess < target:
                await update.message.reply_text("📉 Too low!")
            else:
                await update.message.reply_text("📈 Too high!")
        except ValueError:
            await update.message.reply_text("⚠️ Please enter a valid number.")
        return

    # === Game: Word Scramble ===
    if cid in scramble_sessions:
        if text.lower() == scramble_sessions[cid].lower():
            del scramble_sessions[cid]
            kb = [
                [InlineKeyboardButton("🔁 Try Another", callback_data="game_scramble")],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
            ]
            await update.message.reply_text(
                "✅ You got it!",
                reply_markup=InlineKeyboardMarkup(kb)
            )
        else:
            await update.message.reply_text("❌ Try again.")
        return
    
    # === Quiz: GK ===
    # === Quiz: GK (Answers like A, B, C, D or /A) ===
    if cid in gk_sessions and (text.upper().startswith("/") or text.upper() in ["A", "B", "C", "D"]):
        guess = text.replace("/", "").strip().upper()
        correct = gk_sessions[cid]
        del gk_sessions[cid]
        kb = [
            [InlineKeyboardButton("🔁 Try Another", callback_data="quiz_gk")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
        ]
        if guess == correct:
            await update.message.reply_text("✅ Correct!", reply_markup=InlineKeyboardMarkup(kb))
        else:
            await update.message.reply_text(
                f"❌ Oops! The correct answer was /{correct}",
                reply_markup=InlineKeyboardMarkup(kb)
            )
        return
    
    # === Game: Emoji Quiz ===
    if cid in emoji_sessions:
        session = emoji_sessions[cid]  
        answer = session["answer"]
        if answer in text.lower():
            del emoji_sessions[cid]
            kb = [
                [InlineKeyboardButton("🔁 Try Another", callback_data="game_emoji")],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
            ]
            await update.message.reply_text(
                f"🎉 Correct! The movie was *{answer.title()}*.",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup(kb)
            )
        else:
            emoji = session["emoji"]
            del emoji_sessions[cid]  # ❗ Remove session just like GK does
            
            msg = f"❌ Oops! The correct answer was *{answer.title()}*.\n\n🎬 Emoji: {emoji}"
            kb = [
                [InlineKeyboardButton("🔁 Try Another", callback_data="game_emoji")],
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_root")]
            ]
            await update.message.reply_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))
        return
    
    if "rename_target" in context.user_data:
        old_filename = context.user_data.pop("rename_target")
        new_name = update.message.text.strip()
        
        if not new_name:
            await update.message.reply_text("❌ New name cannot be empty.")
            return

        new_filename = f"{new_name}.pdf"
        old_path = os.path.join("notes_handwritten", old_filename)
        new_path = os.path.join("notes_handwritten", new_filename)

        if os.path.exists(new_path):
            await update.message.reply_text("⚠️ A file with that name already exists.")
            return

        try:
            os.rename(old_path, new_path)
            await update.message.reply_text(f"✅ Renamed to: *{new_filename}*", parse_mode="Markdown")
        except Exception as e:
            await update.message.reply_text(f"❌ Failed to rename file.\n{e}")

    # === Placeholder for Java logic ===
    if text.startswith("/java "):
        return  # handled by separate handler

    if "folder_rename_target" in context.user_data:
        old_name = context.user_data.pop("folder_rename_target")
        new_name = update.message.text.strip()
        
        user_id = str(update.effective_user.id)
        data = load_video_links()

        if new_name in data.get(user_id, {}):
            await update.message.reply_text("⚠️ A folder with that name already exists.")
            return

        data[user_id][new_name] = data[user_id].pop(old_name)
        save_video_links(data)
        await update.message.reply_text(f"✅ Folder renamed to *{new_name}*", parse_mode="Markdown")
        return

    # === Default fallback ===
    await update.message.reply_text("🤔 Try /menu to explore features.")

# === Boot the Bot ===
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # === Menu Buttons ===
    app.add_handler(CallbackQueryHandler(handle_sort_menu_button, pattern="^sort_menu$"))
    app.add_handler(CallbackQueryHandler(show_java_help, pattern="^show_java_help$"))
    app.add_handler(CommandHandler("javahelp", show_java_help))
    app.add_handler(CallbackQueryHandler(handle_java_button, pattern=re.compile("^java:", re.IGNORECASE)))
    app.add_handler(CallbackQueryHandler(handle_bookmark_folders, pattern="^bk_folders$"))
    app.add_handler(CallbackQueryHandler(show_bookmarks_in_folder, pattern="^bk_folder:"))
    app.add_handler(CallbackQueryHandler(handle_mynotes, pattern="^mynotes$"))
    app.add_handler(CallbackQueryHandler(handle_note_read, pattern="^note_read:"))
    app.add_handler(CallbackQueryHandler(handle_menu_selection, pattern="^show_notes_menu$"))

    # === Video Menu Callbacks ===
    app.add_handler(CallbackQueryHandler(show_video_menu, pattern="^show_video_menu$"))
    app.add_handler(CallbackQueryHandler(video_actions_menu, pattern="^video_actions_menu$"))
    app.add_handler(CallbackQueryHandler(view_my_videos, pattern="^view_my_videos$"))
    app.add_handler(CallbackQueryHandler(add_video_mode, pattern="^add_video$"))
    app.add_handler(CallbackQueryHandler(rename_from_menu, pattern="^rename_from_menu$"))
    app.add_handler(CallbackQueryHandler(delete_from_menu, pattern="^delete_from_menu$"))
    app.add_handler(CallbackQueryHandler(rename_video_button, pattern="^rename_video::"))
    app.add_handler(CallbackQueryHandler(delete_video_button, pattern="^delete_video::"))
    app.add_handler(CallbackQueryHandler(view_folders_menu, pattern="^view_folders_menu$"))
    app.add_handler(CallbackQueryHandler(open_folder, pattern="^open_folder::"))
    app.add_handler(CallbackQueryHandler(prompt_folder_rename, pattern="^rename_folder::"))
    app.add_handler(CallbackQueryHandler(handle_menu_selection, pattern="^inline_bots_guide$"))

    app.add_handler(CommandHandler("myvideos", my_videos))
    java_pattern = re.compile(r"^/java\s+", flags=re.IGNORECASE)
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(java_pattern), handle_java_question))

    app.add_handler(CallbackQueryHandler(handle_menu_selection, pattern=r"^(menu_|bk_|note_|game_|scramble_|quiz_|emoji_|guess_the_number_|guess_|note_read:)"))
    app.add_handler(CallbackQueryHandler(show_main_menu, pattern="^menu_root$"))
    app.add_handler(CallbackQueryHandler(handle_unknown_callbacks))

    # === Core Commands ===
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", show_inline_menu))

    app.add_handler(MessageHandler(filters.Document.PDF, handle_handwritten_pdf))

    # === Game & Quiz Commands ===
    app.add_handler(CommandHandler("guess_the_number", start_guess))
    app.add_handler(CommandHandler("scramble", start_scramble))
    app.add_handler(CommandHandler("emoji", start_emoji_quiz))
    app.add_handler(CommandHandler("gk_quiz", start_gk_quiz))
    app.add_handler(MessageHandler(filters.Regex(r"^/[A-Da-d]$"), handle_text))

    # === JDoodle ===
    app.add_handler(CommandHandler("run", run_jdoodle))

    # === Notes Commands ===
    app.add_handler(CommandHandler("note", save_note))
    app.add_handler(CommandHandler("read", read_note))
    app.add_handler(CommandHandler("mynotes", list_notes))
    app.add_handler(CommandHandler("delete", delete_note))
    app.add_handler(CommandHandler("edit", edit_note))
    app.add_handler(CommandHandler("rename", rename_note))
    app.add_handler(CommandHandler("bullets", send_bullet_template))

    # === Bookmark Commands ===
    app.add_handler(CommandHandler("bookmark", save_bookmark))
    app.add_handler(CommandHandler("mybookmarks", show_bookmarks))
    app.add_handler(CommandHandler("deletebookmark", delete_bookmark))
    app.add_handler(CommandHandler("editbookmark", edit_bookmark))
    app.add_handler(CommandHandler("exportbookmarks", export_bookmarks))
    app.add_handler(CommandHandler("exportcategory", export_category))

    # === Fallback for other unmatched text ===
    app.add_handler(MessageHandler(filters.TEXT, handle_text))

    # === Java Help Commands ===
    app.add_handler(CommandHandler("javahelp", show_java_help))
    # app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    # === Unknown Callback Logger ===
    app.add_handler(CallbackQueryHandler(lambda u, c: print(f"[🔍] Caught callback: {u.callback_query.data!r}")))

    # === Error Handling ===
    app.add_error_handler(error_handler)

    print("✅ All handlers registered!")
    print("[DEBUG] Current java_answers keys:", list(java_answers.keys()))
    print("Total keys:", len(java_answers))
    # print("Keys:\n", list(java_answers.keys())) 
    # print("Handlers:", app.handlers) 
    print("🚀 Bot is up and running!")

    app.run_polling()

# 🧪 Launch It
if __name__ == "__main__":
    main()