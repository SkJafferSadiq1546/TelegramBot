import json, os, logging, aiohttp
from bs4 import BeautifulSoup
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

# === Logging Setup ===
logging.basicConfig(level=logging.INFO)

# === File Paths ===
NOTES_FILE = "notes.json"
BOOKMARKS_FILE = "bookmarks.json"

# === Utility Functions ===
def load_notes():
    if os.path.exists(NOTES_FILE):
        try:
            with open(NOTES_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_notes(data):
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_bookmarks():
    if os.path.exists(BOOKMARKS_FILE):
        try:
            with open(BOOKMARKS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_bookmarks(data):
    with open(BOOKMARKS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

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

# === Smart Edit Helper ===
async def safe_edit(query, text, update=None, **kwargs):
    try:
        if query:
            await query.edit_message_text(text, **kwargs)
        elif update and update.message:
            await update.message.reply_text(text, **kwargs)
        else:
            logging.warning("[⚠️] safe_edit() has no valid target to send to.")
    except Exception as e:
        logging.error(f"[❌] safe_edit() failed: {e}")

# [ Paste your complete Notes and Bookmarks handler functions here ]
# (You've already got them ready, and the last message contains the full set!)

# If you'd like me to bundle this full file as a downloadable `.py`, just say the word!

# === Notes Handlers ===

async def save_note(update, context):
    lines = update.message.text.split("\n", 1)
    if len(lines) < 2:
        await update.message.reply_text("✏️ Use:\n/note title\\ncontent")
        return
    title = lines[0].replace("/note", "").strip()
    content = lines[1]
    user_id = str(update.effective_user.id)
    notes = load_notes()
    notes.setdefault(user_id, {})[title] = content
    save_notes(notes)
    await update.message.reply_text(f"✅ Saved note '{title}'")

async def read_note(update, context):
    title = update.message.text.replace("/read", "").strip()
    user_id = str(update.effective_user.id)
    notes = load_notes().get(user_id, {})
    match = next((t for t in notes if t.lower() == title.lower()), None)
    if match:
        await update.message.reply_text(f"📖 <b>{match}</b>:\n{notes[match]}", parse_mode="HTML")
    else:
        await update.message.reply_text("❌ Note not found.")

async def list_notes(update, context):
    user_id = str(update.effective_user.id)
    notes = load_notes().get(user_id, {})
    if not notes:
        await update.message.reply_text("📭 No saved notes.")
        return
    buttons = [[InlineKeyboardButton(f"📝 {title}", callback_data=f"note_read:{title}")] for title in notes]
    buttons.append([InlineKeyboardButton("🏠 Back to Menu", callback_data="menu_root")])
    await update.message.reply_text("📒 Your notes:", reply_markup=InlineKeyboardMarkup(buttons))

async def handle_note_read(update, context):
    query = update.callback_query
    await query.answer()

    user_id = str(update.effective_user.id)
    title = query.data.split("note_read:")[-1]

    notes = load_notes().get(user_id, {})
    content = notes.get(title)

    if not content:
        await query.message.edit_text("❌ Note not found.")
        return

    keyboard = [
        [InlineKeyboardButton("🔙 Back to Notes", callback_data="mynotes")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="menu_root")]
    ]
    await query.message.edit_text(
        f"<b>{title}</b>\n\n{content}",
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_mynotes(update, context):
    query = update.callback_query
    await query.answer()

    user_id = str(update.effective_user.id)
    notes = load_notes().get(user_id, {})

    if not notes:
        keyboard = [[
            InlineKeyboardButton("🔙 Back to Notes Menu", callback_data="menu_notes"),
            InlineKeyboardButton("🏠 Back to Main Menu", callback_data="menu_root")
        ]]
        await query.message.edit_text("📭 No saved notes yet.", reply_markup=InlineKeyboardMarkup(keyboard))
        return

    keyboard = [
        [InlineKeyboardButton(f"📝 {title}", callback_data=f"note_read:{title}")]
        for title in notes
    ]
    keyboard.append([
        InlineKeyboardButton("🔙 Back to Notes Menu", callback_data="menu_notes"),
        InlineKeyboardButton("🏠 Back to Main Menu", callback_data="menu_root")
    ])

    await query.message.edit_text("📒 Your Notes:", reply_markup=InlineKeyboardMarkup(keyboard))

async def delete_note(update, context):
    title = update.message.text.replace("/delete", "").strip()
    user_id = str(update.effective_user.id)
    notes = load_notes()
    if user_id in notes and title in notes[user_id]:
        del notes[user_id][title]
        save_notes(notes)
        await update.message.reply_text(f"🗑️ Deleted '{title}'")
    else:
        await update.message.reply_text("❌ Note not found.")

async def edit_note(update, context):
    lines = update.message.text.split("\n", 1)
    if len(lines) < 2:
        await update.message.reply_text("✏️ Use:\n/edit Note Title\\nNew content")
        return
    title = lines[0].replace("/edit", "").strip()
    user_id = str(update.effective_user.id)
    all_notes = load_notes()
    user_notes = all_notes.get(user_id, {})
    match = next((t for t in user_notes if t.lower() == title.lower()), None)
    if match:
        user_notes[match] = lines[1]
        all_notes[user_id] = user_notes
        save_notes(all_notes)
        await update.message.reply_text(f"✅ Updated note '{match}'")
    else:
        await update.message.reply_text("❌ Note not found.")

async def rename_note(update, context):
    lines = update.message.text.split("\n", 1)
    if len(lines) < 2:
        await update.message.reply_text("✏️ Use:\n/rename Old Title\\nNew Title")
        return
    old_title = lines[0].replace("/rename", "").strip()
    new_title = lines[1].strip()
    user_id = str(update.effective_user.id)
    notes = load_notes()
    user_notes = notes.get(user_id, {})
    match = next((t for t in user_notes if t.lower() == old_title.lower()), None)
    if match:
        user_notes[new_title] = user_notes.pop(match)
        notes[user_id] = user_notes
        save_notes(notes)
        await update.message.reply_text(f"✅ Renamed '{match}' to '{new_title}'")
    else:
        await update.message.reply_text("❌ Note not found.")

async def send_bullet_template(update, context):
    template = (
        "📝 Here's your bullet note template:\n\n"
        "• To bold: use <code>&lt;b&gt;Content&lt;/b&gt;</code>\n"
        "• To underline: <code>&lt;u&gt;Content&lt;/u&gt;</code>\n"
        "• To italicize: <code>&lt;i&gt;Content&lt;/i&gt;</code>\n\n"
        "🧠 Use this format with /note like:\n"
        "/note Loops\n"
        "• <b>For Loop</b>\n"
        "• <u>While Loop</u>\n"
        "• <i>Do-While</i>\n\n"
        "💡 To get the bullet symbol: press Alt + 7 on the right-side numpad."
    )
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Back to Notes Menu", callback_data="menu_notes")],
        [InlineKeyboardButton("🏠 Back to Main Menu", callback_data="menu_root")]
    ])
    await update.message.reply_text(template, parse_mode="HTML", reply_markup=keyboard)

# === Bookmarks Handlers ===

async def save_bookmark(update, context):
    try:
        user_id = str(update.effective_user.id)
        text = update.message.text.split(" ", 1)[1].strip()
        parts = text.split("\n")

        # Format 1: /bookmark Category\nTitle\nURL
        if len(parts) == 3:
            category = parts[0].strip()
            title = parts[1].strip()
            url = parts[2].strip()

        # Format 2: /bookmark Title\nURL
        elif len(parts) == 2:
            title = parts[0].strip()
            url = parts[1].strip()
            category = "General"

        # Format 3: /bookmark URL only
        elif len(parts) == 1:
            url = parts[0].strip()
            title = await fetch_title_from_url(url)
            category = "General"

        else:
            await update.message.reply_text("❌ Use:\n/bookmark [Category]\\nTitle\\nURL")
            return

        bookmarks = load_bookmarks()
        if user_id not in bookmarks:
            bookmarks[user_id] = []

        bookmarks[user_id].append({"category": category, "title": title, "url": url})
        save_bookmarks(bookmarks)

        await update.message.reply_text(f"✅ Saved: [{category}] {title}")

    except Exception as e:
        await update.message.reply_text(f"⚠️ Failed to save bookmark.\n{e}")

def get_all_folders_from_file(path="bookmarks.json", user_id=None):
    try:
        with open(path, "r") as f:
            data = json.load(f)

        print("☑️ JSON keys:", list(data.keys()))  # ✅ This is the safe place
        
        print(f"[DEBUG] Data keys: {list(data.keys())}")
        print(f"[DEBUG] Data for user {user_id}:", data.get(user_id))

        if not user_id or user_id not in data:
            return []

        folders = {entry.get("category", "").strip() for entry in data[user_id] if entry.get("category")}
        return sorted(folders)

    except Exception as e:
        print(f"[ERROR] Could not load folders: {e}")
        return []

async def handle_bookmark_folders(update, context):
    user_id = str(update.effective_user.id)
    folders = get_all_folders_from_file(user_id=user_id)

    await update.callback_query.answer()

    print("[DEBUG] Folder handler triggered for user:", user_id)
    print("→ Folders returned:", folders)
    print("☑️ Effective user ID:", user_id)
    
    if not folders:
        await update.callback_query.message.reply_text("📂 No folders found. Save at least one bookmark with a folder name.")
        return

    keyboard = [
        [InlineKeyboardButton(folder.title(), callback_data=f"bk_folder:{folder}")]
        for folder in folders
    ]
    keyboard.append([InlineKeyboardButton("🏠 Back to Main Menu", callback_data="menu_root")])

    await update.callback_query.message.reply_text(
        "📁 Choose a folder to view its bookmarks:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def show_bookmarks(update, context):
    user_id = str(update.effective_user.id)
    bm = load_bookmarks().get(user_id, [])
    if not bm:
        await update.message.reply_text("📭 No saved bookmarks.")
        return
    text = "\n\n".join([
        f"{i+1}. [{b['category']}] {b['title']}\n{b['url']}" for i, b in enumerate(bm)
    ])
    await update.message.reply_text(f"🔖 Bookmarks:\n\n{text}", disable_web_page_preview=True)

async def delete_bookmark(update, context):
    try:
        user_id = str(update.effective_user.id)
        index = int(context.args[0]) - 1
        data = load_bookmarks()
        deleted = data[user_id].pop(index)
        save_bookmarks(data)
        await update.message.reply_text(f"🗑️ Deleted: {deleted['title']}")
    except Exception:
        await update.message.reply_text("❌ Use: /deletebookmark <index>")

async def edit_bookmark(update, context):
    try:
        user_id = str(update.effective_user.id)
        index = int(context.args[0]) - 1
        text = update.message.text.split("\n", 2)
        new_title = text[1].strip()
        new_url = text[2].strip()
        data = load_bookmarks()
        data[user_id][index].update({"title": new_title, "url": new_url})
        save_bookmarks(data)
        await update.message.reply_text(f"✅ Updated: {new_title}")
    except Exception:
        await update.message.reply_text("❌ Format:\n/editbookmark <index>\\nNew Title\\nNew URL")

async def show_bookmarks_in_folder(update, context):
    query = update.callback_query
    await query.answer()

    try:
        folder_name = query.data.split(":", 1)[1]
        user_id = str(query.from_user.id)
        bookmarks = load_bookmarks().get(user_id, [])

        filtered = [
            b for b in bookmarks
            if b.get("category", "General").lower() == folder_name.lower()
        ]

        if not filtered:
            await query.message.reply_text(
                f"📭 No bookmarks in folder *{folder_name}*",
                parse_mode="Markdown",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Back to Bookmarks Menu", callback_data="menu_bookmarks")],
                    [InlineKeyboardButton("🏠 Main Menu", callback_data="menu_root")]
                ])
            )
            return

        message = f"📁 Bookmarks in *{folder_name}*:\n\n"
        for i, b in enumerate(filtered, 1):
            message += f"{i}. [{b['title']}]({b['url']})\n"

        await query.message.reply_text(
            message,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🔙 Back to Bookmarks Menu", callback_data="menu_bookmarks")],
                [InlineKeyboardButton("🏠 Main Menu", callback_data="menu_root")]
            ])
        )

    except Exception as e:
        print(f"[ERROR] Failed to show bookmarks in folder: {e}")
        await query.message.reply_text("⚠️ Something went wrong while loading that folder.")

