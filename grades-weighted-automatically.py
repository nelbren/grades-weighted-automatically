#!/usr/bin/python3
""" grades-weighted-automatically.py - Calcula las calificaciones y las pondera
    v0.0.6 - 2022-09-29 - nelbren@nelbren.com
    Modulos requeridos: pip3 install pandas argparse
    Fuente: BB->Centro de califaciones->Trabajar sin conexión->Descargar
            ->OPCIONES: Tipo de delimitador: Coma -> Enviar -> DESCARGAR"""

import os
import glob
import math
import argparse
import pandas as pd


def dist(total, valor):
    """distribuye las notas"""
    if total > valor:
        return valor, total - valor
    return total, 0


def func_conv(nota):
    """función para convertir"""
    return round(float(nota.replace(",", ".")), 2)


def show_notes(_file):
    """muestra las notas"""
    TAGS = [ '❌', '✅' ]
    ponderacion = {
        "Ponderación Examen I": 30,
        "Ponderación Examen II": 30,
        "Ponderación Examen III": 30,
        "Ponderación Acumulativo": 10,
    }
    lst_pond = list(ponderacion.values())
    filename = os.path.basename(_file)
    line = (len(filename) + 1) * "="
    print(f"\n{filename}:\n{line}\n")
    data = pd.read_csv(filename, usecols=[1, 2, 7], converters={7: func_conv})
    data.columns.values[0], data.columns.values[1], data.columns.values[2] = "Alumno", "Cuenta", "Total"
    data = data.sort_values(by="Cuenta")

    for key, value in ponderacion.items():
        data[key] = value
    data["total2"] = 100
    for _, row in data.iterrows():
        total, total2, offset = row[2], 0, 3 # 3 es el inicio de ponderación
        for i, _ in enumerate(lst_pond):
            row[i + offset], total = dist(total, lst_pond[i])
            row[i + offset] = f"{row[i + offset]:.2f}".zfill(5)
            total2 += float(row[i + offset])
        row[2], row[7] = f"{row[2]:.2f}".zfill(6), f"{total2:.2f}".zfill(6)
        print(f"{row[0]:>40} ({row[1]}) {row[2]} |", end="")
        for i in range(3, 7):
            plus = "+" if i > 2 else ""
            print(f" {plus} {row[i]}", end="")
        valido = 1 if row[2] == row[7] or row[7] == "100.00" else 0
        total3 = math.ceil(total2)
        print(f" = {row[7]} {TAGS[valido]} {total3:3d}")


parser = argparse.ArgumentParser(
    description=(
        "Calcula las calificaciones y las pondera.\n\n"
        "Obtenga las califaciones así 👇\n\n"
        "BB->Centro de califaciones->Trabajar sin conexión->Descargar"
        "->OPCIONES: Tipo de delimitador: Coma -> Enviar -> DESCARGAR"
    ),
    formatter_class=argparse.RawTextHelpFormatter,
)
args = parser.parse_args()

for file in glob.glob("*.csv"):
    show_notes(file)