import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from IB_Physics_DP.Work_and_Energy.utils import *
from IB_Physics_DP.Work_and_Energy.q3 import *
from IB_Physics_DP.Work_and_Energy.read_explanation import *
import json
from sympy import *

information_check_dict = read_explanation(required_information)

# Find the work done in changing the velocity
def find_work_done_ke(ke_formula):
    steps_response = ""
    work_done = None
    if information_check_dict[required_information[0]] == "Yes":
        steps_response = steps_response + "I understand that the work done in changing the velocity of the football is equal to the change in kinetic energy of the football.\n"
        steps_response = steps_response + "This is given by " + insert_latex("\\delta E_k") + "\n"
        if v in ke_formula.free_symbols:
            work_done = ke_formula.subs(v**2, v_final**2 - v_initial**2)
        else:
            work_done = ke_formula
        steps_response = steps_response + insert_latex("W = " + latex(work_done)) + "\n"
    else:
        steps_response = steps_response + "I am not sure how to calculate the work done based on the formulas given.\n"
    return steps_response, work_done

# Evaluate the question
def evaluate():
    working = ""
    answer = "Could not compute"
    correct = False
    steps_working, ke = find_ke_formula()
    working = working + steps_working
    try:
        steps_working, work_done = find_work_done_ke(ke)
        working = working + steps_working
    except Exception as E:
        print("Hello", E)
        working = working + "I understand that the work done in changing the velocity of the football is equal to the change in kinetic energy of the football. But I don't know what the kinetic energy of the football is.\n"
        print(working, answer, correct)
        return working, answer, correct
    try:
        working = working + insert_latex("W = " + latex(work_done.subs([(m, str(values_dict["m"])), (v_initial, str(values_dict["v_initial"])), (v_final, str(values_dict["v_final"]))]))) + "\n"
        working = working + insert_latex("W = " + latex(work_done.subs([(m, values_dict["m"]), (v_initial, values_dict["v_initial"]), (v_final, values_dict["v_final"])]))) + "\n"
        answer = N(work_done.subs([(m, values_dict["m"]), (v_initial, values_dict["v_initial"]), (v_final, values_dict["v_final"])]))
        working = working + insert_latex("W = " + latex(answer) + answer_unit) + "\n"
        if answer - answer_value < 0.00001:
            correct = True
        answer = '{:.2f}'.format(answer) + answer_unit
    except Exception as e:
        working = working + "I am not sure how to determine the work done.\n"
        print(e)
    if working == "":
        working = "I am not sure how to proceed further."
    print(working, answer, correct)
    return working, answer, correct

evaluate()