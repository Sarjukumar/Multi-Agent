import json
from snowflake.snowpark import Session
import ast
from configuration import ConfigurationExecutor

class Agent1RequirementsAnalyzer:
    def __init__(self):
        self.session = None
        self.config = ConfigurationExecutor()
        self.session = Session.builder.configs(self.config.get_connection_params()).create()
            

    def _construct_llm_prompt(self, requirements_document_text):
        """
        Constructs the prompt for the Snowflake Cortex LLM.
        """
        prompt = f"""Analyze the following software requirements document. Your task is to identify key functionalities, data entities, and relationships that need to be tested from a database perspective. Based on this analysis, generate a list of only 1 distinct, high-level use case or questions that describe what to test in the Snowflake database.

Focus on aspects such as data integrity, correctness of calculations, relationships between entities, and coverage of core features mentioned. Do not generate SQL queries, only natural language use cases.

Output Instructions:

Output must be a valid JSON array of strings.

Each string should be a use case or test scenario, as in the sample below.

Do not include any explanations, formatting, or text outside the JSON array.

Output must match the following format exactly (replace the sample use cases with your own based on the analysis):
[
    "Verify the accuracy of total order value calculation for each customer.",
    "Ensure that all product inventory levels are correctly updated after a sale is processed.",
    "Check for data consistency between the customers table and the orders table via customer IDs.",
    "Validate that user roles and permissions restrict access to sensitive financial data as per requirements.",
    "Test the process for new user registration and ensure all required fields are populated in the user profile table."
]
Remember: Output only a valid JSON array of strings, nothing else. Please don't include unnecessary " and \n in response and only generate 5 usecases not more

Requirements Document:
---BEGIN DOCUMENT---
{requirements_document_text}
---END DOCUMENT---

JSON List of Use Cases:"""
        return prompt

    def _call_snowflake_cortex_llm(self, prompt):

        print("\n--- Simulating Snowflake Cortex LLM Call (Agent 1) ---")

        simulated_response_content = self.session.sql("SELECT SNOWFLAKE.CORTEX.COMPLETE('mistral-large2', %s) AS response_array " % repr(prompt)).collect()
        response_array = simulated_response_content[0]['RESPONSE_ARRAY']
        
        simulated_json_response = json.dumps(response_array)

        print(f"Simulated LLM JSON Response:\n{simulated_json_response}")
        print("--- End of Simulated LLM Call ---\n")
        return simulated_json_response

    def analyze_requirements(self, requirements_document_text):
        if not requirements_document_text:
            print("Error: Requirements document text cannot be empty.")
            return None

        prompt = self._construct_llm_prompt(requirements_document_text)

        llm_response_json = self._call_snowflake_cortex_llm(prompt).strip()
        llm_response_json_cleaned = ast.literal_eval(llm_response_json)


        if not llm_response_json_cleaned:
            print("Error: No response from LLM.")
            return None

        try:
            use_cases = json.loads(llm_response_json_cleaned)
            if not isinstance(use_cases, list) or not all(isinstance(uc, str) for uc in use_cases):
                print("Error: LLM response is not a valid JSON list of strings.")
                return None
            return use_cases
        except json.JSONDecodeError as e:
            print(f"Error decoding LLM JSON response: {e}")
            print(f"LLM Response received: {llm_response_json_cleaned}")
            return None
