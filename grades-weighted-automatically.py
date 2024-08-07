#!/usr/bin/python3
""" grades-weighted-automatically.py - Calcula las calificaciones y las pondera
    v0.1.2 - 2024-08-07 - nelbren@nelbren.com
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
    parser.add_argument(
        "-H",
        "--hide",
        action="store",
        default="0",
        dest="hide",
        help="Hide: 0 = Show names and rating, 1=Show only names, 2=Show only rating",
    )
    args = parser.parse_args()
    if args.url and args.api_key:
        return args.url, args.api_key
    url, api_key, hide = os.getenv('INSTRUCTURE_URL', ''), os.getenv('API_KEY', ''), os.getenv('HIDE', '')
    if url and api_key:
        return url, api_key, int(hide)
    else:
        parser.print_help()
        sys.exit(0)


def weighing(total, max):
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
        total2 += float(value_str)
        if hide == 1:
            value_str = "░░░░░"
        print(f"{plus}{value_str}", end="")
    redondeado = Decimal(total2).to_integral_value(rounding=ROUND_HALF_UP)
    lost = max - total2
    #totalp = total2 / max
    if hide == 1:
        print(f" = ████ - ▒▒▒▒▒▒ = ▓▓▓▓▓▓▓")
    else:
        print(f" = {redondeado:>4} - {max:6.2f} = {lost:7.2f}")


def get_assignments_by_course_and_assignment(course_id, assignment_id):
    """obtiene las asignaciones del estudiante del curso"""
    total = 0
    params = {"include[]": "total_scores", "per_page": "999"}
    response = requests.get(f'{base_url}/courses/{course_id}/assignments/{assignment_id}/submissions', headers=headers, params=params)
    if response.status_code == 200:
        total = 0
        for assignment in response.json():
            if assignment['entered_score'] != None:
                total += assignment['entered_score']
    return total


def get_assignments_by_course_and_user(user_id, course_id):
    """obtiene las asignaciones del estudiante del curso"""
    params = {"include[]": "total_scores", "per_page": "999"}
    response = requests.get(f'{base_url}/users/{user_id}/courses/{course_id}/assignments', headers=headers, params=params)
    if response.status_code == 200:
        total, total2 = 0, 0
        for assignment in response.json():
            assignment_id = assignment['id']
            #total2 += get_assignments_by_course_and_assignment(course_id, assignment_id)
            
            #sys.exit(1)
            total += float(assignment['points_possible'])
        return total
    else:
        print(f'Error: {response}')
        return 0


def line_student(header = 0):
    mark = '─'
    if header:
        print(f"  {'STUDENT NAME':>40} {'NOTE':>4} {'STATUS':>6} {'PART1':>5} + {'PART2':>5} + {'PART3':>5} + {'PART4':>5} = {'NOTE':>4} - {'TOTAL':>6} = {'MISSING':>7}")
    print(f"  {mark * 40} {mark * 4} {mark * 6} {mark * 5} {mark} {mark * 5} {mark} {mark * 5} {mark} {mark * 5} {mark} {mark * 4} {mark} {mark * 6} {mark} {mark * 7}")


def get_students(course_id):
    """obtiene los estudiantes del curso"""
    TAGS2 = ['𐄂 FAIL', '✔ PASS', '≡≡≡≡≡≡']
    params = {"enrollment_type[]": "student", "include[]": "enrollments", "per_page": "999"}
    response = requests.get(f'{base_url}/courses/{course_id}/users', headers=headers, params=params)
    if response.status_code == 200:
        line_student(1)
        grand_total, number_of_students  = 0, 0
        for student in response.json():
            total = get_assignments_by_course_and_user(student['id'], course_id)
            final_score = student['enrollments'][0]['grades']['final_score']
            if final_score:
                real = total * (final_score / 100)
            else:
                real = 0
            redondeado = Decimal(real).to_integral_value(rounding=ROUND_HALF_UP)
            paso = 0 if redondeado < 60 else 1
            grand_total += redondeado
            if hide == 1:
                redondeado = "███"
                paso = 2
            if hide == 2:
                name = len(student['name']) * '█'
            else:
                name = student['name'].upper()
            print(f"  {name:>40} {redondeado:>4} {TAGS2[paso]:>6} ", end="")
            weighing(real, total)
            number_of_students += 1
        line_student()
        average = grand_total / number_of_students
        average = f"{average:3.0f}"
        print(f"  {'AVERAGE':>40} {average:>4}")
        
    else:
        print(f'Error: {response}')


def my_user_id():
    """obtiene el id del usuario del token"""
    """No usado por: https://canvas.instructure.com/doc/api/favorites.html"""
    response = requests.get(f'{base_url}/users/self', headers=headers)
    if response.status_code == 200:
        return response.json()['id']
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
    mark = '═'
    courses = get_courses_favorites()
    if not courses:
        courses = get_courses_non_favorites()
    for course in courses:
        print(f"\n{course['name']}\n{len(course['name']) * mark}\n")
        get_students(course['id'])
        print(end='')


base_url, api_key, hide = get_params()
base_url += "/api/v1"
headers = { "Authorization": f"Bearer {api_key}" }
get_courses()
