class ConfigurationExecutor:    
    def get_connection_params(self):
        return {
                    "user": "",
                    "account": "",
                    "password": "",
                    "role": "sysadmin",
                    "warehouse": "admin_wh_xsmall",
                    "database": "streamlit_apps",
                    "schema": "llm_apps_sch"
        }
    
    def get_api_key(self):
        return ""