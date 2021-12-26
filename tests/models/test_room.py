from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from cerbottana.models.room import Room
from cerbottana.models.user import User

if TYPE_CHECKING:
    from tests.conftest import ServerWs, TestConnection


@pytest.mark.parametrize(
    "room, roomid",
    (
        ("Room1", "room1"),
        ("Room 2", "room2"),
        ("ROOM-3", "room-3"),
        ("room_4", "room4"),
        ("Français", "franais"),
    ),
)
async def test_roomid(mock_connection, room: str, roomid: str) -> None:
    async def handler(ws: ServerWs, conn: TestConnection) -> None:

        assert Room.get(conn, room).roomid == roomid

    await mock_connection(handler)


@pytest.mark.parametrize(
    "messages, buffer",
    (
        (
            [
                [
                    ">room1",
                    "|c|user|msg1",
                ],
                [
                    ">room1",
                    "|c|user|msg2",
                ],
            ],
            ["msg1", "msg2"],
        ),
        (
            [
                [
                    ">room1",
                    "|c|user|msg1",
                ],
                [
                    ">room2",
                    "|c|user|msg2",
                ],
            ],
            ["msg1"],
        ),
        (
            [
                [
                    ">room2",
                    "|c|user|msg1",
                ],
                [
                    ">room2",
                    "|c|user|msg2",
                ],
            ],
            [],
        ),
        (
            [
                [
                    ">room1",
                    "|j| user",
                ],
                [
                    ">room1",
                    "|n| user2|user",
                ],
                [
                    ">room1",
                    "|l|user",
                ],
            ],
            [],
        ),
    ),
)
async def test_buffer(
    mock_connection, messages: list[list[str]], buffer: list[str]
) -> None:
    async def handler(ws: ServerWs, conn: TestConnection) -> None:

        room = Room.get(conn, "room1")
        for message in messages:
            await ws.add_messages(message)
        await ws.get_messages()
        assert list(room.buffer) == buffer

    await mock_connection(handler)


@pytest.mark.parametrize(
    "public_roomids, room, is_private",
    (
        (set(), "room1", True),
        ({"room1"}, "room1", False),
        ({"room12"}, "room1", True),
        ({"room1"}, "room12", True),
    ),
)
async def test_is_private(
    mock_connection, public_roomids: set[str], room: str, is_private: bool
) -> None:
    async def handler(ws: ServerWs, conn: TestConnection) -> None:

        conn.public_roomids = public_roomids
        assert Room.get(conn, room).is_private == is_private

    await mock_connection(handler)


@pytest.mark.parametrize(
    "language, language_id",
    (
        (None, 9),  # English
        ("Japanese", 9),  # English
        ("French", 5),
        ("German", 6),
        ("Spanish", 7),
        ("Italian", 8),
        ("English", 9),
        ("Dummy", 9),  # English
    ),
)
async def test_language_id(
    mock_connection, language: str | None, language_id: int
) -> None:
    async def handler(ws: ServerWs, conn: TestConnection) -> None:

        room = Room.get(conn, "room1")
        if language is not None:
            room.language = language
        assert room.language_id == language_id

    await mock_connection(handler)


@pytest.mark.parametrize(
    "usernames_add, usernames_remove",
    (
        ({"user1": " "}, set()),
        ({"user1": None, "user2": " ", "user3": "+", "user4": "#"}, set()),
        ({"user1": None}, {"user1"}),
        ({"user1": None, "user2": None}, {"user2", "user3"}),
    ),
)
async def test_users(
    mock_connection, usernames_add: dict[str, str], usernames_remove: set[str]
) -> None:
    async def handler(ws: ServerWs, conn: TestConnection) -> None:

        room = Room.get(conn, "room1")
        users = {}

        for username in usernames_add:
            user = User.get(conn, username)
            rank = usernames_add[username]
            room.add_user(user, rank)
            users[user] = rank or " "

        for username in usernames_remove:
            user = User.get(conn, username)
            room.remove_user(user)
            if user in users:
                users.pop(user)

        assert room.users == users

    await mock_connection(handler)
