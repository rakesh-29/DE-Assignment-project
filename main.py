import autogen
import os
import sys
import json
import time
from typing import Dict, List, Tuple, Optional, Union
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Configuration for Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# Using OpenAI's API instead if available
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    llm_config = {
        "config_list": [
            {
                "model": "gpt-4",  # Or another available OpenAI model
                "api_key": OPENAI_API_KEY
            }
        ],
        "temperature": 0.2
    }
else:
   llm_config = {
    "config_list": [
        {
            "model": "llama3-70b-8192",  # Using Llama 3 70B through Groq
            "api_key": GROQ_API_KEY,
            "base_url": "https://api.groq.com/openai/v1",
            "price": [0.0001, 0.0001]  # Add custom pricing to avoid the warning
                                       # [prompt_price_per_1k, completion_token_price_per_1k]
            
        }
    ],
    "temperature": 0.2,  # Low temperature for more deterministic outputs
    "timeout": 120,
    "cache_seed": None  # No caching for fresh results
}

# ANSI color codes for console output
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


# Utility functions
def print_step(agent_name: str, message: str):
    """Print a step with agent name highlighted."""
    print(f"{Colors.HEADER}[{agent_name}]{Colors.ENDC} {message}")

def save_to_file(content: str, filename: str):
    """Save content to a file."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as f:
        f.write(content)
    print(f"{Colors.GREEN}File saved:{Colors.ENDC} {filename}")

# Agent System Class
class MultiAgentCodingSystem:
    def __init__(self):
        """Initialize the multi-agent system."""
        # Create output directories
        os.makedirs("output", exist_ok=True)
        os.makedirs("output/code", exist_ok=True)
        os.makedirs("output/docs", exist_ok=True)
        os.makedirs("output/tests", exist_ok=True)

        # Initialize conversation state
        self.state = {
            "requirement": "",
            "structured_requirement": "",
            "code": "",
            "review_passed": False,
            "documentation": "",
            "tests": "",
            "ui_code": "",
        }
        
        # Initialize the agent system
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all AutoGen agents with their specific configurations."""
        # User Proxy Agent - represents the human user
        self.user_proxy = autogen.UserProxyAgent(
            name="User",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=0,
            system_message="You are a user who needs a software solution. You provide requirements and review the final outputs.",
            code_execution_config={"use_docker": False},
        )
        
        # Requirement Analysis Agent
        system_message = """You are a requirement analysis expert. 
        Your job is to:
        1. Take natural language requirements
        2. Structure them into clear, detailed software requirements
        3. Identify any ambiguities or missing details and resolve them
        4. Organize requirements into functional, non-functional, and technical categories
        5. Output a JSON format with the structured requirements

        Your response should be clear, thorough, and actionable for the coding team.
        """
        self.req_analysis_agent = autogen.AssistantAgent(
            name="RequirementAnalyst",
            system_message=system_message,
            llm_config=llm_config
        )
        
        # Coding Agent
        system_message = """You are an expert Python developer.
        Your job is to:
        1. Take structured requirements
        2. Develop clean, efficient, and modular Python code that satisfies all requirements
        3. Use best practices and design patterns
        4. Provide explanatory comments
        5. Handle edge cases and errors appropriately
        
        If your code is sent back for revision, carefully analyze the feedback and improve accordingly.
        """
        self.coding_agent = autogen.AssistantAgent(
            name="CodeDeveloper",
            system_message=system_message,
            llm_config=llm_config
        )
        
        # Code Review Agent
        system_message = """You are a senior code reviewer.
        Your job is to:
        1. Analyze code for bugs, inefficiencies, and security issues
        2. Check code against requirements to ensure all functionality is implemented
        3. Evaluate code readability and maintainability
        4. Provide specific, actionable feedback
        5. Make a clear PASS/REVISION NEEDED decision
        
        Be thorough but fair. Cite specific issues and suggest improvements.
        """
        self.code_review_agent = autogen.AssistantAgent(
            name="CodeReviewer",
            system_message=system_message,
            llm_config=llm_config
        )
        
        # Documentation Agent
        system_message = """You are a documentation specialist.
        Your job is to:
        1. Create comprehensive documentation for Python code
        2. Follow standard documentation formats
        3. Include overview, installation instructions, usage examples, and API references
        4. Ensure documentation is clear for both technical and non-technical users
        5. Use Markdown format for the documentation
        
        Focus on clarity, completeness, and usability.
        """
        self.doc_agent = autogen.AssistantAgent(
            name="DocumentationSpecialist",
            system_message=system_message,
            llm_config=llm_config
        )
        
        # Test Case Generation Agent
        system_message = """You are a test engineering expert.
        Your job is to:
        1. Generate comprehensive test cases for Python code
        2. Write both unit tests and integration tests using pytest
        3. Ensure high test coverage
        4. Include edge cases and error handling tests
        5. Develop test fixtures and setup/teardown as needed
        
        Make tests thorough, maintainable, and descriptive.
        """
        self.test_agent = autogen.AssistantAgent(
            name="TestEngineer",
            system_message=system_message,
            llm_config=llm_config
        )
        
        # Streamlit UI Agent
        system_message = """You are a Streamlit UI development expert.
        Your job is to:
        1. Create intuitive Streamlit UIs for Python applications
        2. Develop responsive, user-friendly interfaces
        3. Implement proper input validation and error handling
        4. Design consistent styling and layout
        5. Integrate the UI with the underlying application functionality
        
        Focus on usability, aesthetics, and functional completeness.
        """
        self.ui_agent = autogen.AssistantAgent(
            name="StreamlitUIDesigner",
            system_message=system_message,
            llm_config=llm_config
        )
        
    def run_requirement_analysis(self, natural_language_req: str) -> str:
        """Run the requirement analysis agent to structure requirements."""
        print_step("RequirementAnalyst", "Analyzing requirements...")
        
        # Store the original requirement
        self.state["requirement"] = natural_language_req
        
        # Start a conversation with the requirement analysis agent
        self.user_proxy.initiate_chat(
            self.req_analysis_agent,
            message=f"""Please analyze and structure the following requirements into a detailed, 
            JSON-formatted software specification. Identify all functional and non-functional requirements.
            
            REQUIREMENTS:
            {natural_language_req}
            
            Output the structured requirements in JSON format with appropriate sections for:
            - Project overview
            - Functional requirements (broken down by feature/component)
            - Non-functional requirements
            - Technical constraints
            - API specifications (if applicable)
            - Data models (if applicable)
            """
        )
        
        # Extract the structured requirements from the conversation
        last_message = self.req_analysis_agent.last_message()
        self.state["structured_requirement"] = last_message["content"]
        
        # Save to file
        save_to_file(self.state["structured_requirement"], "output/structured_requirements.json")
        
        return self.state["structured_requirement"]
    
    def run_code_development(self, structured_req: str) -> str:
        """Run the coding agent to develop code based on structured requirements."""
        print_step("CodeDeveloper", "Developing code...")
        
        # Start a conversation with the coding agent
        self.user_proxy.initiate_chat(
            self.coding_agent,
            message=f"""Please develop Python code according to these structured requirements. 
            Write clean, well-commented, modular code that implements all required functionality.
            
            STRUCTURED REQUIREMENTS:
            {structured_req}
            
            Please provide fully functional Python code that meets all requirements.
            """
        )
        
        # Extract the code from the conversation
        last_message = self.coding_agent.last_message()
        self.state["code"] = last_message["content"]
        
        # Clean up code (extract from markdown if needed)
        if "```python" in self.state["code"]:
            code_parts = self.state["code"].split("```python")
            for part in code_parts[1:]:
                if "```" in part:
                    clean_code = part.split("```")[0].strip()
                    self.state["code"] = clean_code
                    break
        
        # Save to file
        save_to_file(self.state["code"], "output/code/main.py")
        
        return self.state["code"]
    
    def run_code_review(self, code: str, requirements: str) -> Tuple[bool, str]:
        """Run the code review agent to check code quality."""
        print_step("CodeReviewer", "Reviewing code...")
        
        # Start a conversation with the code review agent
        self.user_proxy.initiate_chat(
            self.code_review_agent,
            message=f"""Please review the following Python code against the provided requirements.
            Evaluate for correctness, efficiency, readability, and security.
            
            REQUIREMENTS:
            {requirements}
            
            CODE:
            ```python
            {code}
            ```
            
            Please provide detailed feedback and explicitly state if the code PASSES review 
            or NEEDS REVISION. If revision is needed, clearly explain what needs to be fixed.
            """
        )
        
        # Extract the review from the conversation
        last_message = self.code_review_agent.last_message()
        review_content = last_message["content"]
        
        # Determine if the code passed review
        passed = "PASS" in review_content.upper() and "NEEDS REVISION" not in review_content.upper()
        self.state["review_passed"] = passed
        
        # Save to file
        save_to_file(review_content, "output/code_review.md")
        
        return passed, review_content
    
    def run_code_iteration(self, code: str, review_feedback: str, requirements: str) -> str:
        """Run another iteration of code development based on review feedback."""
        print_step("CodeDeveloper", "Revising code based on feedback...")
        
        # Start a conversation with the coding agent for revision
        self.user_proxy.initiate_chat(
            self.coding_agent,
            message=f"""Please revise the code based on the review feedback below.
            Ensure all issues are addressed while maintaining compatibility with requirements.
            
            ORIGINAL REQUIREMENTS:
            {requirements}
            
            CURRENT CODE:
            ```python
            {code}
            ```
            
            REVIEW FEEDBACK:
            {review_feedback}
            
            Please provide the revised code that addresses all feedback points.
            """
        )
        
        # Extract the revised code from the conversation
        last_message = self.coding_agent.last_message()
        revised_code = last_message["content"]
        
        # Clean up code (extract from markdown if needed)
        if "```python" in revised_code:
            code_parts = revised_code.split("```python")
            for part in code_parts[1:]:
                if "```" in part:
                    clean_code = part.split("```")[0].strip()
                    revised_code = clean_code
                    break
        
        self.state["code"] = revised_code
        
        # Save to file
        save_to_file(revised_code, "output/code/main_revised.py")
        
        return revised_code
    
    def run_documentation_generation(self, code: str, requirements: str) -> str:
        """Run the documentation agent to generate documentation."""
        print_step("DocumentationSpecialist", "Generating documentation...")
        
        # Start a conversation with the documentation agent
        self.user_proxy.initiate_chat(
            self.doc_agent,
            message=f"""Please generate comprehensive documentation for the following Python code.
            Include project overview, installation instructions, usage examples, and API reference.
            
            REQUIREMENTS:
            {requirements}
            
            CODE:
            ```python
            {code}
            ```
            
            Please provide well-structured Markdown documentation that would help users understand and use this code.
            """
        )
        
        # Extract the documentation from the conversation
        last_message = self.doc_agent.last_message()
        documentation = last_message["content"]
        self.state["documentation"] = documentation
        
        # Save to file
        save_to_file(documentation, "output/docs/documentation.md")
        
        return documentation
    
    def run_test_generation(self, code: str, requirements: str) -> str:
        """Run the test generation agent to create tests."""
        print_step("TestEngineer", "Generating test cases...")
        
        # Start a conversation with the test agent
        self.user_proxy.initiate_chat(
            self.test_agent,
            message=f"""Please generate comprehensive pytest test cases for the following Python code.
            Include unit tests and integration tests with appropriate fixtures.
            
            REQUIREMENTS:
            {requirements}
            
            CODE:
            ```python
            {code}
            ```
            
            Please provide complete, runnable pytest test cases that thoroughly test all functionality.
            """
        )
        
        # Extract the tests from the conversation
        last_message = self.test_agent.last_message()
        tests = last_message["content"]
        
        # Clean up tests (extract from markdown if needed)
        if "```python" in tests:
            test_parts = tests.split("```python")
            extracted_tests = ""
            for part in test_parts[1:]:
                if "```" in part:
                    extracted_tests += part.split("```")[0].strip() + "\n\n"
            if extracted_tests:
                tests = extracted_tests
        
        self.state["tests"] = tests
        
        # Save to file
        save_to_file(tests, "output/tests/test_main.py")
        
        return tests
    
    def run_streamlit_ui_generation(self, code: str, requirements: str) -> str:
        """Run the Streamlit UI agent to create a UI."""
        print_step("StreamlitUIDesigner", "Generating Streamlit UI...")
        
        # Start a conversation with the UI agent
        self.user_proxy.initiate_chat(
            self.ui_agent,
            message=f"""Please generate a Streamlit UI for the following Python application.
            Create an intuitive, user-friendly interface that allows users to interact with all functionality.
            
            REQUIREMENTS:
            {requirements}
            
            APPLICATION CODE:
            ```python
            {code}
            ```
            
            Please provide a complete, runnable Streamlit app.py file that integrates with the application code.
            """
        )
        
        # Extract the UI code from the conversation
        last_message = self.ui_agent.last_message()
        ui_code = last_message["content"]
        
        # Clean up UI code (extract from markdown if needed)
        if "```python" in ui_code:
            ui_parts = ui_code.split("```python")
            for part in ui_parts[1:]:
                if "```" in part:
                    clean_ui = part.split("```")[0].strip()
                    ui_code = clean_ui
                    break
        
        self.state["ui_code"] = ui_code
        
        # Save to file
        save_to_file(ui_code, "output/code/app.py")
        
        return ui_code
    
    def run_full_pipeline(self, natural_language_req: str) -> Dict:
        """Run the full multi-agent pipeline."""
        print(f"{Colors.BOLD}{Colors.BLUE}Starting Multi-Agent Coding Pipeline{Colors.ENDC}")
        
        # Step 1: Requirement Analysis
        structured_req = self.run_requirement_analysis(natural_language_req)
        
        # Step 2: Code Development
        code = self.run_code_development(structured_req)
        
        # Step 3: Code Review (and potential iterations)
        max_iterations = 3
        iteration = 0
        passed = False
        
        while not passed and iteration < max_iterations:
            passed, review_feedback = self.run_code_review(code, structured_req)
            
            if not passed:
                print_step("System", f"Code review failed. Iteration {iteration + 1}/{max_iterations}")
                code = self.run_code_iteration(code, review_feedback, structured_req)
                iteration += 1
            else:
                print_step("System", "Code review passed!")
        
        # If still not passed after max iterations, we proceed anyway
        if not passed:
            print_step("System", f"{Colors.WARNING}Warning: Proceeding with code that did not pass review after {max_iterations} iterations{Colors.ENDC}")
        
        # Step 4: Documentation Generation
        documentation = self.run_documentation_generation(code, structured_req)
        
        # Step 5: Test Generation
        tests = self.run_test_generation(code, structured_req)
        
        # Step 6: Streamlit UI Generation
        ui_code = self.run_streamlit_ui_generation(code, structured_req)
        
        # Final step: Compile results
        print(f"{Colors.BOLD}{Colors.GREEN}Multi-Agent Coding Pipeline Completed{Colors.ENDC}")
        
        return {
            "requirement": natural_language_req,
            "structured_requirement": structured_req,
            "code": code,
            "documentation": documentation,
            "tests": tests,
            "ui_code": ui_code,
            "review_passed": passed
        }

# Main CLI entry point
if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--cli":
        # CLI mode
        system = MultiAgentCodingSystem()
        
        print("Enter your natural language requirements (press Ctrl+D when finished):")
        lines = sys.stdin.readlines()
        requirements = ''.join(lines)
        
        results = system.run_full_pipeline(requirements)
        print(f"\n{Colors.BOLD}Pipeline completed with {'success' if results['review_passed'] else 'warnings'}{Colors.ENDC}")
    else:
        print("This is the main module for the Multi-Agent Coding System.")
        print("To run in CLI mode: python main.py --cli")
        print("To run with Streamlit interface: streamlit run app.py")