import json
import random
import shortuuid
from env import OPENAI_KEY
import pickle
from knowledgeGraph import *
import test_files.basic_probability.q4 as q4
import test_files.basic_probability.q3 as q3
import test_files.basic_probability.q2 as q2
import test_files.basic_probability.q1 as q1
import numpy as np
from numpy.linalg import norm
from openai import OpenAI
from scipy.spatial import distance
from parameters import *
# from langchain_openai import OpenAIEmbeddings
# from langchain_openai import ChatOpenAI


client = OpenAI(
    api_key=OPENAI_KEY,
)

def generate_rephrased_concepts(json_file):
    f = open(json_file)
    json_obj = json.load(f)
    for concept in json_obj["concepts"]:
        concept_sentence = concept["concept"]
        response = client.chat.completions.create(
            model=concept_rephrase_model,
            messages=[
                {"role": "system", "content": concept_rephrase_prompt_system + concept["concept_question"] + "\nA: " + concept_sentence},
                {"role": "user", "content": concept_sentence},
            ],
            temperature=1,
            top_p=1,
            frequency_penalty=1
        )
        response_message = response.choices[0].message.content
        print(response_message)
        rephrase_array = [concept_sentence]
        for sentence in response_message.split("\""):
            rephrase = sentence.split("[")[0].split("]")[0]
            rephrase = rephrase.replace("\n", "").strip()
            if len(rephrase) == 0 or len(rephrase) == 1:
                continue
            rephrase_array.append(rephrase)
        concept["concept_rephrases"] = rephrase_array
    with open("concepts.json", "w") as j:
        json.dump(json_obj, j)

def generate_concept_uuid(json_file):
    f = open(json_file)
    json_obj = json.load(f)
    uuid_dict = {}
    for concept in json_obj["concepts"]:
        concept_id = concept["concept_id"]
        uuid_dict[concept_id] = shortuuid.ShortUUID().random(length=21)
    for concept in json_obj["concepts"]:
        concept["concept_uuid"] = uuid_dict[concept["concept_id"]]
        new_parent_concepts = []
        for concept_id in concept["parent_concepts"]:
            new_parent_concepts.append(uuid_dict[concept_id])
        new_similar_concepts = []
        for concept_id in concept["similar_concepts"]:
            new_similar_concepts.append(uuid_dict[concept_id])
        concept["parent_concepts"] = new_parent_concepts
        concept["similar_concepts"] = new_similar_concepts
    with open("concepts.json", "w") as j:
        json.dump(json_obj, j)

# Retrieve knowledge graph of a specific question
def retrieve_question_subgraph_json(filename, question, overall_json_file, output_filename):
    f = open(overall_json_file)
    json_obj = json.load(f)
    uuid_dict = {}
    for concept in json_obj["concepts"]:
        uuid_dict[concept["concept_id"]] = concept["concept_uuid"]
    question_dict = {}
    question_dict["question"] = question
    question_dict["root_ids"] = json_obj["root_ids"]
    with open(filename, 'rb') as f:
        question_adjacency_dict = pickle.load(f)
    print(question_adjacency_dict)
    question_kg = Graph()
    question_kg.populateGraphFromAdjacencyDict(question_adjacency_dict, kg)
    # Remove nodes
    question_kg.removeNodes([8])
    new_nodes = []
    for node in list(question_kg.nodesDict.keys()):
        new_nodes.append(uuid_dict[node])
    question_dict["nodes"] = new_nodes
    new_adj_dict = {}
    for key in question_kg.adjacencyDict:
        child_nodes = []
        for node in list(question_kg.adjacencyDict[key]):
            child_nodes.append(uuid_dict[node])
        new_adj_dict[uuid_dict[key]] = child_nodes
    question_dict["adjacency_dict"] = new_adj_dict
    with open(output_filename, "w") as j:
        json.dump(question_dict, j)

# Retrieve knowledge graph of a specific question
def retrieve_knowledge_subgraph_json(filename):
    f = open(filename)
    json_obj = json.load(f)
    uuid_dict = {}
    for concept in json_obj["concepts"]:
        uuid_dict[concept["concept_id"]] = concept["concept_uuid"]
    subgraph_dict = {}
    subgraph_dict["root_ids"] = json_obj["root_ids"]
    kg = Graph()
    kg.populateGraphFromJSON(filename)
    # Remove nodes
    kg.removeNodes([8])
    new_nodes = []
    for node in list(kg.nodesDict.keys()):
        new_nodes.append(uuid_dict[node])
    subgraph_dict["nodes"] = new_nodes
    new_adj_dict = {}
    for key in kg.adjacencyDict:
        child_nodes = []
        for node in list(kg.adjacencyDict[key]):
            child_nodes.append(uuid_dict[node])
        new_adj_dict[uuid_dict[key]] = child_nodes
    subgraph_dict["adjacency_dict"] = new_adj_dict
    # json_final = json.dumps(subgraph_dict)
    with open("assignment_subgraph.json", "w") as j:
        json.dump(subgraph_dict, j)



