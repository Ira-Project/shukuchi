import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from IB_Physics_DP.utils import *
from IB_Physics_DP.Work_and_Energy.q4 import *
from IB_Physics_DP.Work_and_Energy.read_explanation import *
import json
from sympy import *

information_check_dict = read_explanation()

# Find the work done by changing the velocity
def find_work_done_ke(ke_formula):
    steps_response = ""
    work_done = None
    if information_check_dict[required_information[0]] == "Yes":
        steps_response = steps_response + "I understand that the work done is equal to the change in kinetic energy.\n"
        steps_response = steps_response + "This is given by " + insert_latex("\\delta E_k") + "\n"
        if v in ke_formula.free_symbols:
            work_done = ke_formula.subs(v**2, v_final**2 - v_initial**2)
        else:
            work_done = ke_formula
        steps_response = steps_response + insert_latex("W = " + latex(work_done)) + "\n"
    return steps_response, work_done

# Check if the total mechanical energy is conserved
def check_total_mechanical_energy_conserved():
    steps_response = ""
    energy_conserved = False
    energy_conserved_isolated = False
    if information_check_dict[required_information[1]] == "Yes":
        steps_response = steps_response + "I understand that the total mechanical energy of an object is the sum of it's kinetic energy and potential energy.\n"
        if information_check_dict[required_information[2]] == "Yes":
            steps_response = steps_response + "I understand that the total mechanical energy is conserved.\n"
            energy_conserved = True
        elif information_check_dict[required_information[2]] == "Wrong":
            if information_check_dict[required_information[5]] == "Yes":
                if information_check_dict[required_information[3]] == "Yes":
                    steps_response = steps_response + "I also understand that an isolated system is one that doesn't exchange any energy with it's surroundings and total mehcanical energy is conserved only for an isolated system\n"
                    energy_conserved_isolated = True
                else:
                    steps_response = steps_response + "I also understand that total mechanical energy is only conserved for an isolated system but I am not sure what is an isolated system.\n"
            else:
                if information_check_dict[required_information[3]] == "Yes":
                    steps_response = steps_response + "I also understand that an isolated system is one that doesn't exchange any energy with it's surroundings.\n"
    elif information_check_dict[required_information[1]] == "No":
        if information_check_dict[required_information[2]] == "Yes":
            steps_response = steps_response + "I understand that the total mechanical energy is conserved but I am not sure how to calculate the total mechanical energy.\n"
        elif information_check_dict[required_information[2]] == "Wrong":
            if information_check_dict[required_information[5]] == "Yes":
                if information_check_dict[required_information[3]] == "Yes":
                    steps_response = steps_response + "I understand that total mechanical energy is only conserved for an isolated system but I am not sure how to calculate the total mechanical energy.\n"
                else:
                    steps_response = steps_response + "I understand that total mechanical energy is only conserved for an isolated system but I am not sure what is an isolated system.\n"
            else:
                if information_check_dict[required_information[3]] == "Yes":
                    steps_response = steps_response + "I understand that an isolated system is one that doesn't exchange any energy with it's surroundings but I am not sure how to proceed further.\n"
    return steps_response, energy_conserved, energy_conserved_isolated


