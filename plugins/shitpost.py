from __future__ import annotations

import json
import random
from typing import TYPE_CHECKING, Dict, List

import utils
from plugins import command_wrapper

if TYPE_CHECKING:
    from models.message import Message


@command_wrapper(
    aliases=("say",),
    helpstr="FOR THE MIMMMSSS",
    is_unlisted=True,
)
async def shitpost(msg: Message) -> None:
    if msg.room is None:
        return
    phrase = utils.remove_accents(msg.arg.strip())
    if len(phrase) > 50:
        await msg.reply("Testo troppo lungo")
        return

    text0 = ""
    text1 = ""
    text2 = ""

    if phrase == "":
        if not msg.room.is_private:
            return
        phrase = "SHITPOST"

    if not msg.room.is_private and ("x" in phrase or "X" in phrase):
        phrase = "lolno"

    for i in phrase:
        if i in LETTERS:
            if text0 != "":
                text0 += " "
                text1 += " "
                text2 += " "
            text0 += LETTERS[i][0]
            text1 += LETTERS[i][1]
            text2 += LETTERS[i][2]

    html = '<pre style="margin: 0; overflow-x: auto">{}<br>{}<br>{}</pre>'

    await msg.reply_htmlbox(html.format(text0, text1, text2))


@command_wrapper(aliases=("meme", "memes", "mims"))
async def memes(msg: Message) -> None:
    if msg.room is None or not msg.room.is_private:
        return

    await msg.reply(random.choice(MEMES))


