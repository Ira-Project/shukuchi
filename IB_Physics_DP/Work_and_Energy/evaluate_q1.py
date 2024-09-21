import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from IB_Physics_DP.Work_and_Energy.utils import *
from IB_Physics_DP.Work_and_Energy.q1 import *
from IB_Physics_DP.Work_and_Energy.read_explanation import *
import json
from sympy import *

information_check_dict = read_explanation(required_information)

# Find the force
def find_force(information_check_dict):
    steps_response = ""
    force = None
    if information_check_dict[required_information[0]] == "Yes":
        steps_response = steps_response + "Since acceleration is zero, the net force on box is zero. So, the boy is exerting 300 N of force in the direction opposite friction.\n"
        force = values_dict["Friction"]
        steps_response = steps_response + insert_latex("F = " + combine_value_and_unit("F")) + "\n"
    elif information_check_dict[required_information[0]] == "Wrong":
        steps_response = steps_response + "Even if acceleration is zero, the net force on box may not be zero. So, I don't how to determine the force exerted by the boy to pull the box.\n"
    elif information_check_dict[required_information[0]] == "No":
        steps_response = steps_response + "I don't how to determine the force exerted by the boy.\n"
    return steps_response, force

# Find the angle between force and displacement
def find_theta(work_formula):
    steps_response = ""
    angle = values_dict["theta"]
    if information_check_dict[required_information[1]] == "Yes":
        steps_response = steps_response + "I understand that we only consider the components of the force that are in the direction of displacement caused by the force.\n"
        steps_response = steps_response + "This component is given by " + insert_latex("F cos(\\theta)") + "\n"
        correct_work_formula = F*s*cos(theta)
        angle = 0
        if simplify(correct_work_formula / work_formula) != 1:
            work_formula = work_formula.subs(F, F*cos(theta))
            steps_response = steps_response + insert_latex("W = " + latex(work_formula)) + "\n"
    return steps_response, angle, work_formula

# Evaluate the question
def evaluate():
    working = ""
    answer = "Could not compute"
    correct = False
    steps_working, force = find_force()
    working = working + steps_working
    steps_working, work_done = find_work_formula()
    working = working + steps_working
    try:
        steps_working, angle, work_done = find_theta(work_done)
        working = working + steps_working
    except Exception as E:
        print("hello", E)
        print(working, answer, correct)
        return working, answer, correct
    try:
        if theta in work_done.free_symbols:
            working = working + insert_latex("W = " + latex(work_done.subs([(F, str(force)), (s, str(values_dict["s"])), (theta, str(angle))]))) + "\n"
            working = working + insert_latex("W = " + latex(work_done.subs([(F, str(force)), (s, values_dict["s"]), (theta, angle)])) + answer_unit_into_1000) + "\n"
            answer = N(work_done.subs([(F, values_dict["F"]), (s, values_dict["s"]), (theta, angle)])) / 1000
        else:
            working = working + insert_latex("W = " + latex(work_done.subs([(F, str(force)), (s, str(values_dict["s"]))]))) + "\n"
            working = working + insert_latex("W = " + latex(work_done.subs([(F, force), (s, values_dict["s"])])) + answer_unit_into_1000) + "\n"
            answer = N(work_done.subs([(F, values_dict["F"]), (s, values_dict["s"])])) / 1000
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