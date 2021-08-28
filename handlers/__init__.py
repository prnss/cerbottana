from __future__ import annotations

import glob
import importlib
from collections.abc import Awaitable, Callable
from functools import wraps
from os.path import basename, dirname, isfile, join
from typing import TYPE_CHECKING, NamedTuple

if TYPE_CHECKING:
    from models.protocol_message import ProtocolMessage

    HandlerFunc = Callable[[ProtocolMessage], Awaitable[None]]


class HandlerTuple(NamedTuple):
    callback: HandlerFunc
    required_parameters: int | None


handlers: dict[str, list[HandlerTuple]] = {}


def handler_wrapper(
    message_types: list[str], *, required_parameters: int | None = None
) -> Callable[[HandlerFunc], HandlerFunc]:
    def cls_wrapper(func: HandlerFunc) -> HandlerFunc:
        if required_parameters:
            func = check_required_parameters(func, required_parameters)
        for message_type in message_types:
            if message_type not in handlers:
                handlers[message_type] = []
            handlers[message_type].append(HandlerTuple(func, required_parameters))
        return func

    return cls_wrapper


def check_required_parameters(
    func: HandlerFunc, required_parameters: int
) -> HandlerFunc:
    @wraps(func)
    async def wrapper(msg: ProtocolMessage) -> None:
        if len(msg.params) < required_parameters:
            return
        await func(msg)

    return wrapper


modules = glob.glob(join(dirname(__file__), "*.py"))

for f in modules:
    if isfile(f) and not f.endswith("__init__.py"):
        name = basename(f)[:-3]
        importlib.import_module("handlers." + name)
