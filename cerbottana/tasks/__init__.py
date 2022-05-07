from __future__ import annotations

import importlib
from collections.abc import Callable, Coroutine
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cerbottana.connection import Connection

    InitTaskFunc = Callable[[Connection], Coroutine[None, None, None]]
    RecurringTaskFunc = Callable[[Connection], Coroutine[None, None, None]]


init_tasks: list[tuple[int, InitTaskFunc, bool]] = []


def init_task_wrapper(
    *, priority: int = 3, skip_unittesting: bool = False
) -> Callable[[InitTaskFunc], InitTaskFunc]:
    def wrapper(func: InitTaskFunc) -> InitTaskFunc:
        init_tasks.append((priority, func, skip_unittesting))
        return func

    return wrapper


recurring_tasks: list[RecurringTaskFunc] = []


def recurring_task_wrapper() -> Callable[[RecurringTaskFunc], RecurringTaskFunc]:
    def wrapper(func: RecurringTaskFunc) -> RecurringTaskFunc:
        recurring_tasks.append(func)
        return func

    return wrapper


modules = Path(__file__).parent.glob("*.py")

for f in modules:
    if f.is_file() and f.name != "__init__.py":
        name = f.stem
        importlib.import_module(f".{name}", __name__)
