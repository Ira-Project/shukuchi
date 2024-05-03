# from sympy import *
import pickle
import json

import test_files.basic_probability.q3
from env import OPENAI_KEY
from time import sleep
from openai import OpenAI
from parameters import *
from test_files import *

class Node:
    def __init__(self, concept_id, concept_question, concept, similar_concepts, concept_formula):
        self.concept_id = concept_id
        self.concept_question = concept_question
        self.concept = concept
        self.similar_concepts = similar_concepts
        if concept_formula == "":
            self.concept_formula = None
        else:
            self.concept_formula = concept_formula

    def __eq__(self, other):
        if self.concept_id in other.similar_concepts:
            return True
        if other.concept_id in self.similar_concepts:
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

    def addNode(self, concept_id, concept_question, concept, similar_concepts, concept_formula):
        node = Node(concept_id, concept_question, concept, similar_concepts, concept_formula)
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
        for concept in json_obj:
            self.addNode(concept["concept_id"], concept["concept_question"], concept["concept"],
                         set(concept["similar_concepts"]), concept["concept_formula"])
            for parent_concept_id in concept["parent_concepts"]:
                self.addEdge(parent_concept_id, concept["concept_id"])


    def addNodeFromKG(self, KG, node_id):
        stack = [node_id]
        while stack:
            nextNode = stack.pop(0)
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

    def conceptNeeded(self, assistant_id, message):
        print(message)
        thread = self.openai_client.beta.threads.create(messages=[{
            "role": "user",
            "content": message,
        }])
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id
        )
        # Polling the run until it is completed
        while (True):
            if run.status == 'completed':
                messages = client.beta.threads.messages.list(
                    thread_id=thread.id
                )
                response = messages.data[0].content[0].text.value
                break
            sleep(1)
        print(response)
        if response == 'Yes':
            return True
        else:
            return False


    # BFS through the concepts starting at startConceptID
    def getSubKG(self, startConceptIDs, assistant_id):
        nodesVisited = set()
        stack = []
        subKG = Graph()
        for id in startConceptIDs:
            stack.append(id)
        while stack:
            nextConceptID = stack.pop(0)
            if self.conceptNeeded(assistant_id, self.nodesDict[nextConceptID].concept):
                subKG.addNodeFromKG(self, nextConceptID)
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
                                if parent_node not in nodesVisited:
                                    all_parents_present = False
                                    break
                            if all_parents_present:
                                stack.append(node)
                                nodesVisited.add(node)
        return subKG

if __name__ == '__main__':
    client = OpenAI(
        api_key=OPENAI_KEY,
    )
    kg = Graph(client=client)
    kg.populateGraphFromJSON("test_files/basic_probability/prob_concepts.json")
    # create the assistant based on the parameters
    question = test_files.basic_probability.q3.q3["question"]
    assistant = client.beta.assistants.create(
        name=kg_assistant_name,
        instructions=kg_instructions + question,
        model=kg_assistant_model,
        file_ids=[]
    )
    question_kg = kg.getSubKG([1], assistant.id)
    print(question_kg.adjacencyDict)
    with open('test_files/basic_probability/q3_kg.pkl', 'wb') as f:
        pickle.dump(question_kg.adjacencyDict, f)
    client.beta.assistants.delete(assistant.id)


