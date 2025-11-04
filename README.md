# Validador y Visualizador de FEN (Tkinter)

Aplicación de escritorio en Python que **valida cadenas FEN** (Forsyth–Edwards Notation) y **dibuja el tablero** con piezas Unicode. Incluye validaciones exhaustivas de los 6 campos FEN y una GUI simple con `tkinter`.

---

## 📌 Objetivos de la práctica

1. Parsear y validar una cadena FEN completa (6 campos).  
2. Detectar y reportar errores con mensajes claros.  
3. Renderizar la posición en un tablero 8×8 usando piezas Unicode.  
4. Mantener el código **sencillo**, **tipado** y **bien estructurado**.

---

## 👥 Autores

- **Sebastián Sánchez Gómez**  
- **Cristóbal Machado Sánchez**

---

## 💻 Entorno

- **Sistema Operativo:** Windows 11 Home, Versión 24H2  
  Instalado: 23 de diciembre de 2024  
  Compilación: 26100.4946  
  Feature Experience Pack: 1000.26100.197.0
- **Windows Subsystem for Linux (WSL):** 2.5.10.0  
  Kernel Linux: 6.6.87.2-1  
  WSLg: 1.0.66
- **Intérprete Prolog:** SWI-Prolog 9.x *(no usado en este script)*
- **Python:** **3.12.x** (recomendado) ✔️

> **Nota:** `tkinter` viene incluido con la instalación estándar de Python en Windows. En WSL, la GUI funciona gracias a **WSLg**.

---

## 🧱 Dependencias

No requiere librerías externas. Solo Python estándar:

- `tkinter` (GUI)
- `typing` (anotaciones)
- `traceback`, `sys` (manejo de errores)

---

## ▶️ Ejecución

1. Asegúrate de tener **Python 3.12** (o 3.11/3.10).  
2. Guarda el archivo como `fen_parser_gui.py`.  
3. Ejecuta en terminal:

```bash
python fen_parser_gui.py
```

La ventana se abrirá con un FEN de ejemplo precargado.  
Pulsa **“Validar y Dibujar”** para renderizar o **“Limpiar”** para reiniciar.

---

## 🧠 ¿Qué valida exactamente?

El FEN debe tener **6 campos** separados por espacios:

1. **Colocación de piezas** (8 filas separadas por `/`)  
   - Cada fila:
     - Puede ser exactamente `'8'` (fila vacía completa), o
     - Secuencias de piezas `[KQRBNPkqrbnp]` y números `1..7` (los dígitos expanden casillas vacías).  
   - **Nunca** más de 8 casillas por fila ni menos de 8.  
   - Caracteres inválidos → error.

2. **Turno:** `'w'` o `'b'`.

3. **Enroque:** `'-'` o combinación **sin repetidos** de `KQkq` (en cualquier orden).

4. **En passant:** `'-'` o una casilla **a–h** con fila **3** o **6** (ej.: `e3`, `c6`).

5. **Semimovimientos (regla de las 50):** entero **no negativo**.

6. **Número de movimiento:** entero **≥ 1**.

> Si algo falla, se muestra un **MessageBox** con un error claro y el detalle técnico se imprime a `stderr`.

---

## 🧩 Piezas Unicode

Se usan glifos estándar (tipografía recomendada: **DejaVu Sans**):

- Blancas: ♔♕♖♗♘♙  
- Negras: ♚♛♜♝♞♟

Si la fuente no está disponible, se usa una fuente por defecto (puede variar el look & feel).

---

## 🧭 Interfaz

- **Entrada FEN**: `Entry` con ejemplo precargado  
  `2r3k1/p3bqp1/Q2p3p/3Pp3/P3N3/8/5PPP/5RK1 b - - 1 27`
- **Botones**:  
  - **Validar y Dibujar**: parsea, valida y dibuja.  
  - **Limpiar**: borra la entrada y redibuja tablero vacío.
- **Info de posición**: muestra turno, enroques, en passant, semimov y mov total.
- **Tablero**: `Canvas` 480×480, casillas bicolor, coordenadas **a–h** y **1–8**.

---

## 🗺️ Estructura del código

- `PIEZAS_UNICODE`: mapa de letra FEN → glifo Unicode.  
- `expandir_fila(str) -> List[str]`: expande una fila (valida `1..7` y piezas).  
- `parsear_colocacion(str) -> List[List[str]]`: arma la matriz **8×8**.  
- Validadores por campo:
  - `validar_turno`, `validar_enroque`, `validar_en_passant`,
  - `validar_semimov`, `validar_mov_total`.  
- `parsear_fen(str) -> dict`: orquesta todo y devuelve:  
  `{'tablero', 'turno', 'enroque', 'en_passant', 'semimov', 'mov_total'}`  
- `AplicacionFEN` (GUI):
  - `validar()`: integra parseo/validación + mensajes.  
  - `dibujar_tablero(...)` y helpers.  
  - `limpiar()`.

---

## 🧪 Pruebas rápidas (copia y pega)

### ✅ Válidos
- Posición inicial:
  ```
  rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
  ```
- En passant y enroques mixtos:
  ```
  r3k2r/8/8/8/8/8/8/R3K2R b KQkq e3 12 37
  ```

### ❌ Inválidos (deben dar error)
- Fila con `'8'` mezclada (no se permite):  
  ```
  rnbqkbnr/pppppppp/8/8/8/8/PPPPPP8/RNBQKBNR w - - 0 1
  ```
- Dígito `0` o `8` dentro de fila:  
  ```
  8/8/8/8/8/8/8/PPP8 w - - 0 1
  ```

---

## 📜 Licencia

Este proyecto se entrega con fines **académicos** para la práctica de análisis de contratos y validación de cadenas FEN en Python.

---
