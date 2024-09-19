import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from IB_Physics_DP.Work_and_Energy.parameters import *
from IB_Physics_DP.Work_and_Energy.q1 import question_json as q1
from IB_Physics_DP.Work_and_Energy.q2 import question_json as q2
from IB_Physics_DP.Work_and_Energy.q3 import question_json as q3
from IB_Physics_DP.Work_and_Energy.q4 import question_json as q4
from IB_Physics_DP.Work_and_Energy.q5 import question_json as q5
from sympy import *

def get_questions_and_concepts():
    # Create a set of all concepts in the assignment
    assignment_concepts = set()
    for question in [q1, q2, q3, q4, q5]:
        for concept in question["required_concepts"]:
            assignment_concepts.add(concept)

    # Create a json object with all the questions and concepts
    questions_and_concepts_json = {}
    for question in [q1, q2, q3, q4, q5]:
        questions_and_concepts_json[question["question_id"]] = {
            "question": question["Question"],
            "concepts": question["required_concepts"],
            "answer": question["Answer"],
            "Question_image": question["Question_image"],
        }

    return assignment_concepts, questions_and_concepts_json
