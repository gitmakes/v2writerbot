from hydrogram import Client, filters
from hydrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ChatPermissions
from hydrogram.enums import ChatAction
from datetime import datetime, timedelta
import requests

def _filter(_, __, m):
    try:
        if len(m.text) > 4000:
            return True
        else:
            raise
    except:
        return False
    
@Client.on_message(filters.group & filters.create(_filter))
def detector(c, m):
    m.chat.restrict_member(m.from_user.id, permissions=ChatPermissions(can_send_messages=False), until_date=datetime.now() + timedelta(seconds=120))
    m.reply_chat_action(ChatAction.TYPING)
    #m.delete()
    #res = requests.post("https://tempnote-1-q9925339.deta.app/post", data=m.text)
    user_id = m.from_user.id
    name = m.from_user.first_name
    user = f"[{name}](tg://user?id={user_id})"
    m.reply(f"Tin nhắn của **{user}** có dấu hiệu spam. \n**[Neko](tg://user?id=5537568128)**, hãy đưa ra quyết định đối với người này đi.")