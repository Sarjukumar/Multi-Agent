from snowflake.snowpark import Session
from snowflake.snowpark.exceptions import SnowparkSQLException
from configuration import ConfigurationExecutor

class Agent3SQLExecutor:
    """
    Agent 3: Executes the generated SQL queries against the Snowflake database
    and formats the results
    """

    def __init__(self):
        self.session = None
        self.config = ConfigurationExecutor()
        self.session = Session.builder.configs(self.config.get_connection_params()).create()
                

    def _execute_single_query_on_snowflake(self, sql_query):
        """
        Executes a single SQL query using Snowpark and fetches results.
        Returns results in tabular format: (headers, data_rows).
        Limits results to 10 records.
        """
        print(f"\n--- Executing SQL Query via Snowpark (Agent 3) ---")
        print(f"Executing SQL Query:\n{sql_query}")

        if not self.session:
            print("Error: Snowpark session not initialized.")
            return ["Error"], [["Session not available"]]

        try:
            df = self.session.sql(sql_query)
            headers = [field.name for field in df.schema.fields]  # Ensure headers are strings

            # Collect up to 11 rows to check for overflow
            result_rows = df.collect()[:11]
            data_rows = [list(row) for row in result_rows[:10]]  # Convert Row objects to lists

            print(f"Fetched {len(data_rows)} records (limited to 10).")
            return headers, data_rows

        except SnowparkSQLException as e:
            print(f"Snowpark SQL execution error: {e}")
            return ["Error"], [[f"SQL Error: {str(e)}"]]
        except Exception as e:
            print(f"General error during Snowpark execution: {e}")
            return ["Error"], [[f"General Error: {str(e)}"]]


    def execute_sql_queries(self, sql_queries_list):
        """
        Executes a list of SQL queries and returns their results.
        """
        if not sql_queries_list or not isinstance(sql_queries_list, list):
            print("Error: No SQL queries provided or format is incorrect.")
            return None

        all_results = {}
        for i, sql_query in enumerate(sql_queries_list):
            if not isinstance(sql_query, str) or not sql_query.strip():
                print(f"Warning: Skipping invalid SQL query at index {i}: {sql_query}")
                all_results[f"Skipped_Invalid_Query_{i}"] = {"headers": ["Error"], "data": [["Invalid SQL query string"]]}
                continue

            headers, data = self._execute_single_query_on_snowflake(sql_query)
            all_results[sql_query] = {"headers": headers, "data": data}

        return all_results
