#!/usr/bin/python3
""" grades-weighted-automatically.py - Calcula las calificaciones y las pondera
    v0.0.7 - 2023-03-29 - nelbren@nelbren.com
    Modulos requeridos: pip3 install pandas argparse
    Fuente: Canvas->Libro de calificaciones->Acciones->Exportar todo el libro de calificaciones"""

import os
import glob
import argparse
import pandas as pd
import numpy as np

def dist(total, valor):
    """distribuye las notas"""
    if total > valor:
        return valor, total - valor
    return total, 0

def show_notes(_file):
    """muestra las notas"""
    TAGS, TAGS2 = [ '❌', '✅' ], [ '🔴', '⚪']
    ponderacion = { "Ponderación Examen I": 30,   "Ponderación Examen II": 30,
                    "Ponderación Examen III": 30, "Ponderación Acumulativo": 10 }
    lst_pond = list(ponderacion.values())
    filename = os.path.basename(_file)
    line = (len(filename) + 1) * "="
    print(f"\n{filename}:\n{line}\n")
    data = pd.read_csv(filename)
    col_total = len(data.columns) - 5 # ultima columna - 5
    
    for key, value in ponderacion.items():
        data[key] = value
    data["total2"] = 100
    for _, row in data.iterrows():
        if np.isnan(row[2]):
            continue
        total, total2, offset = float(row[col_total]), 0, 3 # 3 es el inicio de ponderación
        for i, _ in enumerate(lst_pond):
            row[i + offset], total = dist(total, lst_pond[i])
            row[i + offset] = f"{row[i + offset]:.2f}".zfill(5)
            total2 += float(row[i + offset])
        row[2], row[7] = f"{row[2]:.2f}".zfill(6), f"{total2:.2f}".zfill(6)
        print(f"{row[0]:>40} {row[col_total]} |", end="")
        for i in range(3, 7):
            plus = "+" if i > 2 else ""
            print(f" {plus} {row[i]}", end="")
        valido = 1 if float(row[col_total]) == float(row[7]) or row[7] == "100.00" else 0
        total3 = int(round(total2, 0))
        paso = 0 if total3 < 60 else 1
        print(f" = {row[7]} {TAGS[valido]} {total3:3d} {TAGS2[paso]}")

parser = argparse.ArgumentParser(
    description=(
        "Calcula las calificaciones y las pondera.\n\n"
        "Obtenga las califaciones así 👇\n\n"
        "Canvas->Libro de calificaciones->Acciones->Exportar todo el libro de calificaciones"
    ),
    formatter_class=argparse.RawTextHelpFormatter,
)
args = parser.parse_args()

for file in glob.glob("*.csv"):
    show_notes(file)