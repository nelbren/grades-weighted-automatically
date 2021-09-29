#!/usr/bin/python3
#
# grades-weighted-automatically.py
#
# v0.0.3 - 2021-09-29 - nelbren@nelbren.com
#
# pip3 install pandas
#

import glob, os
import pandas as pd

def dist(total, valor):
    if total > valor:
        return valor, total - valor
    else:
        return total, 0

def show_notes(f):
    ponderacion = { 'Ponderación Examen I':    30,
                    'Ponderación Examen II':   30,
                    'Ponderación Examen III':  30,
                    'Ponderación Acumulativo': 10 }
    lp = list(ponderacion.values())
    filename = os.path.basename(f)
    line = (len(filename)+1) * '='
    print(f'\n{filename}:\n{line}\n')
    f = lambda x: round(float(x.replace(',', '.')), 2)
    data = pd.read_csv(filename, usecols=[1,7], converters={7: f})
    data.columns.values[0], data.columns.values[1]  = "Alumno", "Total"

    for key, value in ponderacion.items():
        data[key] = value
    data['t2'] = 100
    for index, row in data.iterrows():
        total, t2 = row[1], 0
        for i in range(len(lp)):
            row[i + 2], total = dist(total, lp[i])
            row[i + 2] = f'{row[i + 2]:.2f}'.zfill(5)
            t2 += float(row[i + 2])
        row[1], row[6] = f'{row[1]:.2f}'.zfill(6), f'{t2:.2f}'.zfill(6)
        print(f'{row[0]:>35} {row[1]} | ', end='')
        for i in range(2, 6):
            print(f'+{row[i]}', end='')
        print(f'= {row[6]}')

for file in glob.glob("*.csv"):
    show_notes(file)