async def export_bookmarks(update, context):
    user_id = str(update.effective_user.id)
    bookmarks = load_bookmarks().get(user_id, [])
    if not bookmarks:
        await update.message.reply_text("📭 No bookmarks to export.")
        return
    content = "\n\n".join([f"[{b['category']}] {b['title']}\n{b['url']}" for b in bookmarks])
    with open("exported_bookmarks.txt", "w", encoding="utf-8") as f:
        f.write(content)
    with open("exported_bookmarks.txt", "rb") as f:
        await update.message.reply_document(f, filename="MyBookmarks.txt")

async def export_category(update, context):
    user_id = str(update.effective_user.id)
    bookmarks = load_bookmarks().get(user_id, [])
    if not context.args:
        await update.message.reply_text("❗ Usage: `/exportcategory FolderName`", parse_mode="Markdown")
        return
    category = " ".join(context.args).strip()
    filtered = [b for b in bookmarks if b.get("category", "General") == category]
    if not filtered:
        await update.message.reply_text(f"📭 No bookmarks found in category *{category}*", parse_mode="Markdown")
        return
    content = "\n\n".join([f"{b['title']}\n{b['url']}" for b in filtered])
    filename = f"{category}_bookmarks.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    with open(filename, "rb") as f:
        await update.message.reply_document(f, filename=filename)
