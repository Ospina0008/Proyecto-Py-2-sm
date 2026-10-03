"""
player_list.py — Panel derecho: tabla dinámica de jugadores inscritos.
"""

import customtkinter as ctk
from views.theme import *

_HEADERS = ("#", "GAMERTAG", "CORREO ELECTRÓNICO")
_COL_W   = (40, 180, 260)


class PlayerList(ctk.CTkFrame):

    def __init__(self, master, on_select=None, **kwargs):
        super().__init__(master, fg_color=BG_STONE, corner_radius=CORNER_BLOCK,
                         border_width=BORDER_WIDTH, border_color=BORDER_COLOR, **kwargs)
        self._on_select   = on_select or (lambda pid: None)
        self._selected_id = None
        self._row_widgets: list = []
        self.columnconfigure(0, weight=1)
        self._build_skeleton()

    def _build_skeleton(self) -> None:
        # Título
        title_bar = ctk.CTkFrame(self, fg_color=BG_OBSIDIAN, corner_radius=CORNER_BLOCK)
        title_bar.grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(title_bar, text="🗂  JUGADORES INSCRITOS",
                     font=FONT_HEADER, text_color=BTN_UPDATE_BG).pack(side="left", padx=PAD_X, pady=PAD_SM)
        self._lbl_count = ctk.CTkLabel(title_bar, text="[ 0 jugadores ]",
                                       font=FONT_SMALL, text_color=TEXT_GRAY)
        self._lbl_count.pack(side="right", padx=PAD_X, pady=PAD_SM)

        ctk.CTkFrame(self, height=2, fg_color=BORDER_COLOR,
                     corner_radius=0).grid(row=1, column=0, sticky="ew")

        # Cabecera de columnas
        hf = ctk.CTkFrame(self, fg_color="#242424", corner_radius=CORNER_BLOCK)
        hf.grid(row=2, column=0, sticky="ew")
        for col, (txt, w) in enumerate(zip(_HEADERS, _COL_W)):
            ctk.CTkLabel(hf, text=txt, font=FONT_SMALL, text_color=BTN_UPDATE_BG,
                         width=w, anchor="w"
                         ).grid(row=0, column=col,
                                padx=(PAD_X if col == 0 else PAD_SM), pady=PAD_SM, sticky="w")

        ctk.CTkFrame(self, height=2, fg_color=BORDER_COLOR,
                     corner_radius=0).grid(row=3, column=0, sticky="ew")

        # Área scrollable
        self._scroll = ctk.CTkScrollableFrame(
            self, fg_color=BG_STONE, corner_radius=CORNER_BLOCK,
            scrollbar_button_color=BORDER_COLOR,
            scrollbar_button_hover_color=BTN_CLEAR_BG,
        )
        self._scroll.grid(row=4, column=0, sticky="nsew")
        self.rowconfigure(4, weight=1)
        self._scroll.columnconfigure(0, weight=1)

        self._lbl_empty = ctk.CTkLabel(
            self._scroll,
            text="\n\n  [ Lista vacía ]\n\n  Inscribe un jugador usando\n  el formulario de la izquierda.\n",
            font=FONT_BODY, text_color=TEXT_GRAY, justify="left",
        )
        self._lbl_empty.grid(row=0, column=0, sticky="nsew", padx=PAD_X, pady=PAD_Y)

    def refresh(self, players: list[dict], selected_id: str = None) -> None:
        self._selected_id = selected_id
        for widgets in self._row_widgets:
            widgets[0].destroy()
        self._row_widgets.clear()

        n = len(players)
        self._lbl_count.configure(text=f"[ {n} jugador{'es' if n != 1 else ''} ]")

        if not players:
            self._lbl_empty.grid()
            return

        self._lbl_empty.grid_remove()
        for idx, player in enumerate(players):
            self._add_row(idx, player)

    def _add_row(self, idx: int, player: dict) -> None:
        pid    = player["id"]
        is_sel = pid == self._selected_id
        row_bg = "#3A5C3A" if is_sel else ("#2A2A2A" if idx % 2 == 0 else BG_STONE)
        tc     = BTN_CREATE_BG if is_sel else TEXT_WHITE

        rf = ctk.CTkFrame(self._scroll, fg_color=row_bg,
                          corner_radius=CORNER_BLOCK, cursor="hand2")
        rf.grid(row=idx, column=0, sticky="ew", padx=0, pady=1)
        rf.columnconfigure(1, weight=1)

        n_lbl = ctk.CTkLabel(rf, text=f"  {idx+1:02d}", font=FONT_SMALL,
                             text_color=TEXT_GRAY, width=_COL_W[0], anchor="w")
        n_lbl.grid(row=0, column=0, padx=(PAD_X, 0), pady=PAD_SM, sticky="w")

        tag_lbl = ctk.CTkLabel(rf, text=player["tag"], font=FONT_BODY,
                               text_color=tc, width=_COL_W[1], anchor="w")
        tag_lbl.grid(row=0, column=1, padx=PAD_SM, pady=PAD_SM, sticky="w")

        email_lbl = ctk.CTkLabel(rf, text=player["email"], font=FONT_SMALL,
                                 text_color=BTN_CREATE_BG if is_sel else TEXT_GRAY,
                                 width=_COL_W[2], anchor="w")
        email_lbl.grid(row=0, column=2, padx=(PAD_SM, PAD_X), pady=PAD_SM, sticky="w")

        for w in (rf, n_lbl, tag_lbl, email_lbl):
            w.bind("<Button-1>", lambda e, p=pid: self._on_select(p))

        self._row_widgets.append([rf, n_lbl, tag_lbl, email_lbl])