def getEmbedding(text, model='text-embedding-3-small'):
    text = text.replace("\n", " ")
    return client.embeddings.create(input=[text], model=model).data[0].embedding

def generate_concept_embeddings(graph):
    embedded_concept_dict = {}
    for concept_id in graph.nodesDict.keys():
        embedded_concept_dict[concept_id] = []
        for concept in graph.nodesDict[concept_id].concept_rephrases:
            embedded_concept = getEmbedding(concept)
            embedded_concept_dict[concept_id].append(embedded_concept)
    return embedded_concept_dict

def split_message(message, sentence_length = 2):
    message = message.replace("\n", " ").strip()
    sentence_delims = [".", "!", "?"]
    for c in message:
        if c in sentence_delims:
            message = message.replace(c, ',')
    sentences = message.split(',')
    sentences.pop()
    i = 0
    split_arr = []
    while i <= len(sentences):
        if i + sentence_length <= len(sentences):
            chunk = ".".join(sentences[i:i+sentence_length])
        else:
            chunk = ".".join(sentences[i:])
        split_arr.append(chunk)
        i = i + sentence_length
    return split_arr

def perform_calculation(string):
    if string:
        if isinstance(string, str):
            string_split = string.split("(")
            operation = string_split[0]
            if operation == "add":
                sum = 0
                for num in string_split[1].split(")")[0].split(","):
                    num = float(num.strip())
                    sum = sum + num
                return sum
            if operation == "multiply":
                prod = 1
                for num in string_split[1].split(")")[0].split(","):
                    num = float(num.strip())
                    prod = prod * num
                return prod
            if operation == "subtract":
                sub = 0
                start = True
                for num in string_split[1].split(")")[0].split(","):
                    num = float(num.strip())
                    if start:
                        sub = num
                        start = False
                    else:
                        sub = sub - num
                return sub
            if operation == "divide":
                div = 1
                start = True
                for num in string_split[1].split(")")[0].split(","):
                    num = float(num.strip())
                    if start:
                        div = num
                        start = False
                    else:
                        div = div / num
                return div
        else:
            return string
    else:
        return None

def get_concept_apply_message(string1, string2):
    return "Given that:\n" + string1 + "\n" + string2

def create_and_run_missing_concepts_assistant(explanation, concept_questions):
    assistant = client.beta.assistants.create(
        name=missing_concepts_assistant_name,
        instructions=missing_concepts_instructions_pre + concept_questions + missing_concepts_instructions_post,
        model=missing_concepts_assistant_model
    )
    thread = client.beta.threads.create(messages=[{
        "role": "user",
        "content": explanation,
    }])
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread.id,
        assistant_id=assistant.id
    )
    while (True):
        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            response = messages.data[0].content[0].text.value
            break
        sleep(1)
    client.beta.assistants.delete(assistant.id)
    return response

def create_and_run_concepts_present_assistant(explanation, check_concept_ids, overall_kg):
    answer_kg = Graph()
    assistant = client.beta.assistants.create(
        name=concept_present_assistant_name,
        instructions=concept_present_instructions,
        model=missing_concepts_assistant_model,
        response_format={"type": "json_object"},
        temperature=0.2
    )
    thread = client.beta.threads.create()
    start_thread = True
    for concept_id in check_concept_ids:
        user_message = "According to the context provided, " + \
                                       overall_kg.nodesDict[concept_id].concept_question
        if start_thread:
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content="Context:\n'" + explanation + "'\n" + user_message
            )
            start_thread = False
        else:
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=user_message
            )
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id
        )
        while (True):
            if run.status == 'completed':
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                concept_present_json = messages.data[0].content[0].text.value
                break
            sleep(1)
        concept_present_json = json.loads(concept_present_json)
        # print(user_message, concept_present_json)
        if concept_present_json["Answer Present"] == "Yes":
            answer_kg.addNode(concept_id, kg.nodesDict[concept_id].concept_uuid, kg.nodesDict[concept_id].concept_question, concept_present_json["Answer"],
                              kg.nodesDict[concept_id].similar_concepts, "", kg.nodesDict[concept_id].calc_required)
    client.beta.assistants.delete(assistant.id)
    return answer_kg

def create_and_run_concepts_apply_assistant(problem, explanation_kg, concept_nodes):
    final_message = ""
    assistant = client.beta.assistants.create(
        name=concept_apply_assistant_name,
        instructions=concept_apply_instructions_pre + problem + "\n" + concept_apply_instructions_post,
        model=concept_apply_assistant_model,
        response_format={"type": "json_object"},
        temperature=0.5,
        top_p=0.5
    )
    thread = client.beta.threads.create()
    start_thread = True
    for concept_id in concept_nodes:
        if explanation_kg.nodesDict[concept_id].calc_required == "No":
            continue
        if start_thread:
            user_message = explanation_kg.nodesDict[concept_id].concept
            start_thread = False
        else:
            user_message = random.choice(concept_apply_starting_phrase)
            user_message = user_message + explanation_kg.nodesDict[concept_id].concept
        user_message = user_message + "\n" + \
                       "Apply this explanation to the given problem and based on the explanation, state the calculation."
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=user_message
        )
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id
        )
        while (True):
            if run.status == 'completed':
                messages = client.beta.threads.messages.list(thread_id=thread.id)
                concept_apply_json = messages.data[0].content[0].text.value
                break
            sleep(1)
        concept_apply_json = json.loads(concept_apply_json)
        print(concept_apply_json)
        calculation_result = perform_calculation(concept_apply_json["Calculation"])
        final_message = final_message + concept_apply_json["Response"] + "\n" + "Calculation: " + \
                        str(calculation_result) + "\n"
    client.beta.assistants.delete(assistant.id)
    return final_message

