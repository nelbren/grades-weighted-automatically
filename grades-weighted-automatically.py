#!/usr/bin/python3
""" grades-weighted-automatically.py - Calcula las calificaciones y las pondera
    v0.0.4 - 2021-12-21 - nelbren@nelbren.com
    Modulos requeridos: pip3 install pandas argparse
    Fuente: BB->Centro de califaciones->Trabajar sin conexión->Descargar
            ->OPCIONES: Tipo de delimitador: Coma -> Enviar -> DESCARGAR"""

import os
import glob
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
    data = pd.read_csv(filename, usecols=[1, 7], converters={7: func_conv})
    data.columns.values[0], data.columns.values[1] = "Alumno", "Total"

    for key, value in ponderacion.items():
        data[key] = value
    data["total2"] = 100
    for _, row in data.iterrows():
        total, total2 = row[1], 0
        for i, _ in enumerate(lst_pond):
            row[i + 2], total = dist(total, lst_pond[i])
            row[i + 2] = f"{row[i + 2]:.2f}".zfill(5)
            total2 += float(row[i + 2])
        row[1], row[6] = f"{row[1]:.2f}".zfill(6), f"{total2:.2f}".zfill(6)
        print(f"{row[0]:>35} {row[1]} | ", end="")
        for i in range(2, 6):
            print(f"+{row[i]}", end="")
        print(f"= {row[6]}")


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