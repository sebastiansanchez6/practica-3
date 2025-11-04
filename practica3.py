
import tkinter as tk
from tkinter import messagebox, font
import sys
import traceback
from typing import List, Dict

# Mapeo de caracteres FEN a piezas Unicode
PIEZAS_UNICODE: Dict[str, str] = {
    'K': '♔', 'Q': '♕', 'R': '♖', 'B': '♗', 'N': '♘', 'P': '♙',
    'k': '♚', 'q': '♛', 'r': '♜', 'b': '♝', 'n': '♞', 'p': '♟',
    '.': ' ',
}

def expandir_fila(cadena_fila: str) -> List[str]:
    """
    Expande una fila FEN (que NO es '8' completa) a una lista de 8 celdas.
    Regla usada (BNF del enunciado): dentro de la fila, los dígitos válidos son 1..7
    y la fila '8' completa se maneja por fuera como caso especial.
    """
    resultado: List[str] = []
    for caracter in cadena_fila:
        if caracter.isdigit():
            cantidad = int(caracter)
            # Solo 1..7 dentro de una fila (la '8' solo se permite si la fila es exactamente '8')
            if cantidad < 1 or cantidad > 7:
                raise ValueError(f"Número inválido '{caracter}' en la fila (debe ser 1..7, '8' solo si la fila es exactamente '8')")
            resultado.extend(['.'] * cantidad)
        else:
            if caracter not in PIEZAS_UNICODE:
                raise ValueError(f"Carácter de pieza inválido '{caracter}' en la fila")
            resultado.append(caracter)
        if len(resultado) > 8:
            raise ValueError("Una fila tiene más de 8 casillas")
    if len(resultado) != 8:
        raise ValueError("Una fila no tiene exactamente 8 casillas")
    return resultado

def parsear_colocacion(campo: str) -> List[List[str]]:
    """
    Parsea el primer campo de FEN (colocación de piezas) a una matriz 8x8.
    """
    filas = campo.split('/')
    if len(filas) != 8:
        raise ValueError(f"La colocación debe tener 8 filas separadas por '/'. Se encontraron {len(filas)}")
    tablero: List[List[str]] = []
    for fila in filas:
        if fila == '8':
            expandida = ['.'] * 8
        else:
            expandida = expandir_fila(fila)
        tablero.append(expandida)
    return tablero

def validar_turno(campo: str) -> str:
    if campo not in ('w', 'b'):
        raise ValueError("El turno debe ser 'w' o 'b'")
    return campo

def validar_enroque(campo: str) -> str:
    """
    Campo 3: '-' o una combinación SIN repetidos de KQkq (en cualquier orden).
    """
    if campo == '-':
        return campo
    permitidos = set('KQkq')
    vistos = set()
    for ch in campo:
        if ch not in permitidos:
            raise ValueError("Enroque inválido: solo puede contener K, Q, k, q o '-'")
        if ch in vistos:
            raise ValueError("Letra de enroque duplicada")
        vistos.add(ch)
    return campo

def validar_en_passant(campo: str) -> str:
    """
    Campo 4: '-' o casilla de destino de en passant (archivo a-h y fila 3 o 6).
    """
    if campo == '-':
        return campo
    if len(campo) != 2:
        raise ValueError("En passant debe ser '-' o una casilla (ej. 'e3')")
    archivo, fila = campo[0], campo[1]
    if archivo not in 'abcdefgh' or fila not in '36':
        raise ValueError("En passant debe ser archivo a-h y fila 3 o 6")
    return campo

def validar_semimov(campo: str) -> int:
    """
    Campo 5: semimovimientos (enteros no negativos).
    """
    if not campo.isdigit():
        raise ValueError("Semimovimiento debe ser un entero no negativo")
    return int(campo)

def validar_mov_total(campo: str) -> int:
    """
    Campo 6: número de movimiento (entero >= 1).
    """
    if not campo.isdigit():
        raise ValueError("El contador de movimientos debe ser un entero positivo")
    valor = int(campo)
    if valor < 1:
        raise ValueError("El contador de movimientos debe ser >= 1")
    return valor

def parsear_fen(cadena_fen: str) -> dict:
    """
    Parsea y valida una cadena FEN completa de 6 campos.
    Devuelve un diccionario con la matriz del tablero y metadatos.
    """
    partes = cadena_fen.strip().split()
    if len(partes) != 6:
        raise ValueError("El FEN debe tener exactamente 6 campos")
    colocacion, turno, enroque, ep, semimov, mov_total = partes
    tablero = parsear_colocacion(colocacion)
    turno = validar_turno(turno)
    enroque = validar_enroque(enroque)
    ep = validar_en_passant(ep)
    semimov = validar_semimov(semimov)
    mov_total = validar_mov_total(mov_total)
    return {
        'tablero': tablero,
        'turno': turno,
        'enroque': enroque,
        'en_passant': ep,
        'semimov': semimov,
        'mov_total': mov_total
    }

