from sympy import *

F, s, theta, W = symbols("F s theta W")
m, a, v = symbols("m a v")
g, h = symbols("g h")
v_final, v_initial = symbols("v_final v_initial")
h_final, h_initial = symbols("h_final h_initial")
E_p, E_k, E_s = symbols("E_p E_k E_s") 
F_cos_theta = symbols("F_cos_theta")
s_cos_theta = symbols("s_cos_theta")

explanation_sample = "the total mechanical energy is the sum of the kinetic and potential energy. the total mechanical energy is conserved, i.e., it can neither be created nor be destroyed"
formula_sample = "[W = F * s * cos(theta), E_k = 1/2 * m * v**2, E_p = m * g * h]"

known_concepts = [
    "if speed is constant, then acceleration is zero",
    "g is acceleration due to gravity"
    ]

formulas = {}
formulas[W]=F*s*cos(theta)
formulas[F]=m*a
formulas[F_cos_theta]=F*cos(theta)
formulas[s_cos_theta]=s*cos(theta)
formulas[E_p]=m*g*h
formulas[E_k]=(1/2)*m*v**2

unknown_concepts = {}
unknown_concepts["How to find the net force?"] = [
    "force is zero if the acceleration is zero"
    ]
unknown_concepts["How to calculate the work done by a force?"] = [
    "to calculate the work done by a force, we use only the force component along the object's displacement"
    ]
unknown_concepts["What is the work done against gravity?"] = [
    "work done against gravity is equal to change in gravitational potential energy"
    ]
unknown_concepts["What is the work done to change the velocity?"] = [
    "work done to change the velocity is equal to the change in kinetic energy"
    ]
unknown_concepts["What is the conservation of total mechanical enegry?"] = [
    "the total mechanical energy of a system/object is the sum of its kinetic and potential energy",
    "the total mechanical energy is conserved, i.e., it can neither be created nor be destroyed",
    "an isolated system/object is one that doesn't exchange any energy with it's surroundings, i.e, doesn't have any external forces acting on it",
    "work done by external forces on a system or an object transfers energy to or from the system or the object thus, changing it's total mechanical energy",
    "the total mechanical energy of an isolated system is conserved, i.e., it can neither be created nor be destroyed"
    ]

information_questions = {}
information_questions["force is zero if the acceleration is zero"] = "What is the net force when acceleration is zero?"
information_questions["to calculate the work done by a force, we use only the force component along the object's displacement"] = "To calculate the work, is the direction of force important?"
information_questions["work done against gravity is equal to change in gravitational potential energy"] = "What is the work done against gravity?"
information_questions["work done to change the velocity is equal to the change in kinetic energy"] = "How is work done related to kinetic energy?"
information_questions["the total mechanical energy of a system/object is the sum of its kinetic and potential energy"] = "What is the total mechanical energy?"
information_questions["the total mechanical energy is conserved, i.e., it can neither be created nor be destroyed"] = "What is conservation of total mechanical energy?"
information_questions["an isolated system/object is one that doesn't exchange any energy with it's surroundings, i.e, doesn't have any external forces acting on it"] = "What is an isolated system?"
information_questions["work done by external forces on a system or an object transfers energy to or from the system or the object thus, changing it's total mechanical energy"] = "How do external forces affect the total mechanical energy?"
information_questions["the total mechanical energy of an isolated system is conserved, i.e., it can neither be created nor be destroyed"] = "Does conservation of mechanical energy only apply to isolated systems?"

information_checklist_model = "gpt-4o"
information_checklist_instructions = "You are an automated checklist. I need you to carefully read a paragraph to check if it contains some information. Your response should be a valid jsonlist called 'information_checklist' where each json object has 'information' and 'check' attributes. The 'check' can only be 'Yes', 'No', or 'Wrong'. If the paragraph contains the information, then the 'check' should be 'Yes' and if it doesn't contain the information or the informaion is unknown, the check should be 'No'. If the paragraph contradicts the information, then the 'check' should be 'Wrong'. The list of 'information' is given as follows:\n"
information_checklist_prompt_pre = "Read the given paragraph to check if it contains the information. Your 'check' should be based ONLY on the paragraph given below and can only be 'Yes', 'No', or 'Wrong'. Do NOT return 'Unknown'. \nParagraph: "

formula_reader_model = "gpt-4o"
formula_reader_instructions = "You are a latex formula reader. I need you to read over an array in latex and give me a formula that answers the given question. Your response should be a json object called 'formula'. While writing the formula, force should be denoted by 'F', distance/displacement should be denoted by 's', angle should be denoted by 'theta', mass should be denoted by 'm', acceleration should be denoted by 'a', velocity should be denoted by 'v', height should be denoted by 'h', acceleration due to gravity should be denoted by 'g', gravitational potential energy should be denoted by 'E_p', kinetic energy should be denoted by 'E_k', and spring potential energy should be denoted by 'E_s'. You can NOT use any other symbols in the formula. Follow python syntax while writing the formula. If the formula isn't mentioned, respond with 'Unknown' in the 'formula' attribute. The given question is:\n"
formula_reader_prompt_pre = "Read this array and give me a formual that answers the question. Your answer should be based ONLY on the array given below, even if it contradicts common knowledge. \nArray: "

print_working_json_model = "gpt-4o"
print_working_json_instructions = "You are a paraphraser. I need you to read a question and it's working and paraphrase it. Your response should be a json object which has the 'working' attribute. The 'working' will be a paraphrased version of the given working."
print_working_json_prompt_pre = "Help me paraphrase the working to the given question. If no working is given, return an empty string for working. \nQuestion: "
print_working_json_prompt_post = "\nWorking: "