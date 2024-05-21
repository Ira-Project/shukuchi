# from sympy import *
import pickle
import json

import test_files.basic_probability.q1
import test_files.basic_probability.q2
import test_files.basic_probability.q3
import test_files.basic_probability.q4
from env import OPENAI_KEY
from time import sleep
from openai import OpenAI
from parameters import *
from test_files import *

class Node:
    def __init__(self, concept_id, concept_uuid, concept_question, concept, similar_concepts, concept_formula, calc_required,
                 concept_rephrases):
        self.concept_id = concept_id
        self.concept_uuid = concept_uuid
        self.concept_question = concept_question
        self.concept = concept
        self.similar_concepts = similar_concepts
        self.concept_rephrases = concept_rephrases
        if concept_formula == "":
            self.concept_formula = None
        else:
            self.concept_formula = concept_formula
        self.calc_required = calc_required

    def __eq__(self, other):
        if self.concept_uuid in other.similar_concepts:
            return True
        if other.concept_uuid in self.similar_concepts:
            return True
        return False

class Edge:
    def __init__(self, startNode_id, endNode_id):
        if startNode_id == endNode_id:
            print("Edge cannot have same start and end nodes")
        else:
            self.startNode = startNode_id
            self.endNode = endNode_id

    def __eq__(self, other):
        if self.startNode == other.startNode and self.endNode == other.endNode:
            return True
        return False

    def __hash__(self):
        return hash((self.startNode, self.endNode))

