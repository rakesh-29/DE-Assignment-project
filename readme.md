# Multi-Agent Coding Framework

A collaborative AI system that transforms natural language requirements into fully functional Python code using specialized agents.

## Overview

This project implements a Multi-Agentic Framework using AutoGen where specialized agents work together to develop software from natural language requirements. The system includes:

- **Requirement Analysis Agent**: Transforms natural language into structured software requirements
- **Coding Agent**: Converts requirements into functional Python code
- **Code Review Agent**: Reviews code for correctness, efficiency, and security
- **Documentation Agent**: Generates comprehensive documentation
- **Test Case Generation Agent**: Creates unit and integration tests
- **Streamlit UI Agent**: Creates a user interface for the system

The agents work collaboratively in a pipeline, with each agent's output feeding into the next agent in the workflow.

## Architecture

```
DE-Assignment-project/
│
├── app.py                  # Streamlit UI for the multi-agent system
├── main.py                 # Core implementation of the multi-agent system
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables file (create this and add GROQ_API_KEY)
│── readme.md
└── output/                 # Generated outputs (created automatically)
    ├── code/               # Generated Python code
    ├── docs/               # Generated documentation
    └── tests/              # Generated test cases
```

## Key Features

- **Iterative Processing**: If code fails review, it's sent back to the Coding Agent for improvements
- **LLM Integration**: Support for multiple LLM providers (OpenAI, Groq)
- **User-Friendly Interface**: Streamlit UI for interaction with the system
- **Comprehensive Documentation**: Generated automatically for the developed code
- **Test Case Generation**: Creates unit and integration tests for the code

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/multi-agent-coding-framework.git
   cd DE-Assignment-project
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set Environment Variables  in .env
    Add environment variables:
    - `OPENAI_API_KEY`: Your OpenAI API key
    - `GROQ_API_KEY`: Your Groq API key
  
4. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage

1. Access the Streamlit interface at http://localhost:8501
2. Enter your requirements in natural language in the text area
4. Click "Run Pipeline" to start the process
5. View the results in the tabbed interface:
   - Structured requirements
   - Generated code
   - Documentation
   - Test cases
   - Streamlit UI code
   - System Logs



## Technical Requirements

- Python 3.8+
- Internet connection for LLM API access
- OpenAI or Groq cloud API credentials

## License

MIT License

## Acknowledgements

This project uses the following key libraries:
- [AutoGen](https://github.com/microsoft/autogen) for multi-agent coordination
- [Streamlit](https://streamlit.io/) for UI development
- [OpenAI](https://openai.com/) and [Groq](https://groq.com/) for LLM services
