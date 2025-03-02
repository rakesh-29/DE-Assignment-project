import streamlit as st
import sys
import os
import time
from main import MultiAgentCodingSystem, Colors

def create_streamlit_app():
    """Create a Streamlit application for the multi-agent system."""
    st.set_page_config(page_title="Multi-Agent Coding System", layout="wide")
    
    st.title("Automated Project Creation Using Agents")
    st.subheader("Generate code from natural language requirements")
    
    # System description
    with st.expander("About this system", expanded=True):
        st.markdown("""
        This system uses a multi-agent framework powered by LLMs to convert natural language requirements into working code.
        
        **Agents in the pipeline:**
        1. **Requirement Analysis Agent** - Structures natural language requirements
        2. **Coding Agent** - Develops Python code based on structured requirements
        3. **Code Review Agent** - Reviews code and provides feedback
        4. **Documentation Agent** - Creates comprehensive documentation
        5. **Test Case Generation Agent** - Develops test cases
        6. **Streamlit UI Agent** - Creates a user interface
        
        Enter your requirements below to start the process.
        """)
    
    # Input section
    st.header("Requirements Input")
    requirement = st.text_area("Enter your natural language requirements here:", 
                               height=200,
                               placeholder="Example: Create a weather application that fetches current weather data from an API based on user-provided location...")
    
    # Create tabs for different outputs
    output_tabs = st.tabs([
        "Structured Requirements", 
        "Code", 
        "Documentation", 
        "Tests", 
        "UI Code",
        "System Log"
    ])
    
    # Initialize session state
    if 'pipeline_results' not in st.session_state:
        st.session_state.pipeline_results = None
    if 'log_output' not in st.session_state:
        st.session_state.log_output = []
    
    # Custom stdout to capture print statements
    class StreamlitCapture:
        def __init__(self):
            self.content = []
            
        def write(self, content):
            self.content.append(content)
            content_str = ''.join(self.content)
            with output_tabs[5]:
                st.session_state.log_output.append(content)
                st.code(''.join(st.session_state.log_output), language=None)
                
        def flush(self):
            pass
    
    # Run the pipeline when a button is clicked
    col1, col2 = st.columns([1, 5])
    with col1:
        run_button = st.button("Generate Solution", type="primary", use_container_width=True)
    
    with col2:
        if run_button and requirement:
            # Set up a progress bar
            progress_bar = st.progress(0)
            progress_text = st.empty()
            progress_text.text("Initializing agents...")
            
            # Capture stdout
            original_stdout = sys.stdout
            capture = StreamlitCapture()
            sys.stdout = capture
            
            try:
                # Reset log output
                st.session_state.log_output = []
                
                # Initialize the multi-agent system
                system = MultiAgentCodingSystem()
                
                progress_bar.progress(10)
                progress_text.text("Running requirement analysis...")
                
                # Record the start time
                start_time = time.time()
                
                # Run the pipeline
                results = system.run_full_pipeline(requirement)
                st.session_state.pipeline_results = results
                
                # Calculate elapsed time
                elapsed_time = time.time() - start_time
                
                progress_bar.progress(100)
                progress_text.text(f"Solution generated in {elapsed_time:.2f} seconds!")
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
                import traceback
                st.code(traceback.format_exc())
            finally:
                # Restore stdout
                sys.stdout = original_stdout
    
    # Display results in tabs
    if st.session_state.pipeline_results:
        # Structured Requirements tab
        with output_tabs[0]:
            st.markdown("### Structured Requirements")
            st.code(st.session_state.pipeline_results["structured_requirement"], language="json")
            
            # Download button
            st.download_button(
                label="Download Structured Requirements",
                data=st.session_state.pipeline_results["structured_requirement"],
                file_name="structured_requirements.json",
                mime="application/json"
            )
        
        # Code tab
        with output_tabs[1]:
            st.markdown("### Generated Code")
            if st.session_state.pipeline_results["review_passed"]:
                st.success("✓ Code passed review")
            else:
                st.warning("⚠ Code did not pass all reviews")
            st.code(st.session_state.pipeline_results["code"], language="python")
            
            # Download button
            st.download_button(
                label="Download Code",
                data=st.session_state.pipeline_results["code"],
                file_name="main.py",
                mime="text/plain"
            )
        
        # Documentation tab
        with output_tabs[2]:
            st.markdown("### Documentation")
            st.markdown(st.session_state.pipeline_results["documentation"])
            
            # Download button
            st.download_button(
                label="Download Documentation",
                data=st.session_state.pipeline_results["documentation"],
                file_name="documentation.md",
                mime="text/plain"
            )
        
        # Tests tab
        with output_tabs[3]:
            st.markdown("### Test Cases")
            st.code(st.session_state.pipeline_results["tests"], language="python")
            
            # Download button
            st.download_button(
                label="Download Tests",
                data=st.session_state.pipeline_results["tests"],
                file_name="test_main.py",
                mime="text/plain"
            )
        
        # UI Code tab
        with output_tabs[4]:
            st.markdown("### Streamlit UI Code")
            st.code(st.session_state.pipeline_results["ui_code"], language="python")
            
            # Download button
            st.download_button(
                label="Download UI Code",
                data=st.session_state.pipeline_results["ui_code"],
                file_name="app.py",
                mime="text/plain"
            )
    
    # Log tab (already handled by the StreamlitCapture class)
    with output_tabs[5]:
        if not st.session_state.log_output:
            st.info("Run the system to see logs")
        else:
            # Already populated by the capture system
            pass

if __name__ == "__main__":
    create_streamlit_app()