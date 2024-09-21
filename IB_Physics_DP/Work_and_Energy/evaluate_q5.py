import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from IB_Physics_DP.Work_and_Energy.utils import *
from IB_Physics_DP.Work_and_Energy.q5 import *
from IB_Physics_DP.Work_and_Energy.read_explanation import *
import json
from sympy import *

information_check_dict = read_explanation(required_information)

# Check if the total mechanical energy is conserved
def check_total_mechanical_energy_conserved():
    steps_response = ""
    energy_conserved = False
    energy_conserved_isolated = False
    if information_check_dict[required_information[0]] == "Yes":
        steps_response = steps_response + "I understand that the total mechanical energy of the block is the sum of it's kinetic energy and potential energy.\n"
        if information_check_dict[required_information[1]] == "Yes":
            steps_response = steps_response + "I understand that the total mechanical energy is conserved.\n"
            energy_conserved = True
        elif information_check_dict[required_information[1]] == "Wrong":
            if information_check_dict[required_information[3]] == "Yes":
                if information_check_dict[required_information[2]] == "Yes":
                    steps_response = steps_response + "I also understand that an isolated system is one that doesn't exchange any energy with it's surroundings and total mehcanical energy is conserved only for an isolated system\n"
                    energy_conserved_isolated = True
                else:
                    steps_response = steps_response + "I also understand that total mechanical energy is only conserved for an isolated system but I am not sure what is an isolated system.\n"
            else:
                if information_check_dict[required_information[2]] == "Yes":
                    steps_response = steps_response + "I also understand that an isolated system is one that doesn't exchange any energy with it's surroundings.\n"
    elif information_check_dict[required_information[0]] == "No":
        if information_check_dict[required_information[1]] == "Yes":
            steps_response = steps_response + "I understand that the total mechanical energy is conserved but I am not sure how to calculate the total mechanical energy.\n"
        elif information_check_dict[required_information[1]] == "Wrong":
            if information_check_dict[required_information[3]] == "Yes":
                if information_check_dict[required_information[2]] == "Yes":
                    steps_response = steps_response + "I understand that total mechanical energy is only conserved for an isolated system but I am not sure how to calculate the total mechanical energy.\n"
                else:
                    steps_response = steps_response + "I understand that total mechanical energy is only conserved for an isolated system but I am not sure what is an isolated system.\n"
            else:
                if information_check_dict[required_information[2]] == "Yes":
                    steps_response = steps_response + "I understand that an isolated system is one that doesn't exchange any energy with it's surroundings but I am not sure how to proceed further.\n"
    return steps_response, energy_conserved, energy_conserved_isolated


def evaluate():
    working = ""
    answer = "Could not compute"
    correct = False
    steps_working, ke = find_ke_formula()
    if ke:
        working = working + steps_working
    steps_working, gpe = find_gpe_formula()
    if gpe:
        working = working + steps_working
    steps_working, energy_conserved, energy_conserved_isolated = check_total_mechanical_energy_conserved()
    working = working + steps_working
    if energy_conserved:
        working = working + insert_latex("Total ME = E_k + E_p") + "\n"
        total_me = ke + gpe
        working = working + insert_latex("E_k_initial + E_p_initial = E_k_final + E_p_final") + "\n"
        try:
            working = working + insert_latex(latex(total_me.subs([(m, m), (v, "v_initial"), (g, "g"), (h, "h")])) + " = " + latex(total_me.subs([(m, "m"), (v, "v_final"), (g, "g"), (h, 0)]))) + "\n"
            total_me_equation = Eq(total_me.subs([(m, values_dict["m"]), (v, values_dict["v_initial"]), (g, values_dict["g"]), (h, values_dict["h"])]), total_me.subs([(m, values_dict["m"]), (v, "v_final"), (g, values_dict["g"]), (h, 0)]))
            working = working + insert_latex(latex(total_me_equation)) + "\n"
            answer_array = solve(total_me_equation, v_final)
            print(answer_value)
            for val in answer_array:
                if val > 0:
                    answer = val
                    break
            working = working + insert_latex("v_final = " + '{:.2f}'.format(answer) + answer_unit) + "\n"
            working = working + "Even if the air resistance is considered, the final speed will be the same.\n"
            answer = '{:.2f}'.format(answer) + answer_unit + ", the final speed will be the same"
        except Exception as e:
            if not ke:
                working = working + "I am not sure how to determine the kinetic energy of the box.\n"
            if not gpe:
                working = working + "I am not sure how to determine the gravitational potential energy of the box.\n"
            if ke and gpe:
                working = working + "I am not sure how to proceed further.\n"
            print(e)
            print(working, answer, correct)
            return working, answer, correct
    elif energy_conserved_isolated:
        working = working + insert_latex("Total ME = E_k + E_p") + "\n"
        working = working + insert_latex("E_k_initial + E_p_initial = E_k_final + E_p_final") + "\n"
        try:
            working = working + insert_latex(latex(total_me.subs([(m, m), (v, "v_initial"), (g, "g"), (h, "h")])) + " = " + latex(total_me.subs([(m, "m"), (v, "v_final"), (g, "g"), (h, 0)]))) + "\n"
            total_me_equation = Eq(total_me.subs([(m, values_dict["m"]), (v, values_dict["v_initial"]), (g, values_dict["g"]), (h, values_dict["h"])]), total_me.subs([(m, values_dict["m"]), (v, "v_final"), (g, values_dict["g"]), (h, 0)]))
            working = working + insert_latex(latex(total_me_equation)) + "\n"
            answer_array = solve(total_me_equation, v_final)
            for val in answer_array:
                if val > 0:
                    answer = val
                    break
            working = working + insert_latex("v_final = " + '{:.2f}'.format(answer) + answer_unit) + "\n"
            if abs(answer - answer_value) < 0.00001:
                correct = True
            working = working + "If the air resistance is considered, then there will be an external force acting on the block-earth system. Because of this, it won't be an isolated system and the total mechanical energy won't be conserved. Hence, the final speed will not be the same.\n"
            answer = '{:.2f}'.format(answer) + answer_unit + ", the final speed won't be the same"
        except Exception as e:
            if not ke:
                working = working + "I am not sure how to determine the kinetic energy of the box.\n"
            if not gpe:
                working = working + "I am not sure how to determine the gravitational potential energy of the box.\n"
            if ke and gpe:
                working = working + "I am not sure how to proceed further.\n"
            print(e)
            print(working, answer, correct)
            return working, answer, correct
    if working == "":
        working = "I am not sure how to proceed further."
    print(working, answer, correct)
    return working, answer, correct
evaluate()