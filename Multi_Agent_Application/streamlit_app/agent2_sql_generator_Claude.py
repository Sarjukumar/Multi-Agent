import requests
from configuration import ConfigurationExecutor

class Agent2SQLGenerator:
    """
    Agent 2: Takes high-level use cases, understands Snowflake database structure via a Semantic Model,
    and generates specific, executable SQL queries for testing using Snowflake Cortex Analyst (conceptual).
    Updated to reflect P&C Insurance schema and generate simple to complex queries.
    """

    def __init__(self):
        self.config = ConfigurationExecutor()
        self.api_key = self.config.get_api_key()

    def _construct_cortex_agent_api_payload(self, use_case_text):
        """
        Constructs the payload for the conceptual Snowflake Cortex Agent API call.
        """
        payload =  (
            f"Based on the provided P&C Insurance database schema, generate a specific SQL query to test the following use case: {use_case_text}. "
            "Ensure the query is valid for Snowflake. Output should only contain the SQL query, nothing else.\n\n"
            "Schema:\n"
            "# Conceptual P&C Insurance Semantic Model (YAML)\n"
            "version: 1\n"
            "semantic_model:\n"
            "  name: PC_Insurance_DB_SemanticModel\n"
            "  description: Semantic model for the Property & Casualty Insurance database.\n"
            "  tables:\n"
            "    - name: Users\n"
            "      columns:\n"
            "        - {{name: UserID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: UserName, data_type: VARCHAR}}\n"
            "        - {{name: Role, data_type: VARCHAR}}\n"
            "    - name: Customers\n"
            "      columns:\n"
            "        - {{name: CustomerID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: CustomerType, data_type: VARCHAR}}\n"
            "        - {{name: FirstName, data_type: VARCHAR}}\n"
            "        - {{name: LastName, data_type: VARCHAR}}\n"
            "        - {{name: CompanyName, data_type: VARCHAR}}\n"
            "        - {{name: DateOfBirth, data_type: DATE}}\n"
            "        - {{name: AddressLine1, data_type: VARCHAR}}\n"
            "        - {{name: City, data_type: VARCHAR}}\n"
            "        - {{name: State, data_type: VARCHAR}}\n"
            "        - {{name: ZipCode, data_type: VARCHAR}}\n"
            "        - {{name: PhoneNumber, data_type: VARCHAR}}\n"
            "        - {{name: EmailAddress, data_type: VARCHAR}}\n"
            "        - {{name: CreatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "        - {{name: LastUpdatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "    - name: Policies\n"
            "      columns:\n"
            "        - {{name: PolicyID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: CustomerID, data_type: VARCHAR, is_foreign_key: true, references: Customers.CustomerID}}\n"
            "        - {{name: PolicyType, data_type: VARCHAR}}\n"
            "        - {{name: EffectiveDate, data_type: DATE}}\n"
            "        - {{name: ExpirationDate, data_type: DATE}}\n"
            "        - {{name: Status, data_type: VARCHAR}}\n"
            "        - {{name: TotalPremium, data_type: DECIMAL}}\n"
            "        - {{name: UnderwriterID, data_type: VARCHAR, is_foreign_key: true, references: Users.UserID}}\n"
            "        - {{name: IssueDate, data_type: DATE}}\n"
            "        - {{name: CreatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "        - {{name: LastUpdatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "    - name: PolicyCoverages\n"
            "      columns:\n"
            "        - {{name: PolicyCoverageID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: PolicyID, data_type: VARCHAR, is_foreign_key: true, references: Policies.PolicyID}}\n"
            "        - {{name: CoverageType, data_type: VARCHAR}}\n"
            "        - {{name: CoverageLimit, data_type: DECIMAL}}\n"
            "        - {{name: Deductible, data_type: DECIMAL}}\n"
            "        - {{name: PremiumForCoverage, data_type: DECIMAL}}\n"
            "        - {{name: CreatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "        - {{name: LastUpdatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "    - name: InsuredAssets\n"
            "      columns:\n"
            "        - {{name: InsuredAssetID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: PolicyID, data_type: VARCHAR, is_foreign_key: true, references: Policies.PolicyID}}\n"
            "        - {{name: AssetType, data_type: VARCHAR}}\n"
            "        - {{name: Description, data_type: VARCHAR}}\n"
            "        - {{name: InsuredValue, data_type: DECIMAL}}\n"
            "        - {{name: CreatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "        - {{name: LastUpdatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "    - name: PolicyTransactions\n"
            "      columns:\n"
            "        - {{name: PolicyTransactionID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: PolicyID, data_type: VARCHAR, is_foreign_key: true, references: Policies.PolicyID}}\n"
            "        - {{name: TransactionType, data_type: VARCHAR}}\n"
            "        - {{name: TransactionDate, data_type: DATE}}\n"
            "        - {{name: EffectiveDate, data_type: DATE}}\n"
            "        - {{name: PremiumChangeAmount, data_type: DECIMAL}}\n"
            "        - {{name: CreatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "    - name: BillingSchedules\n"
            "      columns:\n"
            "        - {{name: BillingScheduleID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: PolicyID, data_type: VARCHAR, is_foreign_key: true, references: Policies.PolicyID}}\n"
            "        - {{name: DueDate, data_type: DATE}}\n"
            "        - {{name: AmountDue, data_type: DECIMAL}}\n"
            "        - {{name: Status, data_type: VARCHAR}}\n"
            "        - {{name: CreatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "        - {{name: LastUpdatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "    - name: Claims\n"
            "      columns:\n"
            "        - {{name: ClaimID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: PolicyID, data_type: VARCHAR, is_foreign_key: true, references: Policies.PolicyID}}\n"
            "        - {{name: InsuredAssetID, data_type: VARCHAR, is_foreign_key: true, references: InsuredAssets.InsuredAssetID}}\n"
            "        - {{name: DateOfLoss, data_type: TIMESTAMP_NTZ}}\n"
            "        - {{name: DateReported, data_type: TIMESTAMP_NTZ}}\n"
            "        - {{name: CauseOfLoss, data_type: VARCHAR}}\n"
            "        - {{name: LossDescription, data_type: VARCHAR}}\n"
            "        - {{name: Status, data_type: VARCHAR}}\n"
            "        - {{name: AssignedAdjusterID, data_type: VARCHAR, is_foreign_key: true, references: Users.UserID}}\n"
            "        - {{name: CreatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "        - {{name: LastUpdatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "    - name: Claimants\n"
            "      columns:\n"
            "        - {{name: ClaimantID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: ClaimID, data_type: VARCHAR, is_foreign_key: true, references: Claims.ClaimID}}\n"
            "        - {{name: CustomerID, data_type: VARCHAR, is_foreign_key: true, references: Customers.CustomerID}}\n"
            "        - {{name: ClaimantType, data_type: VARCHAR}}\n"
            "        - {{name: CreatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "        - {{name: LastUpdatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "    - name: ClaimCoverages\n"
            "      columns:\n"
            "        - {{name: ClaimCoverageID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: ClaimID, data_type: VARCHAR, is_foreign_key: true, references: Claims.ClaimID}}\n"
            "        - {{name: PolicyCoverageID, data_type: VARCHAR, is_foreign_key: true, references: PolicyCoverages.PolicyCoverageID}}\n"
            "        - {{name: Status, data_type: VARCHAR}}\n"
            "        - {{name: CreatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "    - name: ClaimReserves\n"
            "      columns:\n"
            "        - {{name: ClaimReserveID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: ClaimID, data_type: VARCHAR, is_foreign_key: true, references: Claims.ClaimID}}\n"
            "        - {{name: PolicyCoverageID, data_type: VARCHAR, is_foreign_key: true, references: PolicyCoverages.PolicyCoverageID}}\n"
            "        - {{name: ReserveType, data_type: VARCHAR}}\n"
            "        - {{name: CurrentReserveAmount, data_type: DECIMAL}}\n"
            "        - {{name: CreatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "        - {{name: LastUpdatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "    - name: ClaimPayments\n"
            "      columns:\n"
            "        - {{name: ClaimPaymentID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: ClaimID, data_type: VARCHAR, is_foreign_key: true, references: Claims.ClaimID}}\n"
            "        - {{name: PolicyCoverageID, data_type: VARCHAR, is_foreign_key: true, references: PolicyCoverages.PolicyCoverageID}}\n"
            "        - {{name: ClaimantID, data_type: VARCHAR, is_foreign_key: true, references: Claimants.ClaimantID}}\n"
            "        - {{name: PaymentAmount, data_type: DECIMAL}}\n"
            "        - {{name: PaymentDate, data_type: DATE}}\n"
            "        - {{name: CreatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "    - name: ClaimSubrogations\n"
            "      columns:\n"
            "        - {{name: SubrogationID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: ClaimID, data_type: VARCHAR, is_foreign_key: true, references: Claims.ClaimID}}\n"
            "        - {{name: AmountRecovered, data_type: DECIMAL}}\n"
            "        - {{name: Status, data_type: VARCHAR}}\n"
            "        - {{name: CreatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "        - {{name: LastUpdatedDate, data_type: TIMESTAMP_NTZ}}\n"
            "    - name: ClaimNotes\n"
            "      columns:\n"
            "        - {{name: ClaimNoteID, data_type: VARCHAR, is_primary_key: true}}\n"
            "        - {{name: ClaimID, data_type: VARCHAR, is_foreign_key: true, references: Claims.ClaimID}}\n"
            "        - {{name: NoteText, data_type: VARCHAR}}\n"
            "        - {{name: CreatedByUserID, data_type: VARCHAR, is_foreign_key: true, references: Users.UserID}}\n"
            "        - {{name: CreatedDate, data_type: TIMESTAMP_NTZ}}"
        )
        return payload


    def _call_cortex_agent_api(self, payload):
        url = "https://api.anthropic.com/v1/messages"
        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }
        data = {
            "model": "claude-opus-4-20250514",
            "max_tokens": 1024,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": payload
                        }
                    ]
                }
            ]
        }
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()

        simulated_sql_query =result['content'][0]['text']
        simulated_sql_query = simulated_sql_query.replace("```sql", "")
        simulated_sql_query = simulated_sql_query.replace("`", "")

        simulated_sql_query = simulated_sql_query.strip()

        #print(f"Simulated SQL Query from Cortex Analyst (via Agent) for P&C:\n{simulated_sql_query}")
        print("--- End of Simulated Cortex Agent API Call ---\n")
        return simulated_sql_query

    def generate_sql_queries(self, high_level_use_cases):
        """
        Generates specific SQL queries from high-level use cases for P&C Insurance.
        """
        if not high_level_use_cases or not isinstance(high_level_use_cases, list):
            print("Error: No high-level use cases provided or format is incorrect.")
            return None

        sql_queries = []
        for use_case in high_level_use_cases:
            if not isinstance(use_case, str) or not use_case.strip():
                print(f"Warning: Skipping invalid use case: {use_case}")
                continue
            
            payload = self._construct_cortex_agent_api_payload(use_case)
            sql_query = self._call_cortex_agent_api(payload)
            
            if sql_query and "Placeholder: No specific P&C SQL generated" not in sql_query:
                # Avoid adding exact duplicates if the simulation logic produces them for similar use cases
                if sql_query not in sql_queries:
                    sql_queries.append(sql_query)
            else:
                print(f"Warning: Could not generate a specific SQL query for use case: {use_case}")

        return sql_queries # Return at most 10 as per original high-level plan