import sys
sys.path.append("/Users/likhitnayak/Ira Project/shukuchi")
from env import OPENAI_KEY
from openai import OpenAI
from experiment5.parameters import *
import json

client = OpenAI(
    api_key=OPENAI_KEY,
)

# Put LaTeX text within delimeters
latex_delimeter = "$!$"
def insert_latex(str):
    return latex_delimeter + str + latex_delimeter

def read_explanation(concept_questions, explanation, instructions_post=""):
    response = client.chat.completions.create(
        model=read_explanation_model,
        messages=[
            {"role": "system", "content": read_explanation_instructions + concept_questions + intstructions_post},
            {"role": "user", "content": read_explanation_prompt_pre + explanation},
        ],
        response_format={"type": "json_object"},
        temperature=0.5
    )
    response_message = json.loads(response.choices[0].message.content)
    # print(response_message)
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

def output_maths_answer(question, solution):
    response = client.chat.completions.create(
        model=output_answer_model,
        messages=[
            {"role": "system", "content": output_answer_maths_instructions},
            {"role": "user", "content": output_answer_maths_prompt_pre + question + output_answer_maths_prompt_post + solution},
        ],
        response_format={"type": "json_object"}
    )
    response_message = json.loads(response.choices[0].message.content)
    return response_message


def formula_reader(formula_question, explanation, json_instruction):
    response = client.chat.completions.create(
        model=formula_reader_model,
        messages=[
            {"role": "system", "content": formula_reader_instructions + formula_question + "\n" + json_instruction},
            {"role": "user", "content": formula_reader_prompt_pre + explanation},
        ],
        response_format={"type": "json_object"}
    )
    response_message = json.loads(response.choices[0].message.content)
    return response_message

def thinker(questions, explanation, instructions_post=""):
    response = client.chat.completions.create(
        model=thinker_model,
        messages=[
            {"role": "system", "content": thinker_instructions + questions + instructions_post},
            {"role": "user", "content": thinker_prompt_pre + explanation},
        ],
        response_format={"type": "json_object"},
        temperature=0.5
    )
    response_message = json.loads(response.choices[0].message.content)
    return response_message