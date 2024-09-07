import json
import os, sys
parent_dir = os.path.dirname(os.path.realpath("/Users/likhitnayak/Ira Project/shukuchi/env.py"))
sys.path.append(parent_dir)
from env import OPENAI_KEY
from openai import OpenAI
from parameters import *

client = OpenAI(
    api_key=OPENAI_KEY,
)

def read_explanation(concept_questions, explanation):
    response = client.chat.completions.create(
        model=read_explanation_model,
        messages=[
            {"role": "system", "content": read_explanation_instructions + concept_questions},
            {"role": "user", "content": read_explanation_prompt_pre + explanation},
        ],
        response_format={"type": "json_object"}
    )
    response_message = json.loads(response.choices[0].message.content)
    return response_message

def output_answer(question, solution):
    response = client.chat.completions.create(
        model=output_answer_model,
        messages=[
            {"role": "system", "content": output_answer_instructions},
            {"role": "user", "content": output_answer_prompt_pre + question + output_answer_prompt_post + solution},
        ],
        response_format={"type": "json_object"}
    )
    response_message = json.loads(response.choices[0].message.content)
    return response_message

# Open and read the JSON file
file = open("1_Electric Charge.json")
assignment = json.load(file)
file.close()

# Initialize the dictionaries
required_concepts_dict = {}
not_required_concepts_dict = {}

# Initialize the concepts in the dictionaries
for question in assignment["Questions"]:
    for concept_array in question["required_concepts"]:
        for concept in concept_array:
            required_concepts_dict[concept] = ""
    for concept in question["not_required_concepts"]:
        not_required_concepts_dict[concept] = ""

# Convert requires and not_required concepts to a list of questions
question_number = 1
question_list = ""
for concept_question in required_concepts_dict.keys():
    question_list =  question_list + str(question_number) + ") " + concept_question + "\n"
    question_number += 1
for concept_question in not_required_concepts_dict.keys():
    question_list =  question_list + str(question_number) + ") " + concept_question + "\n"
    question_number += 1

# Get answers to the question_list
learner_explantion = explanation_sample
verifications_json = read_explanation(question_list, learner_explantion)
for verification in verifications_json["verifications"]:
    if verification['verification_question'] in required_concepts_dict:
        required_concepts_dict[verification['verification_question']] = verification['verification_answer']
    elif verification['verification_question'] in not_required_concepts_dict:
        not_required_concepts_dict[verification['verification_question']] = verification['verification_answer']

