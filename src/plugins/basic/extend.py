from hydrogram import Client, filters
from hydrogram.enums import ChatAction


@Client.on_message(filters.command("ext"))
def ext_command_list(c, m):
    m.reply_chat_action(ChatAction.TYPING)
    with open("text/ext.md") as f:
        text = f.read()
    text = text.replace("{first_name}", m.from_user.first_name)
    text = text.replace("{uid}", str(m.from_user.id))
    m.reply(text, quote=True)