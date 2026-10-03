"""
main_window.py — Ventana principal + Controlador MVC.
"""

import customtkinter as ctk
from crud import PlayerManager
from views.components import FormPanel, PlayerList
from views.theme import *

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class MainWindow(ctk.CTk):

    def __init__(self) -> None:
        super().__init__()
        self._manager     = PlayerManager()
        self._selected_id = None
        self._configure_window()
        self._build_layout()

    def _configure_window(self) -> None:
        self.title("⛏  Minecraft Tournament  |  Registro de Jugadores")
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.minsize(WIN_MIN_W, WIN_MIN_H)
        self.configure(fg_color=BG_OBSIDIAN)
        try:
            self.iconbitmap("assets/icon.ico")
        except Exception:
            pass
        self.lift()
        self.attributes("-topmost", True)
        self.after(250, lambda: self.attributes("-topmost", False))
        self.focus_force()

    def _build_layout(self) -> None:
        self.columnconfigure(0, weight=0, minsize=330)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._form = FormPanel(
            self,
            on_create=self._handle_create,
            on_update=self._handle_update,
            on_recall=self._handle_recall,
            on_delete=self._handle_delete,
            on_clear =self._handle_clear,
        )
        self._form.grid(row=0, column=0, sticky="nsew")

        self._list = PlayerList(self, on_select=self._handle_select)
        self._list.grid(row=0, column=1, sticky="nsew")

        self._refresh_list()

    # ── Handlers ──────────────────────────────────────────────────────────────

    def _handle_create(self, tag: str, email: str) -> None:
        try:
            p = self._manager.create(tag, email)
            self._form.set_status(f"¡Jugador '{p['tag']}' inscrito exitosamente!", BTN_CREATE_BG)
            self._form.clear_fields()
            self._selected_id = None
            self._form.set_selected(None)
            self._refresh_list()
        except ValueError as exc:
            self._form.set_status(str(exc), BTN_DELETE_BG)

    def _handle_update(self, tag: str, email: str) -> None:
        if not self._selected_id:
            self._form.set_status("Selecciona un jugador antes de actualizar.", BTN_UPDATE_BG)
            return
        try:
            p = self._manager.update(self._selected_id, tag, email)
            self._form.set_status(f"Jugador actualizado → '{p['tag']}'", BTN_UPDATE_BG)
            self._refresh_list()
        except ValueError as exc:
            self._form.set_status(str(exc), BTN_DELETE_BG)

    def _handle_recall(self) -> None:
        if not self._selected_id:
            self._form.set_status("Selecciona un jugador para recordarlo.", BTN_RECALL_BG)
            return
        p = self._manager.get_by_id(self._selected_id)
        if p:
            self._form.set_fields(p["tag"], p["email"])
            self._form.set_status(f"Datos de '{p['tag']}' cargados en el formulario.", BTN_RECALL_BG)

    def _handle_delete(self) -> None:
        if not self._selected_id:
            self._form.set_status("Selecciona un jugador para eliminar.", BTN_DELETE_BG)
            return
        try:
            p = self._manager.delete(self._selected_id)
            self._form.set_status(f"Jugador '{p['tag']}' eliminado del torneo.", BTN_DELETE_BG)
            self._form.clear_fields()
            self._selected_id = None
            self._form.set_selected(None)
            self._refresh_list()
        except ValueError as exc:
            self._form.set_status(str(exc), BTN_DELETE_BG)

    def _handle_clear(self) -> None:
        self._selected_id = None
        self._form.clear_fields()
        self._form.set_selected(None)
        self._form.set_status("Selección y campos limpiados.")
        self._refresh_list()

    def _handle_select(self, player_id: str) -> None:
        if self._selected_id == player_id:
            self._selected_id = None
            self._form.set_selected(None)
            self._form.set_status("Selección eliminada.")
        else:
            self._selected_id = player_id
            p = self._manager.get_by_id(player_id)
            if p:
                self._form.set_selected(p["tag"])
                self._form.set_status(
                    f"'{p['tag']}' seleccionado. Usa RECORDAR para cargar sus datos.", TEXT_WHITE)
        self._refresh_list()

    def _refresh_list(self) -> None:
        self._list.refresh(self._manager.get_all(), selected_id=self._selected_id)
