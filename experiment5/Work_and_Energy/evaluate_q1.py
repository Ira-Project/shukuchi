import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from experiment5.utils import *
from experiment5.Work_and_Energy.parameters import *
import json
from sympy import *

# Open and read the JSON file
file = open("q1.json")
question = json.load(file)
file.close()

# Assign values and units
values_dict = {}
units_dict = {}
values_dict["Friction"] = 300
units_dict["Friction"] = "N"
values_dict["s"] = 100
units_dict["s"] = "m"
values_dict["theta"] = 30
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

# Calculate the force
def calculate_force():
    return_step = ""
    if general_concepts_dict[g_c[0]] == "Yes":
        k_c.append("if acceleration is zero, then net force is zero.")
        return_step = return_step + "Since acceleration is zero, the net force on box is zero. So, the boy is exerting 300 N of force in the direction opposite friction.\n"
        values_dict["F"] = 300
        units_dict["F"] = "N"
        return_step = return_step + insert_latex("F = " + str(values_dict["F"]) + units_dict)["F"] + "\n"
    elif general_concepts_dict[g_c[0]] == "No":
        k_c.append("if acceleration is zero, then net force may not be zero.")
        return_step = return_step + "Even if acceleration is zero, the net force on box may not be zero. So, I don't how to determine the force exerted by the boy to pull the box.\n"
    elif general_concepts_dict[g_c[0]] == "Unknown":
        return_step = return_step + "But, I don't how to determine the force exerted by the boy to pull the box.\n"
    return return_step

# Get formula for work done
work_done = ""
def get_work_done_formula():
    return_step = ""
    if general_concepts_dict[g_c[1]] == "Yes"
        k_c.append("formula for work is equal to force times displacement")
        work_done = F*s
        return_step = return_step + insert_latex("W = " + str(work_done)) + "\n"
    elif general_concepts_dict[g_c[1]] == "No":
        formula_json = formula_reader("What is the formula for work done?", explanation_sample, "Your response should be a json object called 'formula'. While writing the formula, force should be denoted by 'F', distance/displacement should be denoted by 's', angle should be denoted by 'theta', mass should be denoted by 'm', acceleration should be denoted by 'a', velocity should be denoted by 'v', height should be denoted by 'h', and acceleration due to gravity should be denoted by 'g'. You can NOT use any other symbol in the formula. Follow python syntax while writing the formula. If the formula isn't mentioned, respond with 'Unknown' in the 'formula' attribute.")
            if formula_json['formula'] == "Unknown":
                return_step = return_step + "I am not sure how to proceed further.\n"
            else:
                work_done = sympify(formula_json['formula'])
                return_step = return_step + insert_latex("W = " + formula_json['formula']) + "\n"
    elif general_concepts_dict[g_c[1]] == "Unknown":
        return_step = return_step + "I am not sure how to proceed further.\n"
    return return_step

# Check the meaning of theta
def check_theta():
    return_step = ""
    if general_concepts_dict[g_c[2]] == "Yes":
        k_c.append("to calculate work done, only the force applied in the direction of displacement is considered.")
        return_step = return_step + "I understand when calculating the work done by a force, we only consider the components of the force that are in the direction of displacement caused by the force."
        return_step = return_step + "This component is given by " + insert_latex("F*cos(\\theta)")
        work_done_in_direction = F*s*cos(theta)
        if simplify(work_done_in_direction / work_done) == 1:
            values_dict["theta"] = 0
        else:
            work_done = work_done.subs(F, F*cos(theta))
            return_step = return_step + insert_latex("W = " + str(work_done)) + "\n"
            values_dict["theta"] = 0
    return return_step

# Evaluate the question
def eval_question():
    solution = "The box has zero acceleration as the speed is constant."
    answer = "Could not compute"
    correct = False
    solution = solution + calculate_force()
    solution = solution + get_work_done_formula()
    try:
        solution = solution + check_theta()
    except:
        final_solution = output_maths_answer(q, solution) 
        print(final_solution['solution'], answer, correct)
        return final_solution['solution'], answer, correct

    try:
        if theta in work_done.free_symbols:
            ## MAYBE CONVERT STR() to LATEX() SYMPY
            solution = solution + insert_latex("W = " + str(work_done.subs([(F, print_value("F")), (s, print_value("s")), (theta, print_value("theta"))]))) + "\n"
            solution = solution + insert_latex("W = " + str(work_done.subs([(F, values_dict["F"]), (s, values_dict["s"]), (theta, values_dict["theta"])])) + ans_unit) + "\n"
            answer = round(N(work_done.subs([(F, values_dict["F"]), (s, values_dict["F"]), (theta, 0)])) / 1000, 2)
        else:
            solution = solution + insert_latex("W = " + str(work_done.subs([(F, print_value("F")), (s, print_value("s"))]))) + "\n"
            solution = solution + insert_latex("W = " + str(work_done.subs([(F, values_dict["F"]), (s, values_dict["s"])])) + ans_unit) + "\n"
            answer = round(N(work_done.subs([(F, values_dict["F"]), (s, values_dict["F"]), (theta, 0)])) / 1000, 2)
        if answer == 30:
            correct = True
        answer = str(answer) + ans_unit_by_1000
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