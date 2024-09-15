import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from experiment5.utils import *
from experiment5.Algebraic_Expressions.parameters import *
import json
from sympy import *

# Open and read the JSON file
file = open("q1.json")
question = json.load(file)
file.close()

# Generate sympy function
c = symbols("c")
expr = sympify(question["sympy"]["expressions"][0])


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
learner_explanation = explanation_sample
verifications_json = read_explanation(question_list, learner_explanation)
print(verifications_json)
for verification in verifications_json["verifications"]:
    if verification['verification_question'] in specific_concepts_dict:
        specific_concepts_dict[verification['verification_question']] = verification['verification_answer']
    elif verification['verification_question'] in general_concepts_dict:
        general_concepts_dict[verification['verification_question']] = verification['verification_answer']


# Evaluate the question
q = question["Question"]
s_c = question["specific_concepts"]
k_c = question["known_concepts"]
g_c = question["general_concepts"]
solution = ""
answer = "Could not compute"
correct = False
if general_concepts_dict[g_c[0]] == "Yes":
    k_c.append("variables are symbols in an expression")
    if general_concepts_dict[g_c[1]] == "Yes":
        k_c.append("variables can be substituted with any mathematical quantity")
        solution = solution + "I understand that I can substitute a variable with any mathematical value."
        answer = expr.subs(c, 4)
        correct = True
    elif general_concepts_dict[g_c[1]] == "No":
        k_c.append("variables can't be substituted with a mathematical quantity")
        solution = solution + "Since I can't subsitute a variable with a mathematical quantity, I am not sure how to proceed."
    elif general_concepts_dict[g_c[1]] == "Unknown":
        if specific_concepts_dict[s_c[1]] == "Yes":
            solution = solution + "I understand that I can substitute $c$ with $4$."
            answer = expr.subs(c, 4)
            correct = True
        elif specific_concepts_dict[s_c[1]] == "No":
            follow_up_solution = answer_explanation("What number can $c$ be substituted with?", learner_explanation, "Your response should be a json object 'c' containing the value of the substitution.")
            c_val = follow_up_solution['c']
            solution = solution + "I understand that I can substitute $c$ with $" + str(c_val) + "$"
            answer = expr.subs(c, c_val)
        elif specific_concepts_dict[s_c[1]] == "Unknown":
            solution = solution + "I understood that $c$ is a variable but I am not sure how to proceed."
elif general_concepts_dict[g_c[0]] == "No":
    k_c.append("variables are not symbols in an expression")
    solution = solution + "I understand that variables are not symbols. But using this, I don't know how to solve this question."
elif general_concepts_dict[g_c[0]] == "Unknown":
    if specific_concepts_dict[s_c[0]] == "Yes":
        k_c.append("$c$ is a variable")
        if general_concepts_dict[g_c[1]] == "Yes":
            k_c.append("$c$ can be substituted with any mathematical quantity")
            solution = solution + "I understand that I can substitute $c$ with any mathematical value."
            answer = expr.subs(c, 4)
            correct = True
        elif general_concepts_dict[g_c[1]] == "No":
            k_c.append("$c$ can't be substituted with a mathematical quantity")
            solution = solution + "Since I can't subsitute $c$ with a mathematical quantity, I am not sure how to proceed."
        elif general_concepts_dict[g_c[1]] == "Unknown":
            if specific_concepts_dict[s_c[1]] == "Yes":
                solution = solution + "I understand that I can substitute $c$ with $4$."
                answer = expr.subs(c, 4)
                correct = True
            elif specific_concepts_dict[s_c[1]] == "No":
                follow_up_solution = answer_explanation("What number can $c$ be substituted with?", learner_explanation, "Your response should be a json object 'c' containing the value of the substitution.")
                c_val = follow_up_solution['c']
                solution = solution + "I understand that I can substitute $c$ with $" + str(c_val) + "$"
                answer = expr.subs(c, c_val)
            elif specific_concepts_dict[s_c[1]] == "Unknown":
                solution = solution + "I understood that $c$ is a variable but I am not sure how to proceed."
    elif specific_concepts_dict[s_c[0]] == "No":
        k_c.append("$c$ is not a variable")
        solution = solution + "I understand that $c$ is not a variable ans using that, I don't know how to solve this question."
    elif specific_concepts_dict[s_c[0]] == "Unknown":
        if general_concepts_dict[g_c[1]] == "Yes":
            k_c.append("variables can be substituted with any mathematical quantity")
            solution = solution + "I understand that variables can be substituted with any mathematical quantity but I don't know what a variable is."
        elif general_concepts_dict[g_c[1]] == "No":
            k_c.append("variables can't be substituted with a mathematical quantity")
            solution = solution + "I understand that variables can't be substituted with any mathematical quantity but I don't know what a variable is."
        elif general_concepts_dict[g_c[1]] == "Unknown":
            if specific_concepts_dict[s_c[1]] == "Yes":
                solution = solution + "I understand that I can substitute $c$ with $4$."
                answer = expr.subs(c, 4)
                correct = True
            elif specific_concepts_dict[s_c[1]] == "No":
                follow_up_solution = answer_explanation("What number can $c$ be substituted with?", learner_explanation, "Your response should be a json object 'c' containing the value of the substitution.")
                c_val = follow_up_solution['c']
                solution = solution + "I understand that I can substitute $c$ with $" + str(c_val) + "$"
                answer = expr.subs(c, c_val)
            elif specific_concepts_dict[s_c[1]] == "Unknown":
                solution = solution + "I am not sure how to figure out this question. Can you explain a little more?"
final_solution = output_maths_answer(q, "Based on your explanation, " + solution) 
print(final_solution['solution'], answer, correct)
        