class Graph():
    def __init__(self, client=None):
        self.openai_client = client
        self.nodesDict = {}
        self.adjacencyDict = {}
        self.nodeParents = {}

    def addNode(self, concept_id, concept_uuid, concept_question, concept, similar_concepts, concept_formula, calc_required,
                concept_rephrases=""):
        node = Node(concept_id, concept_uuid, concept_question, concept, similar_concepts, concept_formula, calc_required, concept_rephrases)
        # Add node to nodes dictionary
        if concept_id not in self.nodesDict:
            self.nodesDict[concept_id] = node


    def addEdge(self, concept_id1, concept_id2):
        edge = Edge(concept_id1, concept_id2)

        # Add to adjacency dictionary
        if edge.startNode in self.adjacencyDict:
            self.adjacencyDict[edge.startNode].add(edge.endNode)
        else:
            self.adjacencyDict[edge.startNode] = {edge.endNode}

        # Add to nodesParent dictionary
        if edge.endNode in self.nodeParents:
            self.nodeParents[edge.endNode].add(edge.startNode)
        else:
            self.nodeParents[edge.endNode] = {edge.startNode}


    def populateGraphFromJSON(self, filename):
        f = open(filename)
        json_obj = json.load(f)
        uuid_dict = {}
        for concept in json_obj["concepts"]:
            uuid_dict[concept["concept_uuid"]] = concept["concept_id"]
        for concept in json_obj["concepts"]:
            if "concept_rephrases" in concept:
                self.addNode(concept["concept_id"], concept["concept_uuid"], concept["concept_question"], concept["concept"],
                         set(concept["similar_concepts"]), concept["concept_formula"], concept["calculation_required"],
                             concept_rephrases=concept["concept_rephrases"])
            else:
                self.addNode(concept["concept_id"], concept["concept_uuid"], concept["concept_question"], concept["concept"],
                         set(concept["similar_concepts"]), concept["concept_formula"], concept["calculation_required"])
            for parent_concept_uuid in concept["parent_concepts"]:
                self.addEdge(uuid_dict[parent_concept_uuid], concept["concept_id"])


    def addNodeFromKG(self, KG, node_id):
        stack = [node_id]
        while stack:
            nextNode = stack.pop(0)
            if nextNode not in self.nodesDict:
                self.nodesDict[nextNode] = KG.nodesDict[nextNode]
            if nextNode in KG.nodeParents:
                for parent_node in KG.nodeParents[nextNode]:
                    stack.append(parent_node)
                    edge = Edge(parent_node, nextNode)
                    # Add to adjacency dictionary
                    if edge.startNode in self.adjacencyDict:
                        self.adjacencyDict[edge.startNode].add(edge.endNode)
                    else:
                        self.adjacencyDict[edge.startNode] = {edge.endNode}
                    # Add to nodesParent dictionary
                    if edge.endNode in self.nodeParents:
                        self.nodeParents[edge.endNode].add(edge.startNode)
                    else:
                        self.nodeParents[edge.endNode] = {edge.startNode}


    def populateGraphFromAdjacencyDict(self, adjacency_dict, KG):
        self.adjacencyDict = adjacency_dict
        for parent_node in adjacency_dict:
            if parent_node not in self.nodesDict:
                self.nodesDict[parent_node] = KG.nodesDict[parent_node]
            for child_node in adjacency_dict[parent_node]:
                if child_node not in self.nodesDict:
                    self.nodesDict[child_node] = KG.nodesDict[child_node]
                if child_node in self.nodeParents:
                    self.nodeParents[child_node].add(parent_node)
                else:
                    self.nodeParents[child_node] = {parent_node}

    def removeNodes(self, nodes):
        for node_id in nodes:
            del self.nodesDict[node_id]
            if node_id in self.adjacencyDict:
                del self.adjacencyDict[node_id]
            if node_id in self.nodeParents:
                del self.nodeParents[node_id]
            for id in self.adjacencyDict:
                if node_id in self.adjacencyDict[id]:
                    self.adjacencyDict[id].remove(node_id)
            for id in self.nodeParents:
                if node_id in self.nodeParents[id]:
                    self.nodeParents[id].remove(node_id)

    def conceptNeeded(self, assistant_id, thread_id, message):
        print(message)
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=message
        )
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id
        )
        # Polling the run until it is completed
        while (True):
            if run.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread_id
                )
                response = messages.data[0].content[0].text.value
                break
            sleep(1)
        print(response)
        if response == 'Yes':
            client.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content="Are you sure this concept is required?"
            )
            run = client.beta.threads.runs.create_and_poll(
                thread_id=thread_id,
                assistant_id=assistant_id
            )
            # Polling the run until it is completed
            while (True):
                if run.status == 'completed':
                    messages = client.beta.threads.messages.list(
                        thread_id=thread_id
                    )
                    response = messages.data[0].content[0].text.value
                    break
                sleep(1)
            print(response)
        if response == 'Yes':
            return True
        else:
            return False


    # Generate subgraph by BFSing through concepts of the overall knowledge graph, starting at the parent nodes
    def getSubKG(self, startConceptIDs, assistant_id):
        nodesVisited = set()
        stack = []
        subKG = Graph()
        thread = client.beta.threads.create()
        for id in startConceptIDs:
            stack.append(id)
        while stack:
            nextConceptID = stack.pop(0)
            if self.conceptNeeded(assistant_id, thread.id, self.nodesDict[nextConceptID].concept):
                subKG.addNodeFromKG(self, nextConceptID)
            if nextConceptID in self.adjacencyDict:
                for node in self.adjacencyDict[nextConceptID]:
                    if node not in nodesVisited:
                        stack.append(node)
                        nodesVisited.add(node)
                        # if len(self.nodeParents[node]) == 1:
                        #     stack.append(node)
                        #     nodesVisited.add(node)
                        # else:
                        #     remainingParents = self.nodeParents[node] - {nextConceptID}
                        #     all_parents_present = True
                        #     for parent_node in remainingParents:
                        #         if parent_node not in nodesVisited:
                        #             all_parents_present = False
                        #             break
                        #     if all_parents_present:
                        #         stack.append(node)
                        #         nodesVisited.add(node)
        return subKG


    # A subgraph is said to be valid if all its nodes have parent nodes as part of the subgraph.
    def getValidSubgraph(self, nodes, start_nodes):
        valid_subgraph = []
        for start_node in start_nodes:
            if start_node not in nodes:
                return valid_subgraph, nodes
        nodesVisited = set()
        stack = []
        nodes_left = nodes.copy()
        for id in start_nodes:
            stack.append(id)
        while stack:
            nextConceptID = stack.pop(0)
            if nextConceptID in nodes_left:
                valid_subgraph.append(nextConceptID)
                nodes_left.remove(nextConceptID)
                if nextConceptID in self.adjacencyDict:
                    for node in self.adjacencyDict[nextConceptID]:
                        if node not in nodesVisited:
                            if len(self.nodeParents[node]) == 1:
                                stack.append(node)
                                nodesVisited.add(node)
                            else:
                                remainingParents = self.nodeParents[node] - {nextConceptID}
                                all_parents_present = True
                                for parent_node in remainingParents:
                                    if parent_node not in valid_subgraph:
                                        all_parents_present = False
                                        break
                                if all_parents_present:
                                    stack.append(node)
                                    nodesVisited.add(node)
        return valid_subgraph, nodes_left

    def getMissingConcepts(self, nodes, start_nodes):
        nodesVisited = set()
        stack = []
        for id in start_nodes:
            stack.append(id)
        missing_nodes = []
        nodesLeft = nodes.copy()
        while stack:
            nextConceptID = stack.pop(0)
            if nextConceptID in nodes:
                nodesLeft.remove(nextConceptID)
                if not nodesLeft:
                    break
            else:
                similar_node_present = False
                for similar_concept in self.nodesDict[nextConceptID].similar_concepts:
                    if similar_concept in nodes:
                        similar_node_present = True
                if not similar_node_present:
                    missing_nodes.append(nextConceptID)
            if nextConceptID in self.adjacencyDict:
                for node in self.adjacencyDict[nextConceptID]:
                    if node not in nodesVisited:
                        stack.append(node)
                        nodesVisited.add(node)
        return missing_nodes

    def getMissingParentConcepts(self, nodes, start_nodes):
        nodesVisited = set()
        stack = []
        for id in start_nodes:
            stack.append(id)
        missing_nodes = []
        while stack:
            nextConceptID = stack.pop(0)
            if nextConceptID in nodes:
                break
            else:
                missing_nodes.append(nextConceptID)
            if nextConceptID in self.adjacencyDict:
                for node in self.adjacencyDict[nextConceptID]:
                    if node not in nodesVisited:
                        stack.append(node)
                        nodesVisited.add(node)
        return missing_nodes

    def getConceptLevels(self, nodes, start_nodes):
        nodesVisited = set()
        stack = []
        level = 0
        levels_dict = {}
        levels_dict[level] = set()
        for id in start_nodes:
            stack.append(id)
            levels_dict[level].add(id)
        while stack:
            nextConceptID = stack.pop(0)
            if nextConceptID in nodes:
                if nextConceptID in self.adjacencyDict:
                    if level == 0:
                        level = level + 1
                    else:
                        if nextConceptID not in levels_dict[level-1]:
                            level = level + 1
                    for node in self.adjacencyDict[nextConceptID]:
                        if node not in nodesVisited:
                            stack.append(node)
                            nodesVisited.add(node)
                        if node in nodes:
                            if level in levels_dict:
                                levels_dict[level].add(node)
                            else:
                                levels_dict[level] = {node}
        return levels_dict

    def getConceptQuestions(self, concept_ids):
        id_to_ind = {}
        concept_questions_dict = {}
        ind = 1
        for concept_id in concept_ids:
            similar_id_present = False
            for id in id_to_ind:
                if self.nodesDict[concept_id] == self.nodesDict[id]:
                    similar_id_present = True
                    similar_id = id
                    break
            if similar_id_present:
                id_to_ind[concept_id] = id_to_ind[similar_id]
            else:
                id_to_ind[concept_id] = ind
                ind = ind + 1
        for concept_id in id_to_ind:
            if id_to_ind[concept_id] in concept_questions_dict:
                concept_questions_dict[id_to_ind[concept_id]] = concept_questions_dict[id_to_ind[concept_id]] + " OR " \
                                                                + self.nodesDict[concept_id].concept_question
            else:
                concept_questions_dict[id_to_ind[concept_id]] = self.nodesDict[concept_id].concept_question
        missing_questions_string = ""
        for question_num in concept_questions_dict:
            missing_questions_string = missing_questions_string + str(question_num) + ") " + concept_questions_dict[question_num] + "\n"
        return missing_questions_string, id_to_ind


