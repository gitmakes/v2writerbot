from hydrogram import Client, filters
from hydrogram.enums import ChatAction
from .slash_test import get_config
from environment import test_server
import requests
import asyncio


def check_alive(config):
    check_tool = f"{test_server}/check"
    r = requests.get(check_tool, params={"q": config})
    response = r.json()
    return response.get("alive", False)

def generate_link(item_list):
    data = "\n".join(item_list)
    r = requests.post("https://paste.rs/", data=data)
    return r.text

@Client.on_message(filters.command("filter_alive"))
async def filter_alive(c, m):
    """
    command function
    """
    user = m.from_user.first_name if m.from_user else m.sender_chat.title
    await m.reply_chat_action(ChatAction.TYPING)
    if m.reply_to_message:
        mpath = m.text.split()
        urls = [
            part
            for part in mpath
            if any(part.startswith(scheme) for scheme in ["http://", "https://"])
        ]
    else:
        urls = [
            part
            for part in m.command
            if any(part.startswith(scheme) for scheme in ["http://", "https://"])
        ]

    async def handler(url):
        test_url, count = await get_config(url)
        text = f'**{user}** đang lọc subscription {url} với {count} server'
        tmp = await m.reply(text, quote=True)
        response = requests.get(test_url, timeout=120)
        configs = response.text.splitlines()
        alive_list = []
        dead_list = []
        for config in configs:
            if check_alive(config):
                alive_list.append(config)
            else:
                dead_list.append(config)

        alive_link = generate_link(alive_list)
        dead_count = len(dead_list)
        text = [
            f"Original: {url}",
            f"Kết quả: {alive_link}",
            f"Đã xóa {dead_count} liên kết",
            f"Sender **{user}**",
        ]
        text = "\n".join(text)
        await m.reply(text, quote=True)
        await tmp.delete()

    async def main(urls):
        tasks = []
        for url in urls:
            tasks.append(asyncio.create_task(handler(url)))
        await asyncio.gather(*tasks)

    await main(urls)