# Reasoning engine for question 1
def evaluate_question_1():
    answer = ""
    correct = False
    for question in assignment["Questions"]:
        if question["question_id"] == 1:
            q = question["Question"]
            r_c = question["required_concepts"]
            k_c = question["known_concepts"]
            n_r_c = question["not_required_concepts"]
    if required_concepts_dict[r_c[0][0]] == "Yes":
        k_c.append("negative charges will repel one another")
        answer = answer + "Based on your explanation, I understood that negative charges will repel one another."
        if required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "No":
            k_c.append("conductors and insulators allow free flow of charge")
            answer = answer + "\nI also understood that conductors and insulators both allow charges to flow freely within them, so I think the negative charges present within the wollen ball and the metal sphere will try to move away from each other and come to reside on the surface."
        elif required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "Unknown":
            k_c.append("conductors allow free flow of charge")
            answer = answer + "\nI also understood that conductors allow charges to flow freely within them, so I think the negative charges present within the metal sphere will try to move away from each other and come to reside on the surface."
            answer = answer + " But, I do not know how to find out where the charges will reside on the woollen ball."
        elif required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "Yes":
            k_c.append("conductors allow free flow of charge and insulators prevent free flow of charge")
            answer = answer + " I also understood that conductors allow charges to flow freely within them while insulators prevent charges from freely flowing within them."
            answer = answer + " \nSo, the negative charges present within the metal sphere will move away from each other and come to reside on the surface while in case of the woollen ball, they will be unable to move away from each other and be distributed across the entire volume."
            correct = True
            final_answer = output_answer(q, answer) 
            return final_answer, correct
        elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "Yes":
            k_c.append("conductors and insulators both prevent charge from flowing freely within them")
            answer = answer + "\nI also understood that conductors and insulators both prevent charges from flowing freely within them, so I think the negative charges present within the wollen ball and the metal sphere will be unable to move away from each other and be distributed across the entire volume."
        elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "Unknown":
            k_c.append("conductors prevent charge from flowing freely within them")
            answer = answer + "\nI also understood that conductors prevent charges from flowing freely within them, so I think the negative charges present within the metal sphere will be unable to move away from each other and be distributed across the entire volume."
            answer = answer + " But, I do not know how to find out where the charges will reside on the woollen ball."
        elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "No":
            k_c.append("insulators allow free flow of charge and conductors prevent free flow of charge")
            answer = answer + " I also understood that insulators allow charges to flow freely within them while conductors prevent charges from freely flowing within them."
            answer = answer + " \nSo, the negative charges present within the woollen ball will move away from each other and come to reside on the surface while in case of the metal sphere, they will be unable to move away from each other and be distributed across the entire volume."
        elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "Yes":
            k_c.append("insulators prevent charge from flowing freely within them")
            answer = answer + "\nI also understood that insulators prevent charges from flowing freely within them, so I think the negative charges present within the woollen ball will be unable to move away from each other and be distributed across the entire volume."
            answer = answer + " But, I do not know how to find out where the charges will reside on the metal sphere."
        elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "No":
            k_c.append("insulators allow free flow of charge")
            answer = answer + "\nI also understood that insulators allow charges to flow freely within them, so I think the negative charges present within the woollen ball will try to move away from each other and come to reside on the surface."
            answer = answer + " But, I do not know how to find out where the charges will reside on the metal sphere."
        elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "Unknown":
            answer = answer + " So, for both the woollen ball and the metal sphere, I think the charges will try to move away from each other and reside on the surface."
    elif required_concepts_dict[r_c[0][0]] == "Unknown":
        if required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "No":
            k_c.append("conductors and insulators allow free flow of charge")
            answer = answer + "Based on your explanation, I understood that conductors and insulators both allow charges to flow freely within them, but I am not sure how to figure out where the charges will reside."
        elif required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "Unknown":
            k_c.append("conductors allow free flow of charge")
            answer = answer + "Based on your explanation, I understood that conductors allow charges to flow freely within them. But I don't know how to figure out where the charges will reside on both the woollen ball and the metal sphere."
        elif required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "Yes":
            k_c.append("conductors allow free flow of charge and insulators prevent free flow of charge")
            answer = answer + "Based on your explanation, I understood that conductors allow charges to flow freely within them while insulators prevent charges from freely flowing within them."
            answer = answer + " But I don't know how to figure out where these charges will reside."
        elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "Yes":
            k_c.append("conductors and insulators both prevent charge from flowing freely within them")
            answer = answer + "Based on your explanation, I understood that conductors and insulators both prevent charges from flowing freely within them, but I am not sure how to figure out where the charges will reside."
        elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "Unknown":
            k_c.append("conductors prevent charge from flowing freely within them")
            answer = answer + "Based on your explantion, I understood that conductors prevent charges from flowing freely within them. But I don't know how to figure out where the charges will reside."
        elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "No":
            k_c.append("insulators allow free flow of charge and conductors prevent free flow of charge")
            answer = answer + "Based on your explanation, I understood that insulators allow charges to flow freely within them while conductors prevent charges from freely flowing within them."
            answer = answer + " But I don't know how to figure out where these charges they will reside."
        elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "Yes":
            k_c.append("insulators prevent charge from flowing freely within them")
            answer = answer + "Based on your explanation, I understood that insulators prevent charges from flowing freely within them, but I am not sure how to figure out where these charges will reside."
        elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "No":
            k_c.append("insulators allow free flow of charge")
            answer = answer + "Based on your explanation, I understood that insulators allow charges to flow freely within them, but I am not sure how how to figure out where these charges will reside."
        elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "Unknown":
            answer = answer + "I can't figure how to answer this question based on your explanation."
    elif required_concepts_dict[r_c[0][0]] == "No":
        follow_up_json = read_explanation("1) Do negative charges attract each other?", learner_explantion)
        if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
            k_c.append("negative charges will attract one another")
            answer = answer + "Based on your explanation, I understood that negative charges will attract one another."
            if required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "No":
                k_c.append("conductors and insulators allow free flow of charge")
                answer = answer + "\nI also understood that conductors and insulators both allow charges to flow freely within them, so I think the negative charges present within the wollen ball and the metal sphere will try to move towards each other and come to reside in the center."
            elif required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "Unknown":
                k_c.append("conductors allow free flow of charge")
                answer = answer + "\nI also understood that conductors allow charges to flow freely within them, so I think the negative charges present within the metal sphere will try to move towards each other and come to reside in the center."
                answer = answer + " But, I do not know how to find out where the charges will reside on the woollen ball."
            elif required_concepts_dict[r_c[0][1]] == "Yes" and required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append("conductors allow free flow of charge and insulators prevent free flow of charge")
                answer = answer + " I also understood that conductors allow charges to flow freely within them while insulators prevent charges from freely flowing within them."
                answer = answer + " \nSo, the negative charges present within the metal sphere will move towards each other and come to reside in the center while in case of the woollen ball, they will be unable to move towards each other and be distributed across the entire volume."
            elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append("conductors and insulators both prevent charge from flowing freely within them")
                answer = answer + "\nI also understood that conductors and insulators both prevent charges from flowing freely within them, so I think the negative charges present within the wollen ball and the metal sphere will be unable to move towards each other and be distributed across the entire volume."
            elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "Unknown":
                k_c.append("conductors prevent charge from flowing freely within them")
                answer = answer + "\nI also understood that conductors prevent charges from flowing freely within them, so I think the negative charges present within the metal sphere will be unable to move towards each other and be distributed across the entire volume."
                answer = answer + " But, I do not know how to find out where the charges will reside on the woollen ball."
            elif required_concepts_dict[r_c[0][1]] == "No" and required_concepts_dict[r_c[0][2]] == "No":
                k_c.append("insulators allow free flow of charge and conductors prevent free flow of charge")
                answer = answer + " I also understood that insulators allow charges to flow freely within them while conductors prevent charges from freely flowing within them."
                answer = answer + " \nSo, the negative charges present within the woollen ball will move towards each other and come to reside in the center while in case of the metal sphere, they will be unable to move towards each other and be distributed across the entire volume."
            elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append("insulators prevent charge from flowing freely within them")
                answer = answer + "\nI also understood that insulators prevent charges from flowing freely within them, so I think the negative charges present within the woollen ball will be unable to move towards each other and be distributed across the entire volume."
                answer = answer + " But, I do not know how to find out where the charges will reside on the metal sphere."
            elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "No":
                k_c.append("insulators allow free flow of charge")
                answer = answer + "\nI also understood that insulators allow charges to flow freely within them, so I think the negative charges present within the woollen ball will try to move towards each other and come to reside in the center."
                answer = answer + " But, I do not know how to find out where the charges will reside on the metal sphere."
            elif required_concepts_dict[r_c[0][1]] == "Unknown" and required_concepts_dict[r_c[0][2]] == "Unknown":
                answer = answer + " So, for both the woollen ball and the metal sphere, I think the charges will try to move towards each other and reside in the center."
        elif follow_up_json["verifications"][0]['verification_answer'] == "No":
            k_c.append("negative charges will neither attract nor repel one another")
            answer = answer + "Based on your explanation, I understood that negative charges will have no effect on each other. So the charges will be distributed across the entire volume in both the woollen ball and the metal sphere."
    if not_required_concepts_dict[n_r_c[0]] == "Yes" and not_required_concepts_dict[n_r_c[1]] == "Yes":
        answer = "You mentioned that charges reside on the surface of the conductor and are present across the volume of an insulator. But can you explain how to come to that conclusion?\n" + answer
    else:
        if not_required_concepts_dict[n_r_c[0]] == "Yes":
            answer = "You mentioned that charges reside on the surface of the conductor. But can you explain how to come to that conclusion?\n" + answer
        if not_required_concepts_dict[n_r_c[1]] == "Yes":
            answer = "You mentioned that charges are present across the volume of an insulator. But can you explain how to come to that conclusion?\n" + answer
    final_answer = output_answer(q, answer) 
    return final_answer, correct    

print(evaluate_question_1())

