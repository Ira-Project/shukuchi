reader_assistant_name = "Reader"
reader_assistant_model = "gpt-4o"
reader_instructions = "You take the role of a reader. I need you to read an explanation while following my instructions. Your response should be in a json format with the following field: \n1) Definitions: an array of definitions/concepts present in the explanation."
reader_prompt_pre = "Help me identify the definitions (or concepts) in the given explanation. You don't need to correct the definitions. \nExplanation: "

thinker_assistant_name = "Thinker"
thinker_assistant_model = "gpt-4o"
thinker_instructions = "You take the role of a thinker. I need you to help me gradually ponder over a question while following my instructions. You response should be in a json format with the following fields: \n1) Conditions: An array of conditions \n2) Objective: The objective of the question"
thinker_question_prompt_pre = "Help me analyze the conditions and the objective of a question. You don't need to provide me with a solution for the time being. \nQuestion: "
thinker_new_condition_prompt_pre = "Derive the most direct condition with logical relationships, based on some known conditions. You can NOT use the conditions that are not directly shown in the known conditions. Derive only one condition. \nKnown conditions: "
thinker_new_condition_prompt_post = " \nObjective: "

read_explanation_model = "gpt-4o"
read_explanation_instructions = "You take the role of a thinker. I need you to carefully think over an explanation and verify some information for me. Your response should be a valid jsonlist called 'verifications' where each json object has 'verification_question' and 'verification_answer' attributes. The verification_answer can only be 'Yes', 'No', or 'Unknown'. The verification_questions are given as follows:\n"
read_explanation_prompt_pre = "Help me answer the verification_questions based on the given explanation. \nExplanation: "

output_answer_model = "gpt-4o"
output_answer_instructions = "You are a paraphraser. I need you to read a question and it's solution and reword and rephrase that solution. Your response should be a json object which has 'solution', and 'answer' attributes. The 'solution' will be a reworded and rephrased version of the given solution. The 'answer' will be short and concise verion of the solution that directly addresses the given question."
output_answer_prompt_pre = "Help me paraphrase the solution to the given question. \nQuestion: "
output_answer_prompt_post = "\nSolution: "

explanation_sample = "There is no difference between conductors and insulators. Negative charges have no effect on one another."