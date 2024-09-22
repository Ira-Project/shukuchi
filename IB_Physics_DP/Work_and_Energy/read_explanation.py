import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from IB_Physics_DP.Work_and_Energy.utils import *
from IB_Physics_DP.Work_and_Energy.parameters import *
import json
from sympy import *

# Convert concepts to an information checklist
def read_explanation(required_information):
    information_check_dict = {}
    information_list = ""
    for information in required_information:
        information_list = information_list + "Question: " + information_questions[information] + "\nInformation: " + information + "\n"
        information_check_dict[information] = "Unknown"

    # Perform an automated information check
    checklist_json = check_information(information_list, explanation_sample, instructions_post=information_checklist_prompt_post)
    for information in checklist_json['information_checklist']:
        if information['information'] in information_check_dict:
            information_check_dict[information['information']] = information['check']
    print(information_check_dict)
    return information_check_dict

# Find the formula for work done
def find_work_formula():
    steps_response = ""
    work_done = None
    formula_json = formula_reader("What is the formula for work done?", formula_sample)
    if formula_json['formula'] == "Unknown":
        steps_response = steps_response + "I am not sure how to proceed further since you have not given me the formula for work done.\n"
    else:
        try:
            formula_read = formula_json['formula'].split("=")[1]
        except IndexError:
            formula_read = formula_json['formula']
        work_done = sympify(formula_read)
        steps_response = steps_response + insert_latex("W = " + latex(work_done)) + "\n"
    return steps_response, work_done

# Find the formula for gravitational potential energy (gpe)
def find_gpe_formula():
    steps_response = ""
    gpe = None
    formula_json = formula_reader("What is the formula for gravitational potential energy?", formula_sample)
    if formula_json['formula'] == "Unknown":
        steps_response = steps_response + "I am not sure how to proceed further.\n"
    else:
        try:
            formula_read = formula_json['formula'].split("=")[1]
        except IndexError:
            formula_read = formula_json['formula']
        gpe = sympify(formula_read)
        steps_response = steps_response + insert_latex("Gravitational Potential Energy = " + latex(gpe)) + "\n"
    return steps_response, gpe

# Find the formula for kinetic energy (ke)
def find_ke_formula():
    steps_response = ""
    ke = None
    formula_json = formula_reader("What is the formula for kinetic energy?", formula_sample)
    if formula_json['formula'] == "Unknown":
        steps_response = steps_response + "I am not sure how to proceed further.\n"
    else:
        try:
            formula_read = formula_json['formula'].split("=")[1]
        except IndexError:
            formula_read = formula_json['formula']
        ke = sympify(formula_read)
        steps_response = steps_response + insert_latex("Kinetic Energy = " + latex(ke)) + "\n"
    return steps_response, ke