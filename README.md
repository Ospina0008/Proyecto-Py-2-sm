# ⛏ Minecraft Tournament — Registro de Jugadores

Aplicación de escritorio CRUD con temática **Minecraft**, construida con
**Python 3.11+** y **CustomTkinter**. Sin base de datos: todos los datos
se almacenan en RAM (listas y diccionarios nativos de Python).

---

## 📂 Estructura del Proyecto

```
minecraft_tournament/
├── main.py                        # Punto de entrada
├── requirements.txt               # Dependencias Python
├── README.md
│
├── crud/
│   ├── __init__.py
│   └── player_manager.py          # Lógica CRUD pura (sin GUI)
│
├── assets/
│   └── (icon.ico opcional)        # Ícono de ventana
│
└── views/
    ├── __init__.py
    ├── theme.py                   # Paleta de colores y constantes Minecraft
    ├── main_window.py             # Ventana principal + Controlador
    └── components/
        ├── __init__.py
        ├── form_panel.py          # Panel izquierdo: formulario CRUD
        └── player_list.py         # Panel derecho: tabla de jugadores
```

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────┐
│                    main.py (entry)                  │
└──────────────────────┬──────────────────────────────┘
                       │ instancia
┌──────────────────────▼──────────────────────────────┐
│              MainWindow  (controlador)               │
│  ┌─────────────────┐        ┌───────────────────┐   │
│  │   FormPanel     │◄──────►│   PlayerList      │   │
│  │  (vista: form)  │        │  (vista: tabla)   │   │
│  └────────┬────────┘        └────────┬──────────┘   │
│           │ callbacks               │ on_select      │
│  ┌────────▼────────────────────────▼──────────┐     │
│  │            PlayerManager  (modelo)          │     │
│  │    Lista[dict] en RAM · CRUD · Validación   │     │
│  └─────────────────────────────────────────────┘     │
└─────────────────────────────────────────────────────┘
```

**Separación de responsabilidades:**

| Capa | Archivo | Responsabilidad |
|------|---------|-----------------|
| Modelo | `crud/player_manager.py` | CRUD, validación, estado en RAM |
| Vista – form | `views/components/form_panel.py` | Campos, botones, panel de estado |
| Vista – lista | `views/components/player_list.py` | Tabla dinámica de jugadores |
| Controlador | `views/main_window.py` | Conecta modelo ↔ vistas |
| Tema | `views/theme.py` | Colores, fuentes, radios |

---

## 🎨 Paleta de Colores Minecraft

| Elemento | Color | Referencia |
|----------|-------|-----------|
| Fondo principal | `#141414` | Obsidiana |
| Fondo paneles | `#303030` | Piedra oscura |
| Botón **Inscribir** | `#55FF55` | Verde Creeper |
| Botón **Actualizar** | `#FFAA00` | Antorcha naranja |
| Botón **Recordar** | `#5555FF` | Diamante azul |
| Botón **Eliminar** | `#FF5555` | Lava roja |
| Bordes | `corner_radius=0` | Aspecto de bloque |
| Fuente | `Consolas` / `Courier New` | Monoespaciada |

---

## 🖥️ Requisitos del Sistema

- **Python 3.11** o superior
- **Windows 10/11** (o macOS/Linux con Tk instalado)
- Conexión a Internet para instalar dependencias la primera vez

---

## ⚡ Instalación y Ejecución

### 1 · Clonar / ubicarse en el directorio del proyecto

```powershell
cd C:\Users\junos\.gemini\antigravity\scratch\minecraft_tournament
```

### 2 · Crear y activar un entorno virtual (recomendado)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

> En **macOS/Linux**:
> ```bash
> python3 -m venv .venv
> source .venv/bin/activate
> ```

### 3 · Instalar dependencias

```powershell
pip install -r requirements.txt
```

### 4 · Ejecutar la aplicación

```powershell
python main.py
```

---

## 🕹️ Guía de Uso

### Inscribir un Jugador (Crear)
1. Escribe el **Gamertag** (3–24 caracteres) en el primer campo.
2. Escribe el **Correo Electrónico** válido en el segundo campo.
3. Haz clic en **⚡ INSCRIBIR**.

### Seleccionar un Jugador
- Haz clic sobre cualquier fila de la tabla derecha.
- La fila se resaltará en **verde** y el indicador de selección se actualizará.
- Un segundo clic en la misma fila **deselecciona** al jugador.

### Recordar datos (Leer)
1. Selecciona un jugador de la lista.
2. Haz clic en **🔍 RECORDAR**.
3. Los campos del formulario se rellenarán con sus datos.

### Actualizar un Jugador
1. Selecciona un jugador y usa **🔍 RECORDAR** para cargar sus datos.
2. Modifica los campos que desees.
3. Haz clic en **✏ ACTUALIZAR**.

### Eliminar un Jugador
1. Selecciona un jugador de la lista.
2. Haz clic en **🗑 ELIMINAR**.

### Limpiar Selección
- Haz clic en **✖ LIMPIAR SELECCIÓN** para vaciar los campos y deseleccionar.

---

## 🔠 Fuente Pixel-Art Personalizada (Opcional)

Para usar una fuente `.ttf` estilo pixel-art (ej. **Press Start 2P**):

1. Descarga la fuente desde [Google Fonts](https://fonts.google.com/specimen/Press+Start+2P)
   y guárdala en `assets/PressStart2P.ttf`.

2. Registra la fuente **antes** de crear la ventana en `main.py`:

```python
from tkinter import font as tkfont

root = ctk.CTk()          # CTk inicializa Tk internamente
tkfont.Font(root=root, family="Press Start 2P")

import ctypes
ctypes.windll.gdi32.AddFontResourceW(r"assets\PressStart2P.ttf")
```

3. Cambia `FONT_MONO` en `views/theme.py`:

```python
FONT_MONO = "Press Start 2P"
```

> **Nota:** las fuentes pixel-art tienen tamaños muy pequeños; ajusta los
> tamaños en `theme.py` (`FONT_TITLE`, `FONT_BODY`, etc.) según necesites.

---

## 📋 Reglas de Validación

| Campo | Regla |
|-------|-------|
| Gamertag | 3–24 caracteres, único en el registro |
| Email | Formato `usuario@dominio.ext`, único en el registro |

---

## 📝 Notas Técnicas

- **Sin persistencia**: al cerrar la aplicación los datos se pierden. Esto es
  intencional según los requisitos del proyecto.
- **Rendimiento**: la ventana principal **nunca** se destruye ni recarga.
  Solo el interior del `CTkScrollableFrame` se repinta en cada acción CRUD.
- El proyecto sigue el patrón **MVC ligero**: modelo (`PlayerManager`),
  vistas (`FormPanel`, `PlayerList`) y controlador (`MainWindow`).
