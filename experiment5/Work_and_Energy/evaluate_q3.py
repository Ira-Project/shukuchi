import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from experiment5.utils import *
from experiment5.Work_and_Energy.parameters import *
import json
from sympy import *

# Open and read the JSON file
file = open("q3.json")
question = json.load(file)
file.close()

# Assign values and units
values_dict = {}
units_dict = {}
values_dict["m"] = 200/1000
units_dict["m"] = "kg"
values_dict["v_final"] = 0
units_dict["v_final"] = "m/s"
values_dict["v_initial"] = 20
units_dict["v_initial"] = "m/s"
ans_unit = " J"

# Function to easily print value and unit into a formula
def print_value(var):
    return str(values_dict[var]) + " " + units_dict[var]

# Initialize the dictionaries
general_concepts_dict = {}
specific_concepts_dict = {}

# Initialize the concepts in the dictionaries
for concept in question["general_concepts"]:
    general_concepts_dict[concept] = ""
for concept in question["specific_concepts"]:
    specific_concepts_dict[concept] = ""

# Convert required and not_required concepts to a list of questions
question_list = ""
for concept_question in general_concepts_dict.keys():
    question_list =  question_list + concept_question + "\n"
for concept_question in specific_concepts_dict.keys():
    question_list =  question_list + concept_question + "\n"

# Get solutions to the question_list
thinker_json = thinker(question_list, explanation_sample, instructions_post="You do not know what cos implies.")
# print(question_list)
# print(thinker_json)
for verification in thinker_json["answers"]:
    if verification['question'] in specific_concepts_dict:
        specific_concepts_dict[verification['question']] = verification['answer']
    elif verification['question'] in general_concepts_dict:
        general_concepts_dict[verification['question']] = verification['answer']

# Get the question parameters
q = question["Question"]
s_c = question["specific_concepts"]
k_c = question["known_concepts"]
g_c = question["general_concepts"]


# Get formula for kinetic energy
ke = ""
def get_kinetic_energy_formula():
    return_step = ""
    if general_concepts_dict[g_c[0]] == "Yes"
        k_c.append("formula for kinetic energy is equal to 1/2 * mass * (velocity**2)")
        ke = Rational(1/2)*m*(v**2)
        return_step = return_step + insert_latex("E_k = " + str(ke)) + "\n"
    elif general_concepts_dict[g_c[0]] == "No":
        k_c.append("formula for kinetic energy is not equal to 1/2 * mass * (velocity**2)")
        formula_json = formula_reader("What is the formula for kinetic energy?", explanation_sample, "Your response should be a json object called 'formula'. While writing the formula, force should be denoted by 'F', distance/displacement should be denoted by 's', angle should be denoted by 'theta', mass should be denoted by 'm', acceleration should be denoted by 'a', velocity should be denoted by 'v', height should be denoted by 'h', and acceleration due to gravity should be denoted by 'g'. You can NOT use any other symbol in the formula. Follow python syntax while writing the formula. If the formula isn't mentioned, respond with 'Unknown' in the 'formula' attribute.")
            if formula_json['formula'] == "Unknown":
                return_step = return_step + "I am not sure how to proceed further.\n"
            else:
                ke = sympify(formula_json['formula'])
                return_step = return_step + insert_latex("E_k = " + formula_json['formula']) + "\n"
    elif general_concepts_dict[g_c[0]] == "Unknown":
        return_step = return_step + "I am not sure how to proceed further.\n"
    return return_step

# Calculate change in gravitational potential energy
change_in_ke = ""
def calculate_change_in_ke():
    return_step = ""
    if general_concepts_dict[g_c[1]] == "Yes":
        k_c.append("a change in velocity of an object changes its kinetic energy")
        return_step = return_step + "I understand that a change in velocity of an object results in a change in its kinetic energy.\n"
        change_in_velocity = (v_final ** 2) - (v_initial ** 2)
        if v in ke.free_symbols:
            change_in_ke = ke.subs(v**2, change_in_velocity)
            return_step = return_step + insert_latex("\delta E_k = " + str(change_in_ke)) + "\n"
    else:
        change_in_ke = ke.subs(h, values_dict["v_initial"])
        return_step = return_step + insert_latex("\delta E_k = " + str(change_in_ke)) + "\n"
    return return_step

# Calculate work done
work_done = ""
def calculate_work_done():
    return_step = ""
    if general_concepts_dict[g_c[2]] == "Yes":
        k_c.append("work done by a force transfers equally to a change in kinetic energy")
        return_step = return_step + "I understand that the work done can be calculated by the change in kinetic energy that it produces.\n"
        work_done = change_in_ke
        return_step = return_step + insert_latex("W = " + str(work_done)) + "\n"
    else:
        formula_json = formula_reader("What is the formula for work done?", explanation_sample, "Your response should be a json object called 'formula'. While writing the formula, force should be denoted by 'F', distance/displacement should be denoted by 's', angle should be denoted by 'theta', mass should be denoted by 'm', acceleration should be denoted by 'a', velocity should be denoted by 'v', height should be denoted by 'h', and acceleration due to gravity should be denoted by 'g'. You can NOT use any other symbol in the formula. Follow python syntax while writing the formula. If the formula isn't mentioned, respond with 'Unknown' in the 'formula' attribute.")
        if formula_json['formula'] == "Unknown":
            return_step = return_step + "I am not sure how to calculate the work done.\n"
        else:
            work_done = sympify(formula_json['formula'])
            return_step = return_step + insert_latex("W = " + formula_json['formula']) + "\n"
    return return_step

# Evaluate the question
def eval_question():
    solution = ""
    answer = "Could not compute"
    correct = False
    solution = solution + get_kinetic_energy_formula
    try:
        solution = solution + check_velocity_change
    except:
        final_solution = output_maths_answer(q, solution) 
        print(final_solution['solution'], answer, correct)
        return final_solution['solution'], answer, correct

    try:
        solution = solution + calculate_work_done
    except:
        solution = solution + "I am not sure how to proceed further."

    try:
        if (v_initial in change_in_ke) and (v_final in change_in_ke):
            solution = solution + insert_latex("W = " + str(work_done.subs([(m, print_value("m")), (v_initial, print_value("v_initial")), (v_final, print_value("v_final"))]))) + "\n"
            solution = solution + insert_latex("W = " + str(work_done.subs([(m, values_dict["m"]), (v_initial, values_dict["v_initial"]), (v_final, values_dict["v_final"])])) + unit) + "\n"
            answer = round(N(work_done.subs([(m, values_dict["m"]), (v_initial, values_dict["v_initial"]), (v_final, values_dict["v_final"])])), 1)
        else:
            solution = solution + insert_latex("W = " + str(work_done.subs([(m, print_value("m"))]))) + "\n"
            solution = solution + insert_latex("W = " + str(work_done.subs([(m, values_dict["m"])])) + unit) + "\n"
            answer = round(N(work_done.subs([(m, values_dict["m"])])), 1)
        if answer == 40:
            correct = True
        answer = str(answer) + unit
        solution = solution + insert_latex("W = " + answer)
    except:
        solution = solution + "I am not sure how to determine the work done."
        final_solution = output_maths_answer(q, solution) 
        print(final_solution['solution'], answer, correct)
        return final_solution['solution'], answer, correct
    
    final_solution = output_maths_answer(q, solution) 
    print(final_solution['solution'], answer, correct)
    return final_solution['solution'], answer, correct

eval_question()