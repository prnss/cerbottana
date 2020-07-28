from __future__ import annotations

import queue
from datetime import date, datetime
from functools import wraps
from typing import Callable, Optional

from environs import Env
from flask import Flask, abort, current_app, g, render_template, request
from flask import session as web_session
from sqlalchemy.sql import func
from waitress import serve

import databases.database as d
import utils
from database import Database
from plugins import routes

env = Env()
env.read_env()


class Server(Flask):
    def __init__(self, *args, **kwargs) -> None:  # type:ignore
        super().__init__(*args, **kwargs)
        self.queue: Optional[queue.SimpleQueue[str]] = None

    def serve_forever(self, queue: queue.SimpleQueue[str]) -> None:
        self.queue = queue
        serve(self, listen="*:{}".format(env("PORT")))


SERVER = Server(__name__)

SERVER.secret_key = env("FLASK_SECRET_KEY")


@SERVER.template_filter("format_date")
def format_date(value: str) -> str:
    return date.fromisoformat(value).strftime("%d/%m/%Y")


@SERVER.template_filter("format_datetime")
def format_datetime(value: str) -> str:
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f").strftime(
        "%d/%m/%Y %H:%M:%S"
    )


@SERVER.before_request
def before() -> None:
    g.db = Database.open()

    token = request.args.get("token")

    if token is not None:
        with g.db.get_session() as session:
            data = (
                session.query(d.Tokens)
                .filter_by(token=token)
                .filter(func.julianday() - func.julianday(d.Tokens.expiry) < 0)
                .all()
            )
            if not data:  # invalid token
                abort(401)
            for row in data:
                if row.room is None:
                    web_session["_rank"] = row.rank
                else:
                    web_session[row.room] = row.rank


def require_driver(func: Callable[[], str]) -> Callable[[], str]:
    @wraps(func)
    def wrapper() -> str:
        if not utils.is_driver(web_session.get("_rank")):
            abort(401)
        return func()

    return wrapper


@SERVER.route("/", methods=("GET", "POST"))
@require_driver
def dashboard() -> str:

    current_app.queue.put("aaa", False)

    with g.db.get_session() as session:
        if request.method == "POST":

            if "approva" in request.form:
                parts = request.form["approva"].split(",")
                session.query(d.Users).filter_by(
                    id=parts[0], description_pending=",".join(parts[1:])
                ).update(
                    {
                        "description": d.Users.description_pending,
                        "description_pending": "",
                    }
                )

            if "rifiuta" in request.form:
                parts = request.form["rifiuta"].split(",")
                session.query(d.Users).filter_by(
                    id=parts[0], description_pending=",".join(parts[1:]),
                ).update({"description_pending": ""})

        descriptions_pending = (
            session.query(d.Users)
            .filter(d.Users.description_pending != "")
            .order_by(d.Users.userid)
            .all()
        )

        return render_template(
            "dashboard.html", descriptions_pending=descriptions_pending
        )


for view_func, rule, methods in routes:
    SERVER.add_url_rule(rule, view_func=view_func, methods=methods)
