"""
player_manager.py — Lógica CRUD en RAM (sin GUI, sin persistencia).
"""

import uuid
import re
from typing import Optional


class PlayerManager:
    _EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    _TAG_MIN  = 3
    _TAG_MAX  = 24

    def __init__(self) -> None:
        self._players: list[dict] = []

    def get_all(self) -> list[dict]:
        return list(self._players)

    def get_by_id(self, player_id: str) -> Optional[dict]:
        for player in self._players:
            if player["id"] == player_id:
                return dict(player)
        return None

    def create(self, tag: str, email: str) -> dict:
        tag, email = self._validate(tag, email)
        self._assert_unique_tag(tag)
        self._assert_unique_email(email)
        player = {"id": str(uuid.uuid4()), "tag": tag, "email": email}
        self._players.append(player)
        return dict(player)

    def update(self, player_id: str, tag: str, email: str) -> dict:
        tag, email = self._validate(tag, email)
        index = self._find_index(player_id)
        for i, p in enumerate(self._players):
            if i == index:
                continue
            if p["tag"].lower() == tag.lower():
                raise ValueError(f"El gamertag '{tag}' ya está registrado por otro jugador.")
            if p["email"].lower() == email.lower():
                raise ValueError(f"El correo '{email}' ya está registrado por otro jugador.")
        self._players[index]["tag"]   = tag
        self._players[index]["email"] = email
        return dict(self._players[index])

    def delete(self, player_id: str) -> dict:
        index = self._find_index(player_id)
        return self._players.pop(index)

    def _validate(self, tag: str, email: str) -> tuple[str, str]:
        tag   = tag.strip()
        email = email.strip()
        if not tag:
            raise ValueError("El Gamertag no puede estar vacío.")
        if len(tag) < self._TAG_MIN:
            raise ValueError(f"El Gamertag debe tener al menos {self._TAG_MIN} caracteres.")
        if len(tag) > self._TAG_MAX:
            raise ValueError(f"El Gamertag no puede superar los {self._TAG_MAX} caracteres.")
        if not email:
            raise ValueError("El correo electrónico no puede estar vacío.")
        if not self._EMAIL_RE.match(email):
            raise ValueError("El correo electrónico no tiene un formato válido.")
        return tag, email

    def _find_index(self, player_id: str) -> int:
        for i, p in enumerate(self._players):
            if p["id"] == player_id:
                return i
        raise ValueError(f"Jugador con ID '{player_id}' no encontrado.")

    def _assert_unique_tag(self, tag: str) -> None:
        for p in self._players:
            if p["tag"].lower() == tag.lower():
                raise ValueError(f"El gamertag '{tag}' ya está registrado.")

    def _assert_unique_email(self, email: str) -> None:
        for p in self._players:
            if p["email"].lower() == email.lower():
                raise ValueError(f"El correo '{email}' ya está registrado.")