# generate_rephrased_concepts("test_files/basic_probability/prob_concepts.json")
# generate_concept_uuid("test_files/basic_probability/prob_concepts.json")
# idsdi


kg = Graph()
kg.populateGraphFromJSON("test_files/basic_probability/prob_concepts.json")
kg_start_nodes = [1]
# embedded_concepts = generate_concept_embeddings(kg)
# # Save embeddings of concepts
# with open('test_files/basic_probability/concept_embeddings.pkl', 'wb') as f:
#     pickle.dump(embedded_concepts, f)
# jknk
# Read embedding of concepts
with open('test_files/basic_probability/concept_embeddings.pkl', 'rb') as f:
    embedded_concepts = pickle.load(f)
# print(embedded_concepts[1][0])
# ljkj

# Retrieve knowledge graph of a specific question
question = q4.q4["question"]
# retrieve_question_subgraph_json('test_files/basic_probability/q4_kg.pkl', question,
#                                 "test_files/basic_probability/prob_concepts.json", "q4_subgraph.json")
# retrieve_knowledge_subgraph_json("test_files/basic_probability/prob_concepts.json")
# jlj
with open('test_files/basic_probability/q4_kg.pkl', 'rb') as f:
    question_adjacency_dict = pickle.load(f)
question_kg = Graph()
question_kg.populateGraphFromAdjacencyDict(question_adjacency_dict, kg)

# Remove nodes of the concept graph that might be confusing or are not needed. This condenses the knowledge graph.
kg.removeNodes([8])
question_kg.removeNodes([8])
# print(question_kg.adjacencyDict)
# hjkk

for userPrompt in q3.q3["userPrompts"]:
    prompt = userPrompt["prompt"]
    prompt_len = len(prompt)
    print(prompt)
    if prompt_len <= 100:
        threshold = 0.6
    elif prompt_len > 100 and prompt_len <= 200:
        threshold = 0.55
    elif prompt_len > 200 and prompt_len <= 250:
        threshold = 0.50
    else:
        threshold = 0.45
    explanation_embedding = getEmbedding(prompt)
    explanation_dict = {}
    concept_ids_present = set()
    for concept_id in question_kg.nodesDict.keys():
        explanation_dict[concept_id] = []  # will consist of cosine similarity values and presence of concept
        max_cosine_sim = -1000
        for concept_embedding in embedded_concepts[concept_id]:
            cosine_sim = 1 - distance.cosine(concept_embedding, explanation_embedding)
            if cosine_sim > max_cosine_sim:
                max_cosine_sim = cosine_sim
        explanation_dict[concept_id].append(max_cosine_sim)
        if max_cosine_sim < threshold:
            explanation_dict[concept_id].append("No")
        else:
            explanation_dict[concept_id].append("Yes")
            concept_ids_present.add(concept_id)
    # print(explanation_dict)
    # kjlj
    # print(concept_ids_present, question_kg.nodeParents)
    response_message = "Test"
    if len(concept_ids_present) == 0:
        response_message = random.choice(no_explanation_responses)
    else:
        valid_nodes, isolated_nodes = question_kg.getValidSubgraph(concept_ids_present, kg_start_nodes)
        # print(valid_nodes, isolated_nodes, concept_ids_present)
        if len(valid_nodes) == 0:
            missing_concepts = question_kg.getMissingParentConcepts(concept_ids_present, kg_start_nodes)
            missing_concept_questions, _ = kg.getConceptQuestions(missing_concepts)
            response_message = create_and_run_missing_concepts_assistant(prompt, missing_concept_questions)
        else:
            answer_kg = create_and_run_concepts_present_assistant(prompt, concept_ids_present, kg)
            apply_concept_nodes, other_nodes = question_kg.getValidSubgraph(set(answer_kg.nodesDict.keys()),
                                                                              kg_start_nodes)
            if other_nodes:
                missing_concepts = question_kg.getMissingConcepts(set(answer_kg.nodesDict.keys()), kg_start_nodes)
                missing_concept_questions, _ = kg.getConceptQuestions(missing_concepts)
                missing_concept_message = create_and_run_missing_concepts_assistant(prompt, missing_concept_questions)
                print("Missing Concept Message:")
                print(missing_concept_message)
            if apply_concept_nodes:
                apply_concepts_message = create_and_run_concepts_apply_assistant(question, answer_kg, apply_concept_nodes)
                print("Apply Concept Message:")
                print(apply_concepts_message)
    print(response_message)
    print("-" * 20)
    jkh
