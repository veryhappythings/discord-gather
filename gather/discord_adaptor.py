import discord


class DiscordAdaptor:
    def __init__(self, token):
        self.token = token
        self.client = discord.Client()

    def run(self):
        self.client.run(self.token)

    def register_on_ready(self, target):
        self.client.on_ready = target

    def register_on_message(self, target):
        self.client.on_message = target

    def register_on_member_update(self, target):
        self.client.on_member_update = target

    def username(self):
        return self.client.user.name

    async def send_message(self, channel, message):
        await self.client.send_message(channel, message)
