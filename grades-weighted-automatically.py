#!/usr/bin/python3
""" grades-weighted-automatically.py - Calcula las calificaciones y las pondera
    v0.1.1 - 2024-08-06 - nelbren@nelbren.com
    Fuente: Canvas->API"""

import os
import sys
import argparse
try:
    import requests
except ModuleNotFoundError:
    ext = "bash"
    if os.name == 'nt':
       ext = "bat"
    print(f"Please install the modules by running the script: install_requirements.{ext}")
    sys.exit(3)
from decimal import Decimal, ROUND_HALF_UP

def dist(total, valor):
    """distribuye las notas"""
    if total > valor:
        return valor, total - valor
    return total, 0

def get_params():
    email = "nelbren@nelbren.com"
    parser = argparse.ArgumentParser(
        description=(
            "Grades weighted automatically using API of Canvas Instructure.\n"
            f"Contact email 👉 {email}\n\n"
            "1) Get your API_KEY like this 👇\n\n"
            "  1.1) Canvas->Account->Settings->New Access Token->Fill fields of Purpose and Expires\n"
            "       Generate token->Copy the token!\n"
            "  1.2) Or view this video 👉 https://www.youtube.com/watch?v=cZ5cn8stjM0\n\n"
            "2) Set your Instructure URL and API_KEY like this 👇\n\n"
            "  2.1) Using environment variables:\n"
            "       INSTRUCTURE_URL='https://some.instructure.com'\n       API_KEY='your-api-key'\n"
            "  2.2) Using parameters: 👇"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-u",
        "--instructure_url",
        action="store",
        default="",
        dest="url",
        help="Set your Instructure URL",
    )
    parser.add_argument(
        "-k",
        "--api_key",
        action="store",
        default="",
        dest="api_key",
        help="Set your API KEY",
    )
    args = parser.parse_args()
    if args.url and args.api_key:
        return args.url, args.api_key
    url, api_key = os.getenv('INSTRUCTURE_URL', ''), os.getenv('API_KEY', '')
    if url and api_key:
        return url, api_key
    else:
        parser.print_help()
        sys.exit(0)

def weighing(total):
    ponderacion = { "Ponderación Examen I":   30,   "Ponderación Examen II": 30,
                    "Ponderación Examen III": 30, "Ponderación Acumulativo": 10 }
    lst_pond = list(ponderacion.values())
    notas = []
    for indice in range(len(ponderacion)):
        notas.append(0)
    for i, value in enumerate(lst_pond):
        notas[i], total = dist(total, lst_pond[i])
    total2 = 0
    for i, value in enumerate(notas):
        plus = " + " if i > 0 else ""
        value_str = f"{value:5.2f}"
        print(f"{plus}{value_str}", end="")
        total2 += float(value_str)
    redondeado = Decimal(total2).to_integral_value(rounding=ROUND_HALF_UP)        
    print(f" = {redondeado:>3}")

def get_assignments_by_course_and_user(user_id, course_id):
    """obtiene las asignaciones del estudiante del curso"""
    params = {"include[]": "total_scores", "per_page": "999"}
    response = requests.get(f'{base_url}/users/{user_id}/courses/{course_id}/assignments', headers=headers, params=params)
    if response.status_code == 200:
        total = 0
        for assignment in response.json():
            total += float(assignment['points_possible'])
        return total
    else:
        print(f'Error: {response}')
        return 0

def get_students(course_id):
    """obtiene los estudiantes del curso"""
    TAGS2 = [ '🔴', '⚪']
    params = {"enrollment_type[]": "student", "include[]": "enrollments", "per_page": "999"}
    response = requests.get(f'{base_url}/courses/{course_id}/users', headers=headers, params=params)
    if response.status_code == 200:
        for student in response.json():
            total = get_assignments_by_course_and_user(student['id'], course_id)
            final_score = student['enrollments'][0]['grades']['final_score']
            if final_score:
                real = total * (final_score / 100)
            else:
                real = 0
            redondeado = Decimal(real).to_integral_value(rounding=ROUND_HALF_UP)
            paso = 0 if redondeado < 60 else 1
            print(f"  {student['name'].upper():>40} {redondeado:>3} {TAGS2[paso]} ", end="")
            weighing(real)
    else:
        print(f'Error: {response}')

def my_user_id():
    """obtiene el id del usuario del token"""
    """No usado por: https://canvas.instructure.com/doc/api/favorites.html"""
    response = requests.get(f'{base_url}/users/self', headers=headers)
    if response.status_code == 200:
        return response.json()['id']
        exit(0)
    print(f'Error: {response}')
    exit(1)

def get_courses_favorites():
    """obtiene los cursos favoritos"""
    response = requests.get(f'{base_url}/users/self/favorites/courses', headers=headers)
    if response.status_code == 200:
        courses = []
        for course in response.json():
            courses.append(course)
        return courses
    else:
        print(f'Error: {response}')
        exit(1)
    
def get_courses_non_favorites():
    response = requests.get(f'{base_url}/courses', headers=headers)
    if response.status_code == 200:
        courses = []
        for course in response.json():
            if course['enrollments'][0]['type'] == 'teacher' and course['workflow_state'] == 'available':
                courses.append(course)
        return courses
    else:
        print(f'Error: {response}')
        exit(2)

def get_courses():
    """obtiene los cursos"""
    courses = get_courses_favorites()
    if not courses:
        courses = get_courses_non_favorites()
    for course in courses:
        print(f"\n{course['name']}\n{len(course['name'])*'-'}")
        get_students(course['id'])
        print(end='')

base_url, api_key = get_params()
base_url += "/api/v1"
headers = { "Authorization": f"Bearer {api_key}" }
get_courses()
