import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from experiment5.utils import *
from experiment5.Work_and_Energy.parameters import *
import json
from sympy import *

# Open and read the JSON file
file = open("q2.json")
question = json.load(file)
file.close()

# Assign values and units
values_dict = {}
units_dict = {}
values_dict["g"] = 9.8
units_dict["g"] = insert_latex("m/s^2")
values_dict["m"] = 10
units_dict["m"] = "kg"
values_dict["h_final"] = 3
units_dict["h_final"] = "m"
values_dict["h_initial"] = 1
units_dict["h_initial"] = "m"
ans_unit = " J"
ans_unit_by_1000 = " kJ"

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
thinker_json = thinker(question_list, explanation_sample)
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

# Get formula for gravitational_potential_energy
gpe = ""
def get_gpe_formula():
    return_step = ""
    if general_concepts_dict[g_c[0]] == "Yes"
        k_c.append("formula for gravitational potential energy is equal to mass * acceleration due to gravity * height")
        gpe = m*g*h
        values_dict["m"] = 10
        return_step = return_step + insert_latex("E_p = " + str(gpe)) + "\n"
    elif general_concepts_dict[g_c[0]] == "No":
        k_c.append("formula for gravitational potential energy is not equal to mass * acceleration due to gravity * height")
        formula_json = formula_reader("What is the formula for gravitational potential energy?", explanation_sample, "Your response should be a json object called 'formula'. While writing the formula, force should be denoted by 'F', distance/displacement should be denoted by 's', angle should be denoted by 'theta', mass should be denoted by 'm', acceleration should be denoted by 'a', velocity should be denoted by 'v', height should be denoted by 'h', and acceleration due to gravity should be denoted by 'g'. You can NOT use any other symbol in the formula. Follow python syntax while writing the formula. If the formula isn't mentioned, respond with 'Unknown' in the 'formula' attribute.")
            if formula_json['formula'] == "Unknown":
                return_step = return_step + "I am not sure how to proceed further.\n"
            else:
                gpe = sympify(formula_json['formula'])
                return_step = return_step + insert_latex("E_p = " + formula_json['formula']) + "\n"
    elif general_concepts_dict[g_c[0]] == "Unknown":
        return_step = return_step + "I am not sure how to proceed further.\n"
    return return_step

# Calculate change in gravitational potential energy
change_in_gpe = ""
def calculate_change_in_gpe():
    return_step = ""
    if general_concepts_dict[g_c[1]] == "Yes":
        k_c.append("a change in height of an object changes its gravitational potential energy")
        return_step = return_step + "I understand that a change in height of an object results in a change in its gravitational potential energy.\n"
        change_in_height = h_final - h_initial
        if h in gpe.free_symbols:
            change_in_gpe = gpe.subs(h, change_in_height)
            return_step = return_step + insert_latex("\delta E_p = " + str(change_in_gpe)) + "\n"
    else:
        change_in_gpe = gpe.subs(h, values_dict["h_final"])
        return_step = return_step + insert_latex("\delta E_p = " + str(change_in_gpe)) + "\n"
    return return_step

# Evaluate the question
def eval_question():
    solution = "The acceleration due to gravity " + insert_latex("g = " + print_value("g"))
    answer = "Could not compute"
    correct = False
    solution = solution + get_gpe_formula
    try:
        solution = solution + calculate_change_in_gpe()
    except:
        final_solution = output_maths_answer(q, solution) 
        print(final_solution['solution'], answer, correct)
        return final_solution['solution'], answer, correct
        
    try:
        if (h_initial in change_in_gpe.free_symbols) and (h_final in change_in_gpe.free_symbols):
            solution = solution + insert_latex("\delta E_p = " + str(change_in_gpe.subs([(m, print_value("m")), (g, print_value("g")), (h_final, print_value("h_final")), (h_initial, print_value("h_initial"))]))) + "\n"
            solution = solution + insert_latex("\delta E_p = " + str(change_in_gpe.subs([(m, values_dict["m"]), (g, values_dict["g"]), (h_final, values_dict["h_final"]), (h_initial, values_dict["h_initial"])])) + unit) + "\n"
            answer = round(N(gpe.subs([(m, values_dict["m"]), (g, values_dict["g"]), (h_final, values_dict["h_final"]), (h_initial, values_dict["h_initial"])])), 1)
        else:
            solution = solution + insert_latex("\delta E_p = " + str(change_in_gpe.subs([(m, print_value("m")), (g, print_value("g"))]))) + "\n"
            solution = solution + insert_latex("\delta E_p = " + str(change_in_gpe.subs([(m, values_dict["m"]), (g, values_dict["g"])])) + unit) + "\n"
            answer = round(N(gpe.subs([(m, values_dict["m"]), (g, values_dict["g"])])), 1)
        if answer == 196:
            correct = True
        answer = str(answer) + unit
        solution = solution + insert_latex("\delta E_p = " + answer)
    except:
        solution = solution + "I am not sure how to determine the change in gravitational potential energy."
        final_solution = output_maths_answer(q, solution) 
        print(final_solution['solution'], answer, correct)
        return final_solution['solution'], answer, correct
    
    final_solution = output_maths_answer(q, solution) 
    print(final_solution['solution'], answer, correct)
    return final_solution['solution'], answer, correct

eval_question()