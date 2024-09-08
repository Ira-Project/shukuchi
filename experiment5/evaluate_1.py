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
        response_format={"type": "json_object"},
        temperature=0.5
    )
    response_message = json.loads(response.choices[0].message.content)
    print(response_message)
    return response_message

def answer_explanation(concept_question, explanation, json_instruction):
    response = client.chat.completions.create(
        model=answer_explanation_model,
        messages=[
            {"role": "system", "content": answer_explanation_instructions + concept_question + "\n" + json_instruction},
            {"role": "user", "content": answer_explanation_prompt_pre + explanation},
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
    # question_list =  question_list + str(question_number) + ") " + concept_question + "\n"
    question_list =  question_list + concept_question + "\n"
    question_number += 1
for concept_question in not_required_concepts_dict.keys():
    question_list =  question_list + concept_question + "\n"
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
        else:
            k_c.append("negative charges will neither attract nor repel one another")
            answer = answer + "Based on your explanation, I understood that negative charges will have no effect on each other. So the charges will be distributed across the entire volume in both the woollen ball and the metal sphere."
    if not correct:
        if not_required_concepts_dict[n_r_c[0]] == "Yes" and not_required_concepts_dict[n_r_c[1]] == "Yes":
            answer = "You mentioned that charges reside on the surface of the conductor and are present across the volume of an insulator. But can you explain how to come to that conclusion?\n" + answer
        else:
            if not_required_concepts_dict[n_r_c[0]] == "Yes":
                answer = "You mentioned that charges reside on the surface of the conductor. But can you explain how to come to that conclusion?" + "\n" + answer
            if not_required_concepts_dict[n_r_c[1]] == "Yes":
                answer = "You mentioned that charges are present across the volume of an insulator. But can you explain how to come to that conclusion?" + "\n" + answer
    final_answer = output_answer(q, answer) 
    return final_answer, correct    

# Reasoning engine for question 2
def evaluate_question_2():
    answer = ""
    correct = False
    for question in assignment["Questions"]:
        if question["question_id"] == 2:
            q = question["Question"]
            r_c = question["required_concepts"]
            k_c = question["known_concepts"]
            n_r_c = question["not_required_concepts"]
    if required_concepts_dict[r_c[0][0]] == "Yes":
        k_c.append("there are two types of charges")
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("positive and negative charges are the two types of charges")
            if required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append("opposite charges attract each other")
                answer = answer + "Based on your explanation, I understood that positive and negative charges are two types of charges and opposite charges attract each other."
                answer = answer + " So, one metal sphere will have a postive charge and the other will have a negative charge."
                correct1 = True
            elif required_concepts_dict[r_c[0][2]] == "No":
                follow_up_json = read_explanation("Do opposite charges repel each other?", learner_explantion)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    k_c.append("opposite charges repel each other")
                    answer = answer + "Based on your explanation, I understood that positive and negative charges are two types of charges and opposite charges repel each other."
                    answer = answer + " But, I don't know how to figure out which charges are on the spheres."
                elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                    k_c.append("opposite charges neither attract nor repel each other")
                    answer = answer + "Based on your explanation, I understood that positive and negative charges are two types of charges and opposite charges neither attract nor repel each other."
                    answer = answer + " But, I don't know how to figure out which charges are on the spheres."
                else:
                    follow_up_json = read_explanation("Do like charges attract each other?", learner_explantion)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("like charges attract each other")
                        nswer1 = answer + "Based on your explanation, I understood that positive and negative charges are two types of charges and like charges attract each other."
                        answer = answer + " So, both the metal spheres have a postive charge or both have a negative charge."
                    else:
                        answer = answer + "Based on your explanation, I understood that positive and negative charges are two types of charges and opposite charges do not attract each other."
                        answer = answer + " So, the spheres don't have opposite charges on them. Maybe both the metal spheres have a postive charge or maybe both have a negative charge."
            elif required_concepts_dict[r_c[0][2]] == "Unknown":
                 answer = answer + "Based on your explanation, I understood that positive and negative charges are two types of charges but using just that, I don't know how to determine the nature of the charges on the spheres that attract one another."
        elif required_concepts_dict[r_c[0][1]] == "No":
            follow_up_answer = answer_explanation("What are the two types of charges?", learner_explantion, "Your response should be a json object 'charges' containing an array of the two types of charges.")
            charge_1 = follow_up_answer['charges'][0]
            charge_2 = follow_up_answer['charges'][1]
            print(follow_up_answer)
            k_c.append(charge_1 + " and " + charge_2 + " are the two types of charges")
            if required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append(charge_1 + " and " + charge_2 + " charges attract each other")
                answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + charge_2 + " are the two types of charges and opposite charges attract each other."
                answer = answer + " So, one metal sphere will have a " + charge_1 + " charge and the other will have a " + charge_2 + " charge."
            elif required_concepts_dict[r_c[0][2]] == "No":
                follow_up_json = read_explanation("Do opposite charges repel each other?", learner_explantion)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    k_c.append("opposite charges repel each other")
                    answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + charge_2 + " are the two types of charges and opposite charges repel each other."
                    answer = answer + " But, I don't know how to figure out which charges are on the spheres."
                elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                    k_c.append("opposite charges neither attract nor repel each other")
                    answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + charge_2 + " are the two types of charges and opposite charges neither attract nor repel each other."
                    answer = answer + " But, I don't know how to figure out which charges are on the spheres."
                else:
                    follow_up_json = read_explanation("Do like charges attract each other?", learner_explantion)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("like charges attract each other")
                        nswer1 = answer + "Based on your explanation, I understood that " + charge_1 + " and " + charge_2 + " are the two types of charges and like charges attract each other."
                        answer = answer + " So, both the metal spheres have a " + charge_1 + " charge or both have a " + charge_2 + " charge."
                    else:
                        answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + charge_2 + " are the two types of charges and opposite charges do not attract each other."
                        answer = answer + " So, the spheres don't have opposite charges on them. Maybe both the metal spheres have a " + charge_1 + " charge or maybe both have a " + charge_2 + " charge."
            elif required_concepts_dict[r_c[0][2]] == "Unknown":
                 answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + charge_2 + " are the two types of charges but using just that, I don't know how to determine the nature of the charges on the spheres that attract one another."
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            if required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append("opposite charges attract each other")
                answer = answer + "Based on your explanation, I understood that there are two types of charges and opposite charges attract each other."
                answer = answer + " So, the two metal spheres will have opposite charges on them. But can you specify what these opposite charges are?"
            elif required_concepts_dict[r_c[0][2]] == "No":
                follow_up_json = read_explanation("Do opposite charges repel each other?", learner_explantion)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    k_c.append("opposite charges repel each other")
                    answer = answer + "Based on your explanation, I understood that there are two types of charges and opposite charges repel each other."
                    answer = answer + " So, the two metal spheres will not have opposite charges on them. But I do not know what the specific nature of the charges will be."
                elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                    k_c.append("opposite charges neither attract nor repel each other")
                    answer = answer + "Based on your explanation, I understood that there are two types of charges and opposite charges neither attract nor repel each other."
                    answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                else:
                    follow_up_json = read_explanation("Do like charges attract each other?", learner_explantion)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("like charges attract each other")
                        nswer1 = answer + "Based on your explanation, I understood that there are the two types of charges and like charges attract each other."
                        answer = answer + " So, both the metal spheres have like charges."
                    else:
                        answer = answer + "Based on your explanation, I understood that there are two types of charges and opposite charges do not attract each other."
                        answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
            elif required_concepts_dict[r_c[0][2]] == "Unknown":
                 answer = answer + "Based on your explanation, I understood that there are two types of charges but using just that, I don't know how to determine the nature of the charges on the sphere."
    elif required_concepts_dict[r_c[0][0]] == "No":
        follow_up_json = read_explanation("Is there less than two types of charges?", learner_explantion)
        if follow_up_json["verifications"][0]['verification_answer'] == "Yes" or follow_up_json["verifications"][0]['verification_answer'] == "Unknown":
            k_c.append("there is one type of charges")
            answer = answer + "Based on your explanation, I understood that there is only one type of charge. So both the spheres will have that charge on them."
        elif follow_up_json["verifications"][0]['verification_answer'] == "No":
            follow_up_answer = answer_explanation("How many types of charges are there?", learner_explantion, "Your response should be a json object 'number of types of charges' containing the number of types of charges")
            number_of_type_of_charges = follow_up_answer['number of types of charges']
            if not isinstance(number_of_type_of_charges, str):
                number_of_type_of_charges = str(number_of_type_of_charges)
            k_c.append("there are " + number_of_type_of_charges + " types of charges")
            if required_concepts_dict[r_c[0][1]] == "Yes":
                k_c.append("positive and negative charges are two types of charges")
                if required_concepts_dict[r_c[0][2]] == "Yes":
                    k_c.append("opposite charges attract each other")
                    answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + " types of charges and positive and negative charges attract each other."
                    answer = answer + " So, one metal sphere will have a postive charge and the other will have a negative charge."
                elif required_concepts_dict[r_c[0][2]] == "No":
                    follow_up_json = read_explanation("Do opposite charges repel each other?", learner_explantion)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("opposite charges repel each other")
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + " types of charges and positive and negative charges repel each other."
                        answer = answer + " So, the two metal spheres will not have opposite charges on them. But I do not know what the specific nature of the charges will be."
                    elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                        k_c.append("opposite charges neither attract nor repel each other")
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + " types of charges and positive and negative charges neither attract nor repel each other."
                        answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                    else:
                        follow_up_json = read_explanation("Do like charges attract each other?", learner_explantion)
                        if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                            k_c.append("like charges attract each other")
                            nswer1 = answer + "Based on your explanation, I understood that there are "+ number_of_type_of_charges + " two types of charges and like charges attract each other."
                            answer = answer + " So, both the metal spheres have like charges on them."
                        else:
                            answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + " types of charges and positive and negative charges do not attract each other."
                            answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                elif required_concepts_dict[r_c[0][2]] == "Unknown":
                    follow_up_json = read_explanation("Do any of the two charges attract each other?", learner_explantion)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        follow_up_answer = answer_explanation("Which two charges attract each other?", learner_explantion, "Your response should be a json object 'charges' containing an array of the charges that attract each other.")
                        charge_1 = follow_up_answer['charges'][0]
                        charge_2 = follow_up_answer['charges'][1]
                        k_c.append(charge_1 + " and " + charge_2 + " charges attract each other")
                        answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + charge_2 + " charges attract each other."
                        answer = answer + " So, one metal sphere will have a " + charge_1 + " charge and the other will have a " + charge_2 + " charge."
                    elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + " and none of them attract each other. So, I don't know how to figure out the nature of the charges on the sphere."
                    else:
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + " but using just that, I don't know how to determine the nature of the charges on the sphere."
            elif required_concepts_dict[r_c[0][1]] == "No" or required_concepts_dict[r_c[0][1]] == "Unknown":        
                if required_concepts_dict[r_c[0][2]] == "Yes":
                    k_c.append("opposite charges attract each other")
                    answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + " types of charges and opposite charges attract each other."
                    answer = answer + " So, the two metal spheres will have opposite charges on them."
                elif required_concepts_dict[r_c[0][2]] == "No":
                    follow_up_json = read_explanation("Do opposite charges repel each other?", learner_explantion)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("opposite charges repel each other")
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + " types of charges and opposite charges repel each other."
                        answer = answer + " So, the two metal spheres will not have opposite charges on them. But I do not know what the specific nature of the charges will be."
                    elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                        k_c.append("opposite charges neither attract nor repel each other")
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + " types of charges and opposite charges neither attract nor repel each other."
                        answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                    else:
                        follow_up_json = read_explanation("Do like charges attract each other?", learner_explantion)
                        if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                            k_c.append("like charges attract each other")
                            nswer1 = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + " charges and like charges attract each other."
                            answer = answer + " So, both the metal spheres have a like charges on them."
                        else:
                            answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + " types of charges and opposite charges do not attract each other."
                            answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                elif required_concepts_dict[r_c[0][2]] == "Unknown":
                    follow_up_json = read_explanation("Do any of the two charges attract each other?", learner_explantion)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        follow_up_answer = answer_explanation("Which two charges attract each other?", learner_explantion, "Your response should be a json object 'charges' containing an array of the charges that attract each other.")
                        charge_1 = follow_up_answer['charges'][0]
                        charge_2 = follow_up_answer['charges'][1]
                        k_c.append(charge_1 + " and " + charge_2 + " charges attract each other")
                        answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + charge_2 + " charges attract each other."
                        answer = answer + " So, one metal sphere will have a " + charge_1 + " charge and the other will have a " + charge_2 + " charge."
                    elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + " and none of them attract each other. So, I don't know how to figure out the nature of the charges on the sphere."   
                    else:
                        answer = answer + "Based on your explanation, I understood that there are " + number_of_type_of_charges + " but using just that, I don't know how to determine the nature of the charges on the sphere."
    elif required_concepts_dict[r_c[0][0]] == "Unknown":
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("positive and negative charges are two types of charges")
            if required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append("opposite charges attract each other")
                answer = answer + "Based on your explanation, I understood that positive and negative charges attract each other."
                answer = answer + " So, one metal sphere will have a postive charge and the other will have a negative charge."
            elif required_concepts_dict[r_c[0][2]] == "No":
                follow_up_json = read_explanation("Do opposite charges repel each other?", learner_explantion)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    k_c.append("opposite charges repel each other")
                    answer = answer + "Based on your explanation, I understood that positive and negative charges repel each other."
                    answer = answer + " So, the two metal spheres will not have opposite charges on them. But I do not know what the specific nature of the charges will be."
                elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                    k_c.append("opposite charges neither attract nor repel each other")
                    answer = answer + "Based on your explanation, I understood that positive and negative charges neither attract nor repel each other."
                    answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                else:
                    follow_up_json = read_explanation("Do like charges attract each other?", learner_explantion)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("like charges attract each other")
                        nswer1 = answer + "Based on your explanation, I understood that like charges attract each other."
                        answer = answer + " So, both the metal spheres have a positive charge or both have a negative charge."
                    else:
                        answer = answer + "Based on your explanation, I understood that positive and negative charges do not attract each other."
                        answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
            elif required_concepts_dict[r_c[0][2]] == "Unknown":
                answer = answer + "I cannot figure out the nature of the charges on the sphere."
        elif required_concepts_dict[r_c[0][1]] == "No" or required_concepts_dict[r_c[0][1]] == "Unknown":
            if required_concepts_dict[r_c[0][2]] == "Yes":
                follow_up_json = read_explanation("Do positive and negative charges attract each other?", learner_explantion)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    k_c.append("positive and negative charges attract each other")
                    answer = answer + "Based on your explanation, I understood that positive and negative charges attract each other."
                    answer = answer + " So, one metal sphere will have a positive charge and the other will have a negative charge."
                    correct1 = True
                else:
                    k_c.append("opposite charges attract each other")
                    answer = answer + "Based on your explanation, I understood that opposite charges attract each other."
                    answer = answer + " So, the two metal spheres will have opposite charges on them."
            elif required_concepts_dict[r_c[0][2]] == "No":
                follow_up_json = read_explanation("Do opposite charges repel each other?", learner_explantion)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    k_c.append("opposite charges repel each other")
                    answer = answer + "Based on your explanation, I understood that opposite charges repel each other."
                    answer = answer + " So, the two metal spheres will not have opposite charges on them. But I do not know what the specific nature of the charges will be."
                elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                    k_c.append("opposite charges neither attract nor repel each other")
                    answer = answer + "Based on your explanation, I understood that opposite charges neither attract nor repel each other."
                    answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
                else:
                    follow_up_json = read_explanation("Do like charges attract each other?", learner_explantion)
                    if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                        k_c.append("like charges attract each other")
                        nswer1 = answer + "Based on your explanation, I understood that like charges attract each other."
                        answer = answer + " So, both the metal spheres have like charges but I can't figure out the specific nature of the charges."
                    else:
                        answer = answer + "Based on your explanation, I understood that opposite charges do not attract each other."
                        answer = answer + " So, the spheres don't have opposite charges on them but I can't figure out the specific nature of the charges."
            elif required_concepts_dict[r_c[0][2]] == "Unknown":
                follow_up_json = read_explanation("Do any of the two charges attract each other?", learner_explantion)
                if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                    follow_up_answer = answer_explanation("Which two charges attract each other?", learner_explantion, "Your response should be a json object 'charges' containing an array of the charges that attract each other.")
                    charge_1 = follow_up_answer['charges'][0]
                    charge_2 = follow_up_answer['charges'][1]
                    k_c.append(charge_1 + " and " + charge_2 + " charges attract each other")
                    answer = answer + "Based on your explanation, I understood that " + charge_1 + " and " + charge_2 + " charges attract each other."
                    answer = answer + " So, one metal sphere will have a " + charge_1 + " charge and the other will have a " + charge_2 + " charge."
                else:
                    answer = answer + "Based on your explanation, I don't know how to determine the nature of the charges on the sphere."
    final_answer = output_answer(q, answer) 
    return final_answer, correct 


# Reasoning engine for question 3
def evaluate_question_3():
    answer1 = ""
    answer2 = ""
    imageOutput = ""
    image1 = "" # The plates and the sphere become neutral
    image2 = "" # The charges in the sphere will be distributed across the entire volume (sphere is an insulator)
    image3 = "" # The charges in the sphere will be attracted towards the same charged plate
    imageCorrect = ""
    correct1 = False
    correct2 = False
    for question in assignment["Questions"]:
        if question["question_id"] == 3:
            q = question["Question"]
            r_c = question["required_concepts"]
            k_c = question["known_concepts"]
            n_r_c = question["not_required_concepts"]
    if required_concepts_dict[r_c[0][0]] == "Yes":
        k_c.append("charges are conserved")
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("insulators prevent charges from flowing freely")
            answer1 = answer1 + "Since charges can't be created or destroyed and they can't be transferred through air, the metal sphere will remain neutral."
            correct1 = True
        elif required_concepts_dict[r_c[0][1]] == "No":
            k_c.append("insulators allow charges to flow freely")
            answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through air, the charges from the negative plate will flow through air and the metal sphere and cancel out the charges on the positive plate."
            imageOutput = image1
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            follow_up_json = read_explanation("Can charges be transferred through air?", learner_explantion)
            if follow_up_json["verifications"][0]['verification_answer'] == "No":
                k_c.append("charges can't flow through air")
                answer1 = answer1 + "Since charges can't be created or destroyed and they can't be transferred through air, the metal sphere will remain neutral."
                correct1 = True
            elif follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                k_c.append("charges can flow through air")
                answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through air, the charges from the negative plate will flow through air and the metal sphere and cancel out the charges on the positive plate."
                imageOutput = image1
            else:
                k_c.append("charges may flow through air")
                answer1 = answer1 + "Since charges can't be created or destroyed but they may be transferred through air, the charges from the negative plate may flow through air and the metal sphere and cancel out the charges on the positive plate."
                imageOutput = image1
    elif required_concepts_dict[r_c[0][0]] == "No":
        k_c.append("charges are not conserved")
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("insulators prevent charges from flowing freely")
            answer1 = answer1 + "I understand that charges can't be transferred through air but they can be created or destroyed."
            answer1 = answer1 + " So, I can't figure out the charge on the sphere."
        elif required_concepts_dict[r_c[0][1]] == "No":
            k_c.append("insulators allow charges to flow freely")
            answer1 = answer1 + "Since charges can be created, destroyed, and transferred through air, the charges from the negative plate may flow through air and the metal sphere and cancel out the charges on the positive plate."
            answer1 = answer1 + " New charges may also be created or old ones may be destroyed. So, I can't figure out the charge on the sphere."
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            answer1 = answer1 + " New charges may also be created or old ones may be destroyed. So, I can't figure out the charge on the sphere."
    elif required_concepts_dict[r_c[0][0]] == "Unknown":
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("insulators prevent charges from flowing freely")
            answer1 = answer1 + "I understand that charges can't be transferred through air but they may be created or destroyed."
            answer1 = answer1 + " So, I can't figure out the charge on the sphere."
        elif required_concepts_dict[r_c[0][1]] == "No":
            k_c.append("insulators allow charges to flow freely")
            answer1 = answer1 + "Since charges can be transferred through air, the charges from the negative plate may flow through air and the metal sphere and cancel out the charges on the positive plate."
            answer1 = answer1 + " But, new charges may also be created or old ones may be destroyed. So, I can't figure out the charge on the sphere."
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            answer1 = answer1 + " New charges may also be created or old ones may be destroyed. So, I can't figure out the charge on the sphere."
    # Second part
    if correct1:
        if required_concepts_dict[r_c[1][0]] == "Yes":
            k_c.append("positive and negative charges attract each other")
            if required_concepts_dict[r_c[1][1]] == "Yes":
                k_c.append("conductors allow free flow of charges within them")  
                answer2 = answer2 + "The charges in the metal sphere will be attracted towards the oppositely charged metal plate."
                correct2 = True
                imageOutput = imageCorrect
            elif required_concepts_dict[r_c[1][1]] == "No":
                k_c.append("conductors prevent free flow of charges within them") 
                answer2 = answer2 + "The charges in the metal sphere will be attracted towards the oppositely charged metal plate but won't be able to move through the conductor."
                imageOutput = image2
            elif required_concepts_dict[r_c[1][1]] == "Unknown":
                if not_required_concepts_dict[n_r_c[0]] == "Yes":
                    k_c.append("polarization is the separation of charges in a material")
                    answer2 = answer2 + "I understand that metal sphere might be polarized and the charges in the metal sphere will be attracted towards the oppositely charged metal plate."
                    correct2 = True
                    imageOutput = imageCorrect
                else:
                    answer2 = answer2 + "The charges in the metal sphere will be attracted towards the oppositely charged metal plate but I don't know if they will be able to move."
                    imageOutput = image2
        elif required_concepts_dict[r_c[1][0]] == "No":
            follow_up_json = read_explanation("Do positive and negative charges repel each other?", learner_explantion)
            if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                k_c.append("positive and negative charges repel each other")
                if required_concepts_dict[r_c[1][1]] == "Yes":
                    k_c.append("conductors allow free flow of charges within them")  
                    answer2 = answer2 + "The charges in the metal sphere will be attracted towards the similarly charged metal plate."
                    imageOutput = image3
                elif required_concepts_dict[r_c[1][1]] == "No":
                    k_c.append("conductors prevent free flow of charges within them") 
                    answer2 = answer2 + "The charges in the metal sphere will be attracted towards the similarly charged metal plate but won't be able to move through the conductor."
                    imageOutput = image2
                elif required_concepts_dict[r_c[1][1]] == "Unknown":
                    if not_required_concepts_dict[n_r_c[0]] == "Yes":
                        k_c.append("polarization is the separation of charges in a material")
                        answer2 = answer2 + "I understand that metal sphere might be polarized and the charges in the metal sphere will be attracted towards the similarly charged metal plate."
                        imageOutput = image3
                    else:
                        answer2 = answer2 + "The charges in the metal sphere will be attracted towards the similarly charged metal plate but I don't know if they will be able to move."
                        imageOutput = image2
            elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                k_c.append("positive and negative charges do not attract or repel each other")
                answer2 = answer2 + "The charges in the metal sphere will neither be attracted nor be repelled."
                imageOutput = image2
            elif follow_up_json["verifications"][0]['verification_answer'] == "Unknown":
                k_c.append("positive and negative charges do not attract each other")
                answer2 = answer2 + "I understand that positive and negative charges do not attract each other."
                answer2 = answer2 + " But, I am not sure how to draw the charges on the sphere."
        elif required_concepts_dict[r_c[1][0]] == "Unknown":
            if not_required_concepts_dict[n_r_c[0]] == "Yes":
                k_c.append("polarization is the separation of charges in a material")
                answer2 = answer2 + "I understand that metal sphere might be polarized but I am not sure how."
            else:
                answer2 = answer2 + "Based on your explanation, I am not sure how to draw the charges on the sphere."
    answer = answer1 + "\n" + answer2
    correct = correct1 and correct2
    final_answer = output_answer(q, answer)
    return final_answer, correct

# Reasoning engine for question 4
def evaluate_question_4():
    answer1 = ""
    answer2 = ""
    imageOutput = ""
    imageCorrect = ""
    image1 = "" # The rod and both the spheres are neutral
    image2 = "" # There is no grounding
    image3 = "" # Original image
    image4 = "" # Correct image but with opposite charges attracting one another
    correct1 = False
    correct2 = False
    for question in assignment["Questions"]:
        if question["question_id"] == 4:
            q = question["Question"]
            r_c = question["required_concepts"]
            k_c = question["known_concepts"]
            n_r_c = question["not_required_concepts"]
    if required_concepts_dict[r_c[0][0]] == "Yes":
        k_c.append("charges are conserved")
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("insulators prevent charges from flowing freely")
            correct1 = True
        elif required_concepts_dict[r_c[0][1]] == "No":
            k_c.append("insulators allow charges to flow freely")
            answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through air or plastic, the charges will get neutralized with the environment or ground."
            imageOutput = image1
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            follow_up_json = read_explanation("Can charges be transferred through air?" + "\n" + "Can charges be transferred through plastic?", learner_explantion)
            if follow_up_json["verifications"][0]['verification_answer'] == "No" and follow_up_json["verifications"][1]['verification_answer'] == "No":
                k_c.append("charges can't flow through air or plastic")
                correct1 = True
            elif follow_up_json["verifications"][0]['verification_answer'] == "No" and follow_up_json["verifications"][1]['verification_answer'] == "Yes":
                k_c.append("charges can flow through plastic")
                answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through plastic, the charges will get neutralized with the ground."
                imageOutput = image1
            elif follow_up_json["verifications"][0]['verification_answer'] == "No" and follow_up_json["verifications"][1]['verification_answer'] == "Unknown":
                k_c.append("charges may flow through plastic")
                answer1 = answer1 + "Since charges can't be created or destroyed but they may be transferred through plastic, the charges will get neutralized with the ground."
                imageOutput = image1
            elif follow_up_json["verifications"][0]['verification_answer'] == "Yes" and follow_up_json["verifications"][1]['verification_answer'] == "No":
                k_c.append("charges can flow through air")
                answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through air, the charges will get neutralized with the environment."
                imageOutput = image1
            elif (follow_up_json["verifications"][0]['verification_answer'] == "Yes" or follow_up_json["verifications"][0]['verification_answer'] == "Unknown") and (follow_up_json["verifications"][1]['verification_answer'] == "Yes" or follow_up_json["verifications"][1]['verification_answer'] == "Unknown"):
                k_c.append("charges may flow through air or plastic")
                answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through air or plastic, the charges will get neutralized."
                imageOutput = image1
            elif follow_up_json["verifications"][0]['verification_answer'] == "Unknown" and follow_up_json["verifications"][1]['verification_answer'] == "No":
                k_c.append("charges may flow through air")
                answer1 = answer1 + "Since charges can't be created or destroyed but they can be transferred through air, the charges will get neutralized with the environment."
                imageOutput = image1
    elif required_concepts_dict[r_c[0][0]] == "No":
        k_c.append("charges are not conserved")
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("insulators prevent charges from flowing freely")
            answer1 = answer1 + "I understand that charges can't be transferred through air or plastic but they can be created or destroyed."
            answer1 = answer1 + " So, I can't figure out how to draw that charges."
        elif required_concepts_dict[r_c[0][1]] == "No":
            k_c.append("insulators allow charges to flow freely")
            answer1 = answer1 + "Since charges can be created, destroyed, and transferred through air or plastic, the charges from the rod may flow in all directions."
            answer1 = answer1 + " New charges may also be created or old ones may be destroyed. So, I can't figure out how to draw that charges."
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            answer1 = answer1 + "New charges may also be created or old ones may be destroyed. So, I can't figure out how to draw that charges."
    elif required_concepts_dict[r_c[0][0]] == "Unknown":
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("insulators prevent charges from flowing freely")
            answer1 = answer1 + "I understand that charges can't be transferred through air or plastic but they may be created or destroyed."
            answer1 = answer1 + " So, I can't figure out the charge on the sphere."
        elif required_concepts_dict[r_c[0][1]] == "No":
            k_c.append("insulators allow charges to flow freely")
            answer1 = answer1 + "Since charges can be created, destroyed, and transferred through air or plastic, the charges from the rod may flow in all directions."
            answer1 = answer1 + " New charges may also be created or old ones may be destroyed. So, I can't figure out how to draw that charges."
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            answer1 = answer1 + "New charges may also be created or old ones may be destroyed. So, I can't figure out how to draw that charges."
    # Second part
    if correct1:
        if required_concepts_dict[r_c[1][0]] == "Yes":
            k_c.append("positive and negative charges attract each other")
            if required_concepts_dict[r_c[1][1]] == "Yes":
                k_c.append("conductors allow free flow of charges within them")  
                if required_concepts_dict[r_c[1][2]] == "Yes":
                    k_c.append("grounding removes excess charges")
                    correct2 = True
                    imageOutput = imageCorrect
                elif required_concepts_dict[r_c[1][2]] == "No" or required_concepts_dict[r_c[1][2]] == "Unknown":
                    imageOutput = image2
            elif required_concepts_dict[r_c[1][1]] == "No":
                k_c.append("conductors prevent free flow of charges within them")
                answer2 = answer2 + "The charges will not be able to flow within the metal spheres."
                imageOutput = image3
            elif required_concepts_dict[r_c[1][1]] == "Unknown":
                if not_required_concepts_dict[n_r_c[0]] == "Yes":
                    k_c.append("polarization is the separation of charges in a material")
                    if required_concepts_dict[r_c[1][2]] == "Yes":
                        k_c.append("grounding removes excess charges")
                        correct2 = True
                        imageOutput = imageCorrect
                    elif required_concepts_dict[r_c[1][2]] == "No" or required_concepts_dict[r_c[1][2]] == "Unknown":
                        imageOutput = image2
                else:
                    answer2 = answer2 + "The charges in the metal sphere will be attracted towards the oppositel charges but I don't know if they will be able to move."
                    imageOutput = image3
        elif required_concepts_dict[r_c[1][0]] == "No":
            follow_up_json = read_explanation("Do positive and negative charges repel each other?", learner_explantion)
            if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                if required_concepts_dict[r_c[1][1]] == "Yes":
                    k_c.append("conductors allow free flow of charges within them")  
                    if required_concepts_dict[r_c[1][2]] == "Yes":
                        k_c.append("grounding removes excess charges")
                        answer2 = answer2 + "I understood that opposite charges will repel each other."
                        imageOutput = image4
                    elif required_concepts_dict[r_c[1][2]] == "No" or required_concepts_dict[r_c[1][2]] == "Unknown":
                        imageOutput = image2
                elif required_concepts_dict[r_c[1][1]] == "No":
                    k_c.append("conductors prevent free flow of charges within them")
                    answer2 = answer2 + "The charges will not be able to flow within the metal spheres."
                    imageOutput = image3
                elif required_concepts_dict[r_c[1][1]] == "Unknown":
                    if not_required_concepts_dict[n_r_c[0]] == "Yes":
                        k_c.append("polarization is the separation of charges in a material")
                        if required_concepts_dict[r_c[1][2]] == "Yes":
                            k_c.append("grounding removes excess charges")
                            answer2 = answer2 + "I understood that opposite charges will repel each other."
                            imageOutput = image4
                        elif required_concepts_dict[r_c[1][2]] == "No" or required_concepts_dict[r_c[1][2]] == "Unknown":
                            imageOutput = image2
                    else:
                        answer2 = answer2 + "The charges in the metal sphere will repel from the opposite charge but I don't know if they will be able to move."
                        imageOutput = image3
            elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                k_c.append("positive and negative charges do not attract or repel each other")
                answer2 = answer2 + "The charges in the metal sphere will neither be attracted nor be repelled."
                imageOutput = image3
            elif follow_up_json["verifications"][0]['verification_answer'] == "Unknown":
                k_c.append("positive and negative charges do not attract each other")
                answer2 = answer2 + "I understand that positive and negative charges do not attract each other."
                answer2 = answer2 + " But, I am not sure how to draw the charges on the sphere."
        elif required_concepts_dict[r_c[1][0]] == "Unknown":
            if not_required_concepts_dict[n_r_c[0]] == "Yes":
                k_c.append("polarization is the separation of charges in a material")
                answer2 = answer2 + "I understand that metal sphere might be polarized but I am not sure how."
            if not_required_concepts_dict[n_r_c[1]] == "Yes":
                answer2 = answer2 + " I understand that transfer of charges without contact is called induction but I don't know how it works."
    answer = answer1 + "\n" + answer2
    correct = correct1 and correct2
    final_answer = output_answer(q, answer)
    return final_answer, correct
    
# Reasoning engine for question 5
def evaluate_question_5():
    answer = ""
    correct = False
    for question in assignment["Questions"]:
        if question["question_id"] == 5:
            q = question["Question"]
            r_c = question["required_concepts"]
            k_c = question["known_concepts"]
            n_r_c = question["not_required_concepts"]
    if required_concepts_dict[r_c[0][0]] == "Yes":
        k_c.append("charges are conserved")
        if required_concepts_dict[r_c[0][1]] == "Yes":
            k_c.append("positive charges repel each other")
            if required_concepts_dict[r_c[0][2]] == "Yes":
                k_c.append("conductors allow charges to flow freely within them")
                answer = answer + "The positive charges will repel each other and move away towards the metal ruler, which will have a positive charge."
                correct = True
            elif required_concepts_dict[r_c[0][2]] == "No":
                k_c.append("conductors do not allow charges to flow freely within them")
                answer = answer + "The positive charges will repel each other and but won't be able to move away."
                answer = answer + " The metal ruler will remain neutral."
            elif required_concepts_dict[r_c[0][2]] == "Unknown":
                if not_required_concepts_dict[n_r_c[0]] == "Yes":
                    k_c.append("conduction is the transfer of charges by contact")
                    answer = answer + "I understand that conduction will happen and the positive charges will repel each other and move away towards the metal ruler. The ruler will have a positive charge. "
                    correct = True
                else:
                    answer = answer + "I understand that the positive charges will repel each other but I am not sure how they will move."
        elif required_concepts_dict[r_c[0][1]] == "No":
            follow_up_json = read_explanation("Do positive charges attract each other?", learner_explantion)
            if follow_up_json["verifications"][0]['verification_answer'] == "Yes":
                k_c.append("positive charges attract each other")
                if required_concepts_dict[r_c[0][2]] == "Yes":
                    k_c.append("conductors allow charges to flow freely within them")
                    answer = answer + "The positive charges will move towards each other and be concentrated in the center of the rod. The ruler will remain neutral."
                elif required_concepts_dict[r_c[0][2]] == "No":
                    k_c.append("conductors do not allow charges to flow freely within them")
                    answer = answer + "The positive charges will won't be able to move towards each other."
                    answer = answer + " The metal ruler will remain neutral."
                elif required_concepts_dict[r_c[0][2]] == "Unknown":
                    if not_required_concepts_dict[n_r_c[0]] == "Yes":
                        k_c.append("conduction is the transfer of charges by contact")
                        answer = answer + "I understand that conduction will happen and the positive charges will move towards each other and be concentrated in the center of the rod. The ruler will remain neutral."
                    else:
                        answer = answer + "I understand that the positive charges will attract each other but I am not sure how they will move."
            elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                k_c.append("positive charges will neither attract nor repel each other")
                answer = answer + "The positive charges will neither attract nor repel each other. The metal ruler will remain neutral."
             elif follow_up_json["verifications"][0]['verification_answer'] == "No":
                k_c.append("positive charges will not attract each other")
                answer = answer + "The positive charges will not attract each other but based on that, I don't know how to figure out the charge on the metal ruler."
        elif required_concepts_dict[r_c[0][1]] == "Unknown":
            answer = answer + "I understand that the charges will be conserved but I don't know if the positive charges will move. So, I think metal ruler will remain neutral."
    elif required_concepts_dict[r_c[0][0]] == "No":
        k_c.append("charges are not conserved")
        answer = answer + "I understand that the charges can be created or be destroyed so, I don't know how to figure out the charges on the metal ruler."
    elif required_concepts_dict[r_c[0][0]] == "Unknown":
        answer = answer + "I am not sure if charges can be created or be destroyed so, I don't know how to figure out the charges on the metal ruler."
        final_answer = output_answer(q, answer)
    return final_answer, correct