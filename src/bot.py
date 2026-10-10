from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import traceback

from config import telegramBotToken
from database import Database
from discovery import DeveloperDiscovery
from formatter import formatDevelopers

db = Database()

async def findCommand(update:Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user:
        return
    
    telegramUserId = update.effective_user.id

    statusMessage = await update.message.reply_text("🔎 Finding fresh developers")
    
    seen = db.getSeenUsernames(telegramUserId)

    discovery = DeveloperDiscovery()

    try:
        developers = await discovery.find(seenUsernames=seen)

        if not developers:
            await statusMessage.edit_text("No new developers found.")
            return
        
        usernames = [dev["username"] for dev in developers]

        db.markSeen(telegramUserId, usernames)

        message = formatDevelopers(developers)

        await statusMessage.delete()

        await update.message.reply_text(
            message,
            parse_mode="HTML",
            disable_web_page_preview=True
        )
    except Exception:
        traceback.print_exc()
        await statusMessage.edit_text("Something went wrong while searching.\n\nContact Dev")
    finally:
        await discovery.close()

async def resetCommand(update:Update, context:ContextTypes.DEFAULT_TYPE):
    if not update.effective_user:
        return
    
    telegramUserId = update.effective_user.id

    count = db.countSeen(telegramUserId)

    db.resetUser(telegramUserId)

    await update.message.reply_text(
        "♻️ Reset complete.\n\n"
        f"Forgot {count} previously shown developers."
    )

def main():
    application = (
        Application.builder().token(telegramBotToken).build()
    )

    application.add_handler(
        CommandHandler("find", findCommand)
    )

    application.add_handler(
        CommandHandler("reset", resetCommand)
    )

    print("Bot is running...")

    application.run_polling()

if __name__ == "__main__":
    main()