# fmt: off
LETTERS: Dict[str, List[str]] = {
    "a": [
        "┌─┐",
        "├─┤",
        "┴ ┴",
    ],
    "b": [
        "┌┐ ",
        "├┴┐",
        "└─┘",
    ],
    "c": [
        "┌─┐",
        "│  ",
        "└─┘",
    ],
    "d": [
        "┌┬┐",
        " ││",
        "─┴┘",
    ],
    "e": [
        "┌─┐",
        "├┤ ",
        "└─┘",
    ],
    "f": [
        "┌─┐",
        "├┤ ",
        "└  ",
    ],
    "g": [
        "┌─┐",
        "│ ┬",
        "└─┘",
    ],
    "h": [
        "┬ ┬",
        "├─┤",
        "┴ ┴",
    ],
    "i": [
        "┬",
        "│",
        "┴",
    ],
    "j": [
        " ┬",
        " │",
        "└┘",
    ],
    "k": [
        "┬┌─",
        "├┴┐",
        "┴ ┴",
    ],
    "l": [
        "┬  ",
        "│  ",
        "┴─┘",
    ],
    "m": [
        "┌┬┐",
        "│││",
        "┴ ┴",
    ],
    "n": [
        "┌┐┌",
        "│││",
        "┘└┘",
    ],
    "o": [
        "┌─┐",
        "│ │",
        "└─┘",
    ],
    "p": [
        "┌─┐",
        "├─┘",
        "┴  ",
    ],
    "q": [
        "┌─┐ ",
        "│─┼┐",
        "└─┘└",
    ],
    "r": [
        "┬─┐",
        "├┬┘",
        "┴└─",
    ],
    "s": [
        "┌─┐",
        "└─┐",
        "└─┘",
    ],
    "t": [
        "┌┬┐",
        " │ ",
        " ┴ ",
    ],
    "u": [
        "┬ ┬",
        "│ │",
        "└─┘",
    ],
    "v": [
        "┬  ┬",
        "└┐┌┘",
        " └┘ ",
    ],
    "w": [
        "┬ ┬",
        "│││",
        "└┴┘",
    ],
    "x": [
        "─┐ ┬",
        "┌┴┬┘",
        "┴ └─",
    ],
    "y": [
        "┬ ┬",
        "└┬┘",
        " ┴ ",
    ],
    "z": [
        "┌─┐",
        "┌─┘",
        "└─┘",
    ],
    "A": [
        "╔═╗",
        "╠═╣",
        "╩ ╩",
    ],
    "B": [
        "╔╗ ",
        "╠╩╗",
        "╚═╝",
    ],
    "C": [
        "╔═╗",
        "║  ",
        "╚═╝",
    ],
    "D": [
        "╔╦╗",
        " ║║",
        "═╩╝",
    ],
    "E": [
        "╔═╗",
        "╠╣ ",
        "╚═╝",
    ],
    "F": [
        "╔═╗",
        "╠╣ ",
        "╚  ",
    ],
    "G": [
        "╔═╗",
        "║ ╦",
        "╚═╝",
    ],
    "H": [
        "╦ ╦",
        "╠═╣",
        "╩ ╩",
    ],
    "I": [
        "╦",
        "║",
        "╩",
    ],
    "J": [
        " ╦",
        " ║",
        "╚╝",
    ],
    "K": [
        "╦╔═",
        "╠╩╗",
        "╩ ╩",
    ],
    "L": [
        "╦  ",
        "║  ",
        "╩═╝",
    ],
    "M": [
        "╔╦╗",
        "║║║",
        "╩ ╩",
    ],
    "N": [
        "╔╗╔",
        "║║║",
        "╝╚╝",
    ],
    "O": [
        "╔═╗",
        "║ ║",
        "╚═╝",
    ],
    "P": [
        "╔═╗",
        "╠═╝",
        "╩  ",
    ],
    "Q": [
        "╔═╗ ",
        "║═╬╗",
        "╚═╝╚",
    ],
    "R": [
        "╦═╗",
        "╠╦╝",
        "╩╚═",
    ],
    "S": [
        "╔═╗",
        "╚═╗",
        "╚═╝",
    ],
    "T": [
        "╔╦╗",
        " ║ ",
        " ╩ ",
    ],
    "U": [
        "╦ ╦",
        "║ ║",
        "╚═╝",
    ],
    "V": [
        "╦  ╦",
        "╚╗╔╝",
        " ╚╝ ",
    ],
    "W": [
        "╦ ╦",
        "║║║",
        "╚╩╝",
    ],
    "X": [
        "═╗ ╦",
        "╔╩╦╝",
        "╩ ╚═",
    ],
    "Y": [
        "╦ ╦",
        "╚╦╝",
        " ╩ ",
    ],
    "Z": [
        "╔═╗",
        "╔═╝",
        "╚═╝",
    ],
    "0": [
        "╔═╗",
        "║ ║",
        "╚═╝",
    ],
    "1": [
        "╗",
        "║",
        "╩",
    ],
    "2": [
        "╔═╗",
        "╔═╝",
        "╚═╝",
    ],
    "3": [
        "╔═╗",
        " ═╣",
        "╚═╝",
    ],
    "4": [
        "╦ ╦",
        "╚═╣",
        "  ╩",
    ],
    "5": [
        "╔═╗",
        "╚═╗",
        "╚═╝",
    ],
    "6": [
        "╔═╗",
        "╠═╗",
        "╚═╝",
    ],
    "7": [
        "═╗",
        " ║",
        " ╩",
    ],
    "8": [
        "╔═╗",
        "╠═╣",
        "╚═╝",
    ],
    "9": [
        "╔═╗",
        "╚═╣",
        "╚═╝",
    ],
    " ": [
        "  ",
        "  ",
        "  ",
    ],
    "!": [
        "║",
        "║",
        "▫",
    ],
    "\"": [
        "╚╚",
        "  ",
        "  ",
    ],
    "£": [
        "╔═╗",
        "╬═ ",
        "╩══",
    ],
    "$": [
        "╔╬╗",
        "╚╬╗",
        "╚╬╝",
    ],
    "%": [
        "▫ ╦ ",
        " ╔╝ ",
        " ╩ ▫",
    ],
    "\\": [
        "╦ ",
        "╚╗",
        " ╩",
    ],
    "(": [
        "╔",
        "║",
        "╚",
    ],
    ")": [
        "╗",
        "║",
        "╝",
    ],
    "=": [
        "  ",
        "══",
        "══",
    ],
    "'": [
        "╚",
        " ",
        " ",
    ],
    "?": [
        "╔═╗",
        " ╔╝",
        " ▫ ",
    ],
    "/": [
        " ╦",
        "╔╝",
        "╩ ",
    ],
    "|": [
        "║",
        "║",
        "║",
    ],
    "-": [
        "  ",
        "══",
        "  ",
    ],
    "+": [
        " ║ ",
        "═╬═",
        " ║ ",
    ],
    ":": [
        "╗",
        " ",
        "╗",
    ],
    ".": [
        " ",
        " ",
        "╗",
    ],
    "_": [
        "   ",
        "   ",
        "═══",
    ],
    "[": [
        "╔",
        "║",
        "╚",
    ],
    "]": [
        "╗",
        "║",
        "╝",
    ],
    "{": [
        "╔",
        "╣",
        "╚",
    ],
    "}": [
        "╗",
        "╠",
        "╝",
    ],
    "#": [
        "  ",
        "╬╬",
        "╬╬",
    ],
    "~": [
        "   ",
        "╔═╝",
        "   ",
    ],
    ",": [
        " ",
        " ",
        "╗",
    ],
    ";": [
        "╗",
        " ",
        "╗",
    ],
    "°": [
        "┌┐",
        "└┘",
        "  ",
    ],
}
# fmt: on


with open("./data/memes.json", "r") as f:
    MEMES = json.load(f)
