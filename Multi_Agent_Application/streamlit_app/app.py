import streamlit as st
import pandas as pd
from agent1_requirements_analyzer import Agent1RequirementsAnalyzer
from agent2_sql_generator import Agent2SQLGenerator
from agent3_sql_executor import Agent3SQLExecutor
from PIL import Image

# Correct image path
icon_path = "streamlit_app/173995_minion_reading_icon.png"
icon_image = Image.open(icon_path)

# --- Page Configuration ---
st.set_page_config(
    page_title="Snowflake SQL Test Case Generator",
    page_icon="❄️",
    layout="wide",
    initial_sidebar_state="expanded"
)




# --- Custom CSS for Enhanced Styling ---
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main theme variables */
    :root {
        --primary-color: #0066CC;
        --secondary-color: #4A90E2;
        --success-color: #00C851;
        --warning-color: #FF8800;
        --error-color: #FF4444;
        --background-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --card-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        --glass-bg: rgba(255, 255, 255, 0.25);
        --border-radius: 16px;
    }
    
    /* Main app styling */
    .main > div {
        padding-top: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    /* Header styling */
    .main-header {
        background: var(--background-gradient);
        padding: 2rem;
        border-radius: var(--border-radius);
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: var(--card-shadow);
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    /* Card styling */
    .card {
        background: var(--glass-bg);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: var(--card-shadow);
    }
    
    /* Agent progress cards */
    .agent-card {
        background: linear-gradient(145deg, #f0f4f8, #ffffff);
        border-left: 4px solid var(--primary-color);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    .agent-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .agent-header {
        display: flex;
        align-items: center;
        margin-bottom: 1rem;
    }
    
    .agent-icon {
        font-size: 2rem;
        margin-right: 1rem;
    }
    
    .agent-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0;
    }
    
    .agent-status {
        margin-left: auto;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 500;
    }
    
    .status-pending {
        background-color: #f39c12;
        color: white;
    }
    
    .status-running {
        background-color: var(--secondary-color);
        color: white;
        animation: pulse 2s infinite;
    }
    
    .status-complete {
        background-color: var(--success-color);
        color: white;
    }
    
    .status-error {
        background-color: var(--error-color);
        color: white;
    }
    
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    /* Progress bar */
    .progress-container {
        background-color: #e9ecef;
        border-radius: 10px;
        height: 8px;
        margin: 1rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 10px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        transition: width 0.5s ease;
    }
    
    /* SQL Code styling */
    .sql-container {
        background: #2d3748;
        border-radius: var(--border-radius);
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid var(--success-color);
    }
    
    /* Instructions card */
    .instructions {
        background: linear-gradient(135deg, #667eea22, #764ba222);
        border: 1px solid rgba(102, 126, 234, 0.3);
        border-radius: var(--border-radius);
        padding: 1.5rem;
        margin: 1rem 0;
    }
    
    /* File upload area */
    .upload-area {
        border: 2px dashed var(--primary-color);
        border-radius: var(--border-radius);
        padding: 2rem;
        text-align: center;
        background: rgba(0, 102, 204, 0.05);
        transition: all 0.3s ease;
    }
    
    .upload-area:hover {
        background: rgba(0, 102, 204, 0.1);
        border-color: var(--secondary-color);
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        border-radius: var(--border-radius);
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-top: 3px solid var(--primary-color);
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-color);
        margin: 0;
    }
    
    .metric-label {
        color: #6c757d;
        font-size: 0.9rem;
        margin: 0;
    }
    
    /* Button styling */
    .stButton button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: var(--border-radius);
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 102, 204, 0.3);
    }
    
    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 102, 204, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa, #e9ecef);
    }
    
    /* Table styling */
    .dataframe {
        border-radius: var(--border-radius);
        overflow: hidden;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def flatten_cell(cell):
    """Flattens a cell if it's a list or dict, otherwise returns as is."""
    if isinstance(cell, dict):
        return ', '.join(f"{k}: {v}" for k, v in cell.items())
    elif isinstance(cell, list):
        return ', '.join(str(item) for item in cell)
    else:
        return cell

def get_agent_info():
    """Returns information about each agent for display"""
    return {
        1: {
            "name": "Requirements Analyzer",
            "icon": "🔍",
            "description": "Analyzing requirements and generating high-level use cases",
            "color": "#3498db"
        },
        2: {
            "name": "SQL Generator",
            "icon": "⚡",
            "description": "Converting use cases into SQL test queries",
            "color": "#e74c3c"
        },
        3: {
            "name": "Query Executor",
            "icon": "🚀",
            "description": "Executing SQL queries and gathering results",
            "color": "#2ecc71"
        }
    }

def display_agent_progress(agent_num, status, result=None):
    """Display individual agent progress with enhanced styling"""
    agent_info = get_agent_info()[agent_num]
    
    status_class = f"status-{status.lower()}"
    status_text = {
        "PENDING": "⏳ Pending",
        "RUNNING": "🔄 Running",
        "COMPLETE": "✅ Complete",
        "ERROR": "❌ Error"
    }.get(status, status)
    
    st.markdown(f"""
    <div class="agent-card">
        <div class="agent-header">
            <span class="agent-icon">{agent_info['icon']}</span>
            <div>
                <h3 class="agent-title">Agent {agent_num}: {agent_info['name']}</h3>
                <p style="margin: 0; color: #7f8c8d; font-size: 0.9rem;">{agent_info['description']}</p>
            </div>
            <span class="agent-status {status_class}">{status_text}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if result and status == "COMPLETE":
        if agent_num == 1 and result.get("high_level_use_cases"):
            st.markdown("**📋 Generated Use Cases:**")
            for i, uc in enumerate(result["high_level_use_cases"], 1):
                st.markdown(f"**{i}.** {uc}")
                
        elif agent_num == 2 and result.get("generated_sql_queries"):
            st.markdown("**🗄️ Generated SQL Queries:**")
            for i, sql in enumerate(result["generated_sql_queries"], 1):
                st.markdown(f"**Query {i}:**")
                st.code(sql, language="sql")
                
        elif agent_num == 3 and result.get("sql_execution_results"):
            st.markdown("**📊 Execution Results (Max 10 rows per query):**")
            for query, result_data in result["sql_execution_results"].items():
                st.markdown(f"**Results for Query:**")
                st.code(query, language="sql")
                
                if result_data.get("headers") and result_data.get("data") is not None:
                    if result_data["headers"][0] == "Error":
                        st.error(f"Error executing query: {result_data['data'][0][0]}")
                    else:
                        flattened_data = [
                            [flatten_cell(cell) for cell in row]
                            for row in result_data["data"]
                        ]
                        df = pd.DataFrame(flattened_data, columns=result_data["headers"])
                        st.dataframe(df, use_container_width=True)
                else:
                    st.info("No data returned for this query.")

def display_progress_bar(current_step, total_steps):
    """Display overall progress bar"""
    progress = (current_step / total_steps) * 100
    st.markdown(f"""
    <div class="progress-container">
        <div class="progress-bar" style="width: {progress}%"></div>
    </div>
    <p style="text-align: center; margin: 0.5rem 0; color: #6c757d;">
        Overall Progress: {current_step}/{total_steps} ({progress:.0f}%)
    </p>
    """, unsafe_allow_html=True)

def display_metrics(results):
    """Display summary metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    use_cases_count = len(results.get("high_level_use_cases", []))
    queries_count = len(results.get("generated_sql_queries", []))
    executed_count = len(results.get("sql_execution_results", {}))
    error_count = len(results.get("errors", []))
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">🔍 {use_cases_count}</p>
            <p class="metric-label">Use Cases</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">⚡ {queries_count}</p>
            <p class="metric-label">SQL Queries</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">🚀 {executed_count}</p>
            <p class="metric-label">Executed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <p class="metric-value">❌ {error_count}</p>
            <p class="metric-label">Errors</p>
        </div>
        """, unsafe_allow_html=True)

# --- Main Application UI ---
col1, col2 = st.columns([1,10])

with col1:
    st.image(icon_image,use_container_width=True)   
     
with col2:
    st.markdown("""
    <div class="main-header"> 
        <h1>❄️  SQL Test Case Generator ❄️</h1>
        <p>AI-Powered Multi-Agent System for P&C Insurance Test Case Generation</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="instructions">
    <h3>🎯 How It Works</h3>
    <p><strong>This application uses a sophisticated multi-agent system to transform your requirements into executable SQL test cases:</strong></p>
    <ol>
        <li><strong>📁 Upload</strong> your requirements document (plain text .txt file)</li>
        <li><strong>🔍 Agent 1</strong> analyzes requirements and generates high-level use cases</li>
        <li><strong>⚡ Agent 2</strong> converts use cases into SQL test queries</li>
        <li><strong>🚀 Agent 3</strong> executes queries and gathers results</li>
        <li><strong>📊 Review</strong> the complete analysis and generated test cases</li>
    </ol>
</div>
""", unsafe_allow_html=True)


# File Upload Section
st.markdown("## 📁 Upload Requirements Document")
st.markdown('<div class="upload-area">', unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a .txt file with your requirements", 
    type="txt",
    help="Upload a plain text file containing your requirements"
)

requirements_text = ""
if uploaded_file is not None:
    try:
        requirements_text = uploaded_file.read().decode("utf-8")
        st.success(f"✅ File uploaded successfully! ({len(requirements_text)} characters)")
        
        with st.expander("📋 Preview Requirements Document", expanded=False):
            st.text_area("Requirements Content", requirements_text, height=200, disabled=True)
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        requirements_text = ""

st.markdown('</div>', unsafe_allow_html=True)

# Processing Section
st.markdown("## 🚀 Process and Generate Results")

if st.button("🔥 Start Processing", type="primary", use_container_width=True):
    if not requirements_text or len(requirements_text.strip()) == 0:
        st.warning("⚠️ Please upload a requirements document first.")
    elif len(requirements_text.strip()) < 10:
        st.warning("⚠️ Requirements document seems too short. Please provide more detailed requirements.")
    else:
        # Initialize session state for real-time updates
        if "processing_status" not in st.session_state:
            st.session_state.processing_status = {}
        
        # Create placeholders for real-time updates
        progress_placeholder = st.empty()
        agent1_placeholder = st.empty()
        agent2_placeholder = st.empty()
        agent3_placeholder = st.empty()
        
        try:
            with st.spinner("🔄 Initializing agents..."):
                # Validate requirements text before processing
                requirements_text_clean = requirements_text.strip()
                if not requirements_text_clean:
                    st.error("❌ Requirements text is empty after cleaning.")
                    st.stop()
                
                st.success("✅ Agents initialized successfully!")
                
                # Initialize agent statuses
                for i in range(1, 4):
                    st.session_state.processing_status[f"agent_{i}"] = "PENDING"
                
                # Display initial progress
                with progress_placeholder.container():
                    display_progress_bar(0, 3)
                
                with agent1_placeholder.container():
                    display_agent_progress(1, "PENDING")
                with agent2_placeholder.container():
                    display_agent_progress(2, "PENDING")
                with agent3_placeholder.container():
                    display_agent_progress(3, "PENDING")
                
                # Process each agent with real-time updates
                results = {"errors": []}
                
                # Agent 1: Requirements Analysis
                with agent1_placeholder.container():
                    display_agent_progress(1, "RUNNING")
                with progress_placeholder.container():
                    display_progress_bar(0, 3)
                
                try:
                    # Step 1: Generate high-level use cases
                    st.info("🔍 Agent 1: Analyzing requirements...")
                    agent1 = Agent1RequirementsAnalyzer()
                    use_cases = agent1.analyze_requirements(requirements_text_clean)
                    results["high_level_use_cases"] = use_cases
                    
                    if use_cases:
                        with agent1_placeholder.container():
                            display_agent_progress(1, "COMPLETE", {"high_level_use_cases": use_cases})
                        
                        with progress_placeholder.container():
                            display_progress_bar(1, 3)
                        
                        # Agent 2: SQL Generation
                        with agent2_placeholder.container():
                            display_agent_progress(2, "RUNNING")
                        
                        st.info("⚡ Agent 2: Generating SQL queries...")
                        
                        # If we already have the full result, use it; otherwise generate SQL
                        agent2 = Agent2SQLGenerator()
                        sql_queries = agent2.generate_sql_queries(use_cases)
                        results["generated_sql_queries"] = sql_queries 
                        
                        if sql_queries:
                            with agent2_placeholder.container():
                                display_agent_progress(2, "COMPLETE", {"generated_sql_queries": sql_queries})
                            
                            with progress_placeholder.container():
                                display_progress_bar(2, 3)
                            
                            # Agent 3: Execution
                            with agent3_placeholder.container():
                                display_agent_progress(3, "RUNNING")
                            
                            st.info("🚀 Agent 3: Executing SQL queries...")
                            agent3 = Agent3SQLExecutor()
                            execution_results = agent3.execute_sql_queries(sql_queries)
                            results["sql_execution_results"] = execution_results
                            
                            if execution_results:
                                with agent3_placeholder.container():
                                    display_agent_progress(3, "COMPLETE", {"sql_execution_results": execution_results})
                                
                                with progress_placeholder.container():
                                    display_progress_bar(3, 3)
                            else:
                                with agent3_placeholder.container():
                                    display_agent_progress(3, "ERROR")
                                st.warning("⚠️ Agent 3: No execution results generated")
                        else:
                            with agent2_placeholder.container():
                                display_agent_progress(2, "ERROR")
                            st.warning("⚠️ Agent 2: No SQL queries generated")
                    else:
                        with agent1_placeholder.container():
                            display_agent_progress(1, "ERROR")
                        st.warning("⚠️ Agent 1: No use cases generated")
                        
                except Exception as agent_error:
                    st.error(f"❌ Error in agent processing: {str(agent_error)}")
                    # Try fallback approach
                    st.info("🔄 Attempting fallback processing...")
                    try: 
                        # Update displays based on what we got
                        if results.get("high_level_use_cases"):
                            with agent1_placeholder.container():
                                display_agent_progress(1, "COMPLETE", results)
                        
                        if results.get("generated_sql_queries"):
                            with agent2_placeholder.container():
                                display_agent_progress(2, "COMPLETE", results)
                        
                        if results.get("sql_execution_results"):
                            with agent3_placeholder.container():
                                display_agent_progress(3, "COMPLETE", results)
                            with progress_placeholder.container():
                                display_progress_bar(3, 3)
                    except Exception as fallback_error:
                        st.error(f"❌ Fallback processing also failed: {str(fallback_error)}")
                        results = {"errors": [f"Processing Error: {str(fallback_error)}"]}
                        
                        # Show error status for all agents
                        with agent1_placeholder.container():
                            display_agent_progress(1, "ERROR")
                        with agent2_placeholder.container():
                            display_agent_progress(2, "ERROR")
                        with agent3_placeholder.container():
                            display_agent_progress(3, "ERROR")
                
                st.session_state.results = results
                
                # Show completion message
                st.balloons()
                st.success("🎉 Processing completed successfully!")
                
        except Exception as e:
            st.error(f"❌ An error occurred during processing: {e}")
            st.session_state.results = {"errors": [f"Orchestration Error: {str(e)}"]}

# Display final results if available
if "results" in st.session_state and st.session_state.results:
    st.markdown("## 📊 Final Results Summary")
    display_metrics(st.session_state.results)
    
    if st.session_state.results.get("errors"):
        st.error("⚠️ Errors encountered during processing:")
        for error in st.session_state.results["errors"]:
            st.write(f"• {error}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #7f8c8d;">
    <p><strong>🏢 Multi-Agent System for P&C Insurance Test Case Generation</strong></p>
    <p>Powered by  AI • Built with ❤️ using Streamlit</p>
</div>
""", unsafe_allow_html=True)