def evaluate():
    working = ""
    answer = "Could not compute"
    correct = False
    steps_working, work_done_1 = find_work_formula()
    if work_done_1:
        working = working + steps_working
    steps_working, ke = find_ke_formula()
    if ke:
        working = working + steps_working
    try:
        steps_working, work_done_2 = find_work_done_ke(ke)
        working = working + steps_working
    except Exception as E:
        print("Hello", E)
        working = working + "I also understand that the work done in changing the velocity is equal to the change in kinetic energy. But I don't know what the kinetic energy of the box is.\n"
        print(working, answer, correct)
        return working, answer, correct
    if work_done_1 and not work_done_2:
        try:
            working = working + insert_latex("W = " + latex(work_done_1.subs([(s, values_dict["s_old"])]))) + "\n"
            working = working + insert_latex("100 J = " + latex(work_done_1.subs([(s, values_dict["s_old"])]))) + "\n"
            work_done_old = work_done_1.subs([(s, values_dict["s_old"])])
            working = working + "Substituting " + insert_latex(latex(values_dict["s_old"])) + " for " + insert_latex(latex(values_dict["s_new"])) + "\n"
            working = working + insert_latex("W = " + latex(work_done_1.subs([(s, values_dict["s_new"])]))) + "\n"
            work_done_new = work_done_1.subs([(s, values_dict["s_new"])])
            answer = work_done_new / work_done_old * values_dict["W"]
            working = working + insert_latex("W = " + '{:.2f}'.format(answer) + answer_unit)
            if abs(answer - answer_value) < 0.00001:
                correct = True
            answer = '{:.2f}'.format(answer) + answer_unit
        except Exception as e:
            working = working + "I am not sure how to determine the work done."
            print("HELLLLLO",e)
    elif work_done_2 and not work_done_1:
        try:
            answer = simplify(work_done_2.subs([(m, "m"), (v_final, values_dict["v2"]), (v_initial, values_dict["v1"])]))
            working = working + insert_latex("W = " + '{:.2f}'.format(answer) + answer_unit)
            if abs(answer - answer_value) < 0.00001:
                correct = True
            answer = '{:.2f}'.format(answer) + answer_unit
        except Exception as e:
            working = working + "I am not sure how to determine the work done."
            print(e)
    elif work_done_1 and work_done_2:
        steps_working, energy_conserved, energy_conserved_isolated = check_total_mechanical_energy_conserved()
        if energy_conserved:
            working = working + steps_working
            working = working + insert_latex("Total ME = E_k + E_p") + "\n"
            working = working + "Since Total ME of the box doesn't change and there is no change in E_p along the horizontal surface, E_k of the box is also constant.\n"
            working = working + insert_latex("W = \\delta E_k = 0") + "\n"
            answer = 0
            if abs(answer - answer_value) < 0.00001:
                correct = True
            answer = '{:.2f}'.format(answer) + answer_unit
        elif energy_conserved_isolated:
            if information_check_dict[required_information[4]] == "Yes":
                try:
                    working = working + "I understand that work done on an object by external forces transfers energy to or from the object. So the work done by the force dragging the box is transferring energy to the box and the work done by friction is transferring energy away from the box. Hence, the box is not an isolated system and the conservation of mechanical energy won't apply.\n"
                    wokring = working + "To calculate this work done: \n"
                    working = working + insert_latex("W = " + latex(work_done_1.subs([(s, values_dict["s_old"])]))) + "\n"
                    working = working + insert_latex("100 J = " + latex(work_done_1.subs([(s, values_dict["s_old"])]))) + "\n"
                    work_done_old = work_done_1.subs([(s, values_dict["s_old"])])
                    working = working + "Substituting " + insert_latex(latex(values_dict["s_old"])) + " for " + insert_latex(latex(values_dict["s_new"])) + "\n"
                    working = working + insert_latex("W = " + latex(work_done_1.subs([(s, values_dict["s_new"])]))) + "\n"
                    work_done_new = work_done_1.subs([(s, values_dict["s_new"])])
                    answer = work_done_new / work_done_old * values_dict["W"]
                    working = working + insert_latex("W = " + '{:.2f}'.format(answer) + answer_unit)
                    working = working + "The kinetic energy of the box doesn't change as the net work done by all the external forces on the box is zero. This is because the work done by the dragging force is equal and opposite to the work done by friction.\n"
                    if abs(answer - answer_value) < 0.00001:
                        correct = True
                    answer = '{:.2f}'.format(answer) + answer_unit
                except Exception as e:
                    working = working + "I understand that work done on an object transfers energy to or from the object. So the work done by the force dragging the box is transferring energy to the box and the work done by friction is transferring energy away from the box. Hence, the box is not an isolated system and the conservation of mechanical energy won't apply.\n"
                    working = working + "But, I am not able to calculate the work done."
                    print(e)
            else:
                working = working + steps_working
                working = working + "I understand that the box may not be an isolated system. But it's being dragged at a constant speed, so it's kinetic energy remains the same. Hence, the work done is zero.\n"
                working = working + insert_latex("W = \\delta E_k = 0") + "\n"
                answer = 0
                if abs(answer - answer_value) < 0.00001:
                    correct = True
                answer = '{:.2f}'.format(answer) + answer_unit
        else:
            try:
                answer = simplify(work_done_2.subs([(m, "m"), (v_final, values_dict["v2"]), (v_initial, values_dict["v1"])]))
                working = working + insert_latex("W = " + '{:.2f}'.format(answer) + answer_unit)
                if abs(answer - answer_value) < 0.00001:
                    correct = True
                answer = '{:.2f}'.format(answer) + answer_unit
            except Exception as e:
                working = working + "I am not sure how to determine the work done."
                print(e)
    print(working, answer, correct)
    return working, answer, correct


evaluate()