"""
MIT License

Copyright (c) 2022 itttgg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__all__: tuple[str] = (
    "DisMessage"
)

from typing import (
    Optional,
    final
)

from disspy.embed import DisEmbed
from disspy.jsongenerators import _EmbedGenerator


class _SendingRestHandler:
    @staticmethod
    async def execute(channel_id, payload, token):
        from aiohttp import ClientSession as CS

        async with CS(headers={'Authorization': f'Bot {token}'}) as s:
            _u = f"https://discord.com/api/v9/channels/{channel_id}/messages"

            async with s.post(_u, data=payload) as p:
                j = await p.json()

                return j


@final
class DisMessage:
    def __init__(self, _data, _token):
        from disspy.channel import DisChannel

        self._json = _data

        self.channel = DisChannel(_data["channel_id"], _token)

        self._headers = {'Authorization': f'Bot {_token}'}

        self.content = _data["content"]
        self.id = _data["id"]

        self._t = _token

    async def reply(self, content: Optional[str] = None, embeds: Optional[list[DisEmbed]] = None):
        _url = f"https://discord.com/api/v9/channels/{self.channel.id}/messages"

        _d = {
            "content": None,
            "embeds": None,
            "type": 19,
            "message_reference": {
                "message_id": self.id
            },
            "referenced_message": self._json
            }

        if content:
            _d["content"] = content

        if embeds:
            embeds_jsons = []

            for i in embeds:
                embeds_jsons.append(_EmbedGenerator(i))

            _d["embeds"] = embeds_jsons

        if not embeds and not content:
            return

        d = await _SendingRestHandler.execute(self.channel.id, _d, self._t)
        print(_d)
        print(d)

    async def reply(self, content: Optional[str] = None, embed: Optional[DisEmbed] = None):
        _url = f"https://discord.com/api/v9/channels/{self.channel.id}/messages"

        _d = {
            "content": None,
            "embeds": None,
            "type": 19,
            "message_reference": {
                "message_id": self.id
            },
            "referenced_message": self._json
        }

        if embed:
            _d["embeds"] = [_EmbedGenerator(embed)]

        if content:
            _d["content"] = content

        if not content and not embed:
            return

        d = await _SendingRestHandler.execute(self.channel.id, _d, self._t)
        print(_d)
        print(d)
