import sqlite3
from typing import List, Dict, Tuple

import telethon.tl.types

from utils.chat_aux import get_sender_name


def add_lobby_to_db(con: sqlite3.Connection, cur: sqlite3.Cursor, lobby_id: int, owner_id: int, chat_id: int, game: str,
                    participant: int, ping_id: int, in_lobby: bool) -> None:
    """Adds every pinged user for lobby to database"""
    cur.execute("INSERT INTO lobbies(lobbyid, ownerid, chatid, game, participant, ping, in_lobby) "
                "VALUES (?,?,?,?,?,?,?)", (lobby_id, owner_id, chat_id, game, participant, ping_id, in_lobby))
    con.commit()


def remove_lobby_from_db(con: sqlite3.Connection, cur: sqlite3.Cursor, lobby_id: int, chat_id):
    cur.execute("""DELETE FROM lobbies WHERE lobbyid == ? AND chatid == ?""", (lobby_id, chat_id,))
    con.commit()


async def get_lobby(cur: sqlite3.Cursor, event: telethon.events.CallbackQuery) -> List[Dict]:
    """Gets all lobby from database and format it friendly way"""
    lobby_msg = await event.get_message()
    lobby = cur.execute("SELECT lobbyid, ownerid, chatid, game, participant, ping, in_lobby "
                        "FROM lobbies WHERE lobbyid == ? AND chatid == ?",
                        (lobby_msg.id, event.chat.id,)).fetchall()
    keys = [x[0] for x in cur.description]
    return [{keys[0]: user[0],
             keys[1]: user[1],
             keys[2]: user[2],
             keys[3]: user[3],
             keys[4]: user[4],
             keys[5]: user[5],
             keys[6]: user[6]} for user in lobby] if lobby else [{'error': 'lobby does not exist in database'}]


async def get_lobby_participants(cur: sqlite3.Cursor, event: telethon.events.CallbackQuery, in_lobby: bool) -> List[
    Dict]:
    """Gets only in lobby participants from database and format it friendly way"""
    lobby_msg = await event.get_message()
    lobby = cur.execute("SELECT lobbyid, ownerid, chatid, game, participant, ping, in_lobby "
                        "FROM lobbies WHERE lobbyid == ? AND chatid == ? AND in_lobby == ?",
                        (lobby_msg.id, event.chat.id, in_lobby,)).fetchall()
    keys = [x[0] for x in cur.description]
    return [{keys[0]: user[0],
             keys[1]: user[1],
             keys[2]: user[2],
             keys[3]: user[3],
             keys[4]: user[4]} for user in lobby] if lobby else [{'error': 'lobby does not exist in database'}]


def get_lobby_game(cur: sqlite3.Cursor, event: telethon.events.CallbackQuery) -> str:
    # TODO: Code it
    ...


async def get_lobby_owner(cur: sqlite3.Cursor, event: telethon.events.CallbackQuery) -> int:
    lobby_msg = await event.get_message()
    return cur.execute("SELECT ownerid FROM lobbies WHERE lobbyid == ? AND chatid == ? AND ownerid == participant",
                       (lobby_msg.id, event.chat.id,)).fetchone()[0]


def is_in_lobby(userid: int, lobby: List) -> bool:
    """Checks if user is in lobby"""
    return userid in [user['participant'] for user in lobby if user['in_lobby']]


def change_lobby_participants(con: sqlite3.Connection, cur: sqlite3.Cursor, userid: int, lobbyid: int, joined: bool):
    """Changes in_lobby parameter to True/False for a specified userid and lobbyid, depends on join/leave"""
    cur.execute("""UPDATE lobbies SET in_lobby = ? WHERE participant == ? AND lobbyid == ?""",
                (joined, userid, lobbyid))
    con.commit()


def is_lobby_empty(lobby: List) -> bool:
    """Checks if lobby is empty"""
    return not any((user['in_lobby'] for user in lobby))


async def parse_lobby(cur: sqlite3.Cursor, event: telethon.events.CallbackQuery) -> str:
    lobby_msg = await event.get_message()
    lobby_id = lobby_msg.id
    lobby = await get_lobby(cur=cur, event=event)

    ...
    return str()
