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
