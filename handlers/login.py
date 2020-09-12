from __future__ import annotations

import json
import urllib.parse
import urllib.request
from typing import TYPE_CHECKING

import utils
from handlers import handler_wrapper

if TYPE_CHECKING:
    from connection import Connection
    from models.room import Room


@handler_wrapper(["challstr"])
async def challstr(conn: Connection, room: Room, *args: str) -> None:
    if len(args) < 1:
        return

    challstring = "|".join(args)

    payload = (
        "act=login&"
        f"name={conn.username}"
        f"&pass={conn.password}"
        f"&challstr={challstring}"
    ).encode()

    req = urllib.request.Request(
        "https://play.pokemonshowdown.com/action.php",
        payload,
        {"User-Agent": "Mozilla"},
    )
    resp = urllib.request.urlopen(req)

    assertion = json.loads(resp.read().decode("utf-8")[1:])["assertion"]

    if assertion:
        await conn.send(f"|/trn {conn.username},0,{assertion}")


@handler_wrapper(["updateuser"])
async def updateuser(conn: Connection, room: Room, *args: str) -> None:
    if len(args) < 4:
        return

    user = args[0]
    # named = args[1]
    avatar = args[2]
    # settings = args[3]

    username = user.split("@")[0]
    if utils.to_user_id(username) != utils.to_user_id(conn.username):
        return

    if conn.avatar and avatar != conn.avatar:
        await conn.send(f"|/avatar {conn.avatar}")

    if conn.statustext:
        await conn.send(f"|/status {conn.statustext}")

    for roomid in conn.rooms:
        await conn.send(f"|/join {roomid}")
