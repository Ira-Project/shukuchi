import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from IB_Physics_DP.Work_and_Energy.parameters import *
from IB_Physics_DP.Work_and_Energy.q1 import question_json as q1
from IB_Physics_DP.Work_and_Energy.q2 import question_json as q2
from IB_Physics_DP.Work_and_Energy.q3 import question_json as q3
from IB_Physics_DP.Work_and_Energy.q4 import question_json as q4
from IB_Physics_DP.Work_and_Energy.q5 import question_json as q5
from sympy import *
import json

def get_questions_and_concepts():
    # Create a set of all concepts in the assignment
    concepts_set = set()
    for question in [q1, q2, q3, q4, q5]:
        for concept in question["required_concepts"]:
            concepts_set.add(information_questions[concept])

    # Create a json object with all the questions and concepts
    questions_json = {}
    for question in [q1, q2, q3, q4, q5]:
        questions_json[question["question_id"]] = {
            "question": question["Question"],
            "answer": question["Answer"],
            "Question_image": question["Question_image"],
        }
    print(concepts_set)
    return concepts_set, questions_json

if __name__ == "__main__":
    concepts_set, questions_json = get_questions_and_concepts()
    with open("questions.json", "w") as f:
        json.dump(questions_json, f, indent=4)
    with open("concepts.json", "w") as f:
        json.dump(list(concepts_set), f, indent=4)