class AplicacionFEN:
    def __init__(self, ventana: tk.Tk) -> None:
        self.ventana = ventana
        ventana.title('Validador FEN - Tablero de Ajedrez')
        ventana.resizable(False, False)

        marco_superior = tk.Frame(ventana, padx=10, pady=10)
        marco_superior.pack(fill='x')

        tk.Label(marco_superior, text='Introduce una cadena FEN:').pack(anchor='w')
        self.entrada_fen = tk.Entry(marco_superior, width=70)
        self.entrada_fen.pack(side='left', padx=(0,10))
        self.entrada_fen.insert(0, "2r3k1/p3bqp1/Q2p3p/3Pp3/P3N3/8/5PPP/5RK1 b - - 1 27")

        marco_botones = tk.Frame(marco_superior)
        marco_botones.pack(side='left')
        tk.Button(marco_botones, text='Validar y Dibujar', command=self.validar).pack(fill='x')
        tk.Button(marco_botones, text='Limpiar', command=self.limpiar).pack(fill='x', pady=(5,0))

        marco_info = tk.Frame(ventana, padx=10)
        marco_info.pack(fill='x')
        self.etiqueta_info = tk.Label(marco_info, text='Información de la posición')
        self.etiqueta_info.pack(fill='x')

        marco_tablero = tk.Frame(ventana, padx=10, pady=10)
        marco_tablero.pack()
        self.lienzo = tk.Canvas(marco_tablero, width=480, height=480)
        self.lienzo.pack()

        self.etiqueta_estado = tk.Label(ventana, text='Estado: esperando entrada')
        self.etiqueta_estado.pack(fill='x', padx=10, pady=(0,10))

        # Fuente para piezas (DejaVu Sans suele incluir glifos de ajedrez en la mayoría de instalaciones)
        try:
            self.fuente_piezas = font.Font(family='DejaVu Sans', size=28)
        except Exception:
            self.fuente_piezas = font.Font(size=28)

        self.dibujar_tablero_vacio()

    def validar(self) -> None:
        fen = self.entrada_fen.get()
        try:
            datos = parsear_fen(fen)
        except Exception as e:
            # Mensaje simple y claro, con detalles opcionales a consola
            messagebox.showerror('Error FEN', f"FEN inválido: {e}")
            print("Detalle del error:\n", traceback.format_exc(), file=sys.stderr)
            self.etiqueta_estado.config(text=f'Error: {e}')
            return

        self.etiqueta_estado.config(text='FEN válido. Dibujando tablero...')
        self.etiqueta_info.config(text=(
            f"Turno: {datos['turno']}   Enroque: {datos['enroque']}   "
            f"EP: {datos['en_passant']}   Semimov: {datos['semimov']}   "
            f"Mov total: {datos['mov_total']}"
        ))
        self.dibujar_tablero(datos['tablero'])

    def dibujar_tablero_vacio(self) -> None:
        self._dibujar_cuadricula([['.']*8 for _ in range(8)])

    def dibujar_tablero(self, matriz: List[List[str]]) -> None:
        self._dibujar_cuadricula(matriz)

    def _dibujar_cuadricula(self, matriz: List[List[str]]) -> None:
        self.lienzo.delete('all')
        tam = 60
        for fila in range(8):
            for col in range(8):
                x0, y0 = col*tam, fila*tam
                color = '#F0D9B5' if (fila+col) % 2 == 0 else '#B58863'
                self.lienzo.create_rectangle(x0, y0, x0+tam, y0+tam, fill=color, outline='')
                pieza = matriz[fila][col]
                if pieza != '.':
                    self.lienzo.create_text(x0+tam/2, y0+tam/2, text=PIEZAS_UNICODE.get(pieza, ' '), font=self.fuente_piezas)
        # Etiquetas de coordenadas
        for i in range(8):
            self.lienzo.create_text((i+0.5)*tam, 8*tam-10, text=chr(ord('a')+i))
            self.lienzo.create_text(10, (i+0.5)*tam, text=str(8-i))

    def limpiar(self) -> None:
        self.entrada_fen.delete(0, 'end')
        self.etiqueta_info.config(text='Información de la posición')
        self.etiqueta_estado.config(text='Estado: limpio')
        self.dibujar_tablero_vacio()

def main() -> None:
    try:
        raiz = tk.Tk()
        app = AplicacionFEN(raiz)
        raiz.mainloop()
    except Exception as e:
        print('Error inesperado:', e, file=sys.stderr)
        traceback.print_exc()

if __name__ == '__main__':
    main()
