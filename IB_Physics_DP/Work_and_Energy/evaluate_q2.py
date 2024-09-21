import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from IB_Physics_DP.Work_and_Energy.utils import *
from IB_Physics_DP.Work_and_Energy.q2 import *
from IB_Physics_DP.Work_and_Energy.read_explanation import *
import json
from sympy import *

information_check_dict = read_explanation(required_information)

# Find the work done against gravity
def find_work_done_gpe(gpe_formula):
    steps_response = ""
    work_done = None
    if information_check_dict[required_information[0]] == "Yes":
        steps_response = steps_response + "I understand that the work done in lifting the dumbbell against gravity is the same as the change in gravitational potential energy of the dumbbell.\n"
        steps_response = steps_response + "This is given by " + insert_latex("\\delta E_p") + "\n"
        if h in gpe_formula.free_symbols:
            work_done = gpe_formula.subs(h, h_final - h_initial)
        else:
            work_done = gpe_formula
        steps_response = steps_response + insert_latex("W = " + latex(work_done)) + "\n"
    else:
        steps_response = steps_response + "I am not sure how to calculate the work done based on the formulas given.\n"
    return steps_response, work_done

# Evaluate the question
def evaluate():
    working = ""
    answer = "Could not compute"
    correct = False
    steps_working, gpe = find_gpe_formula()
    working = working + steps_working
    try:
        steps_working, work_done = find_work_done_gpe(gpe)
        working = working + steps_working
    except Exception as E:
        print("hello", E)
        working = working + "I understand that the work done in lifting the dumbbell against gravity is the same as the change in gravitational potential energy of the dumbbell. But I don't know what the gravitational potential energy of the dumbbell is.\n"
        print(working, answer, correct)
        return working, answer, correct
    try:
        working = working + insert_latex("W = " + latex(work_done.subs([(m, str(values_dict["m"])), (g, str(values_dict["g"])), (h_initial, str(values_dict["h1"])), (h_final, str(values_dict["h2"]))]))) + "\n"
        working = working + insert_latex("W = " + latex(work_done.subs([(m, values_dict["m"]), (g, values_dict["g"]), (h_initial, values_dict["h1"]), (h_final, values_dict["h2"])])) + answer_unit) + "\n"
        answer = N(work_done.subs([(m, values_dict["m"]), (g, values_dict["g"]), (h_initial, values_dict["h1"]), (h_final, values_dict["h2"])]))
        working = working + insert_latex("W = " + '{:.2f}'.format(answer) + answer_unit)
        if abs(answer - answer_value) < 0.00001:
            correct = True
        answer = '{:.2f}'.format(answer) + answer_unit
    except Exception as e:
        working = working + "I am not sure how to determine the work done."
        print(e)
    if working == "":
        working = "I am not sure how to proceed further."
    print(working, answer, correct)
    return working, answer, correct

evaluate()
