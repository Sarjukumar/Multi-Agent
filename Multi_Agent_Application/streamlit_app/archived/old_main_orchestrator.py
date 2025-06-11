from agent1_requirements_analyzer import Agent1RequirementsAnalyzer
from agent2_sql_generator import Agent2SQLGenerator
from agent3_sql_executor import Agent3SQLExecutor


class MainOrchestrator:
    """
    Orchestrates the workflow between Agent 1, Agent 2, and Agent 3.
    """
    def __init__(self):
        """
        Initializes the orchestrator and the agents.
        """
        print("Main Orchestrator initializing...")
        self.agent1 = Agent1RequirementsAnalyzer()
        self.agent2 = Agent2SQLGenerator()
        self.agent3 = Agent3SQLExecutor()
        print("Main Orchestrator initialized successfully.")

    def process_requirements_to_sql_results(self, requirements_document_text):
        """
        Runs the full pipeline from requirements document to SQL execution results.

        Args:
            requirements_document_text (str): The content of the requirements document.

        Returns:
            dict: A dictionary containing all intermediate and final results.
                  {
                      "high_level_use_cases": list | None,
                      "generated_sql_queries": list | None,
                      "sql_execution_results": dict | None,
                      "errors": list
                  }
        """
        results = {
            "high_level_use_cases": None,
            "generated_sql_queries": None,
            "sql_execution_results": None,
            "errors": []
        }

        print("\nOrchestrator: Starting Agent 1 - Requirements Analysis...")
        high_level_use_cases =  self.agent1.analyze_requirements(requirements_document_text)
        results["high_level_use_cases"] = high_level_use_cases
        print(f"Orchestrator: Agent 1 completed.")
        print(f"{high_level_use_cases}")

        print("\nOrchestrator: Starting Agent 2 - SQL Generation...")
        generated_sql_queries = self.agent2.generate_sql_queries(high_level_use_cases)
        if generated_sql_queries:
            results["generated_sql_queries"] = generated_sql_queries
            print(f"Orchestrator: Agent 2 completed. Generated {len(generated_sql_queries)} SQL queries.")
        else:
            error_msg = "Orchestrator: Agent 2 failed to generate SQL queries."
            print(error_msg)
            results["errors"].append(error_msg)
            # We can still proceed to show Agent 1 results even if Agent 2 fails
            return results 

        print("\nOrchestrator: Starting Agent 3 - SQL Execution...")
        sql_execution_results = self.agent3.execute_sql_queries(generated_sql_queries)
        if sql_execution_results:
            results["sql_execution_results"] = sql_execution_results
            print(f"Orchestrator: Agent 3 completed. Executed {len(sql_execution_results)} queries.")
        else:
            error_msg = "Orchestrator: Agent 3 failed to execute SQL queries or process results."
            print(error_msg)
            results["errors"].append(error_msg)
            
        return results