if __name__ == '__main__':
    client = OpenAI(
        api_key=OPENAI_KEY,
    )
    kg = Graph(client=client)
    kg.populateGraphFromJSON("test_files/basic_probability/prob_concepts.json")
    # create the assistant based on the parameters and find the knowledge graph for a question
    question = test_files.basic_probability.q4.q4["question"]
    assistant = client.beta.assistants.create(
        name=kg_assistant_name,
        instructions=kg_instructions + question,
        model=kg_assistant_model,
        temperature=1
    )
    question_kg = kg.getSubKG([1], assistant.id)
    print(question_kg.adjacencyDict)
    with open('test_files/basic_probability/q4_kg.pkl', 'wb') as f:
        pickle.dump(question_kg.adjacencyDict, f)
    client.beta.assistants.delete(assistant.id)

    # # Create specific questions for each knowledge graph for a given problem
    # question = test_files.basic_probability.q3.q3["question"]
    # with open('test_files/basic_probability/q3_kg.pkl', 'rb') as f:
    #     question_adjacency_dict = pickle.load(f)
    # question_kg = Graph()
    # question_kg.populateGraphFromAdjacencyDict(question_adjacency_dict, kg)
    # concept_questions_string, concept_id_dict = question_kg.getConceptQuestions(list(question_kg.nodesDict.keys()))
    # assistant = client.beta.assistants.create(
    #     name=specific_questions_assistant_name,
    #     instructions=specific_questions_instructions_pre + concept_questions_string + "\n" +
    #                  specific_questions_instructions_post,
    #     model=specific_questions_assistant_model,
    #     response_format={"type": "json_object"}
    # )
    # thread = client.beta.threads.create(messages=[{
    #     "role": "user",
    #     "content": question,
    # }])
    # run = client.beta.threads.runs.create_and_poll(
    #     thread_id=thread.id,
    #     assistant_id=assistant.id
    # )
    # while (True):
    #     if run.status == 'completed':
    #         messages = client.beta.threads.messages.list(thread_id=thread.id)
    #         response_message = messages.data[0].content[0].text.value
    #         break
    #     sleep(1)
    # # print(response_message)
    # try:
    #     response_json = json.loads(response_message)
    # except json.decoder.JSONDecodeError:
    #     response_message = response_message.split("```json")[1].split("```")[0]
    #     response_json = json.loads(response_message)
    # specific_questions_dict = {}
    # # print(response_json)
    # for concept_id in concept_id_dict:
    #     specific_questions_dict[concept_id] = response_json[str(concept_id_dict[concept_id])]
    # print(specific_questions_dict)
    # with open('test_files/basic_probability/q3_specific_questions.pkl', 'wb') as f:
    #     pickle.dump(specific_questions_dict, f)
    # client.beta.assistants.delete(assistant.id)
    # kk


