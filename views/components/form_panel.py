"""
form_panel.py — Panel izquierdo: formulario CRUD con tema Minecraft.
"""

import customtkinter as ctk
from views.theme import *


class FormPanel(ctk.CTkFrame):

    def __init__(self, master, **callbacks):
        super().__init__(
            master,
            fg_color=BG_STONE,
            corner_radius=CORNER_BLOCK,
            border_width=BORDER_WIDTH,
            border_color=BORDER_COLOR,
        )
        self._cb_create = callbacks.get("on_create", lambda t, e: None)
        self._cb_update = callbacks.get("on_update", lambda t, e: None)
        self._cb_recall = callbacks.get("on_recall", lambda: None)
        self._cb_delete = callbacks.get("on_delete", lambda: None)
        self._cb_clear  = callbacks.get("on_clear",  lambda: None)
        self._build_ui()

    def _build_ui(self) -> None:
        self.columnconfigure(0, weight=1)

        # Título
        title_bar = ctk.CTkFrame(self, fg_color=BG_OBSIDIAN, corner_radius=CORNER_BLOCK)
        title_bar.grid(row=0, column=0, sticky="ew", pady=(0, PAD_Y))
        ctk.CTkLabel(title_bar, text="⛏  MINECRAFT  TOURNAMENT",
                     font=FONT_TITLE, text_color=BTN_CREATE_BG).pack(pady=PAD_Y)
        ctk.CTkLabel(title_bar, text="[ SERVER REGISTRATION ]",
                     font=FONT_SMALL, text_color=TEXT_GRAY).pack(pady=(0, PAD_SM))

        self._sep(1)

        # Gamertag
        self._lbl(2, "▶  GAMERTAG  (Nombre de Jugador)")
        self._tag_var   = ctk.StringVar()
        self._entry_tag = self._entry(3, self._tag_var, "Steve_2025")

        # Email
        self._lbl(4, "▶  CORREO ELECTRÓNICO")
        self._email_var   = ctk.StringVar()
        self._entry_email = self._entry(5, self._email_var, "steve@minecraft.net")

        self._sep(6)

        # Botones
        bf = ctk.CTkFrame(self, fg_color="transparent")
        bf.grid(row=7, column=0, sticky="ew", padx=PAD_X, pady=PAD_SM)
        bf.columnconfigure((0, 1), weight=1)

        self._mkbtn(bf, 0, 0, "⚡  INSCRIBIR",   BTN_CREATE_BG, BTN_CREATE_HV, TEXT_DARK,  self._on_create)
        self._mkbtn(bf, 0, 1, "✏  ACTUALIZAR",  BTN_UPDATE_BG, BTN_UPDATE_HV, TEXT_DARK,  self._on_update)
        self._mkbtn(bf, 1, 0, "🔍  RECORDAR",   BTN_RECALL_BG, BTN_RECALL_HV, TEXT_WHITE, self._cb_recall)
        self._mkbtn(bf, 1, 1, "🗑  ELIMINAR",   BTN_DELETE_BG, BTN_DELETE_HV, TEXT_WHITE, self._cb_delete)
        ctk.CTkButton(bf, text="✖  LIMPIAR SELECCIÓN", font=FONT_BTN,
                      fg_color=BTN_CLEAR_BG, hover_color=BTN_CLEAR_HV,
                      text_color=TEXT_WHITE, corner_radius=CORNER_BLOCK,
                      command=self._cb_clear
                      ).grid(row=2, column=0, columnspan=2, sticky="ew",
                             padx=PAD_SM, pady=(PAD_SM, 0))

        self._sep(8)

        # Panel de estado
        status_frame = ctk.CTkFrame(self, fg_color=BG_OBSIDIAN,
                                    corner_radius=CORNER_BLOCK,
                                    border_width=BORDER_WIDTH, border_color=BORDER_COLOR)
        status_frame.grid(row=9, column=0, sticky="ew", padx=PAD_X, pady=PAD_SM)
        ctk.CTkLabel(status_frame, text=" CONSOLA  DE  ESTADO ",
                     font=FONT_SMALL, text_color=TEXT_GRAY).pack(anchor="w", padx=PAD_SM, pady=(PAD_SM, 0))
        self._status_var = ctk.StringVar(value="> Esperando acción...")
        self._lbl_status = ctk.CTkLabel(status_frame, textvariable=self._status_var,
                                        font=FONT_BODY, text_color=BTN_CREATE_BG,
                                        wraplength=280, justify="left")
        self._lbl_status.pack(anchor="w", padx=PAD_SM, pady=(0, PAD_SM))

        # Indicador selección
        self._sel_var = ctk.StringVar(value="[ Sin selección ]")
        ctk.CTkLabel(self, textvariable=self._sel_var,
                     font=FONT_SMALL, text_color=TEXT_GRAY
                     ).grid(row=10, column=0, sticky="ew", padx=PAD_X, pady=(PAD_SM, PAD_Y))

    def _sep(self, row: int) -> None:
        ctk.CTkFrame(self, height=2, fg_color=BORDER_COLOR,
                     corner_radius=0).grid(row=row, column=0, sticky="ew", pady=PAD_SM)

    def _lbl(self, row: int, text: str) -> None:
        ctk.CTkLabel(self, text=text, font=FONT_SMALL,
                     text_color=TEXT_GRAY, anchor="w"
                     ).grid(row=row, column=0, sticky="ew", padx=PAD_X, pady=(PAD_SM, 0))

    def _entry(self, row: int, var, placeholder: str) -> ctk.CTkEntry:
        e = ctk.CTkEntry(self, textvariable=var, placeholder_text=placeholder,
                         placeholder_text_color=TEXT_GRAY, font=FONT_BODY,
                         fg_color=BG_STONE_LIGHT, text_color=TEXT_WHITE,
                         border_color=BORDER_COLOR, border_width=BORDER_WIDTH,
                         corner_radius=CORNER_BLOCK)
        e.grid(row=row, column=0, sticky="ew", padx=PAD_X, pady=(0, PAD_SM))
        return e

    def _mkbtn(self, parent, row, col, text, fg, hv, tc, cmd) -> ctk.CTkButton:
        b = ctk.CTkButton(parent, text=text, font=FONT_BTN,
                          fg_color=fg, hover_color=hv, text_color=tc,
                          corner_radius=CORNER_BLOCK, command=cmd)
        b.grid(row=row, column=col, sticky="ew", padx=PAD_SM, pady=PAD_SM)
        return b

    def _on_create(self): self._cb_create(self._tag_var.get(), self._email_var.get())
    def _on_update(self): self._cb_update(self._tag_var.get(), self._email_var.get())

    # API pública
    def set_fields(self, tag="", email=""):
        self._tag_var.set(tag); self._email_var.set(email)

    def clear_fields(self):
        self._tag_var.set(""); self._email_var.set("")

    def set_status(self, msg: str, color: str = None):
        self._status_var.set(f"> {msg}")
        self._lbl_status.configure(text_color=color or BTN_CREATE_BG)

    def set_selected(self, tag: str = None):
        self._sel_var.set(f"[ Seleccionado: {tag} ]" if tag else "[ Sin selección ]")
