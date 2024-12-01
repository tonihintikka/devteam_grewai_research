# Devteam Crew

Welcome to the Devteam Crew project, powered by [crewAI](https://crewai.com). This project is designed to automate research tasks using a multi-agent AI system, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex research tasks, maximizing their collective intelligence and capabilities. We've integrated the Serper.dev Google Search API to enhance the agents' ability to gather information from the web.

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [UV](https://docs.astral.sh/uv/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install UV:

```bash
pip install uv
```

Next, navigate to your project directory and install the dependencies:

(Optional) Lock the dependencies and install them by using the CLI command:

```bash
crewai install
```

### Customizing

**Add your `OPENAI_API_KEY` and `SERPER_API_KEY` into the `.env` file**

- Create a `.env` file in the `src/devteam` directory (if it doesn't already exist) and add:

  ```bash
  OPENAI_API_KEY=your_openai_api_key_here
  SERPER_API_KEY=your_serper_api_key_here
  ```

- Modify `src/devteam/config/agents.yaml` to define your agents. Agents can use the `{topic}` placeholder to dynamically include the research topic.

- Modify `src/devteam/config/tasks.yaml` to define your tasks. Tasks can also use `{topic}` to refer to the research topic.

- Modify `src/devteam/crew.py` to add your own logic, tools, and specific arguments. We've implemented the `SerperSearchTool` to enable agents to perform Google searches via the Serper.dev API.

- Modify `src/devteam/main.py` to add custom inputs for your agents and tasks. Specify your research topic in the `inputs` dictionary.

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
crewai run  
```

Alternatively, you can run the main script directly:

```bash
python3 src/devteam/main.py
```

This command initializes the Devteam Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will create a `final_report.md` file with the output of research on the specified topic.

## Understanding Your Crew

The Devteam Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

- **Agents:**

  - **Researcher:** Performs in-depth research on the specified topic using the Serper.dev Google Search API.
  - **Reporting Analyst:** Analyzes the research findings and compiles them into a detailed report.

- **Tasks:**

  - **Research Task:** Conducts thorough research on the topic and generates intermediate results.
  - **Reporting Task:** Processes the intermediate results and produces the final report.

## Setting Up the Serper.dev API

To enable your agents to perform web searches, you'll need to set up an account with Serper.dev and obtain an API key.

1. **Sign Up:** Visit [Serper.dev](https://serper.dev/) and create an account.
2. **Obtain API Key:** After logging in, navigate to your dashboard to find your API key.
3. **Configure `.env` File:** Add your `SERPER_API_KEY` to the `.env` file as shown above.

## Customizing the Research Topic

In `src/devteam/main.py`, specify your research topic in the `inputs` dictionary:

```python
def run():
    inputs = {
        'topic': 'Your research topic here'
    }
    devteam = Devteam(inputs=inputs)
    devteam.crew().kickoff()
```

Replace `'Your research topic here'` with the topic you want the agents to research.

## Viewing the Reports

- **Intermediate Results:** The agents will generate `intermediate_research_results.md`, containing summaries of the top search results.
- **Final Report:** The `final_report.md` file will contain the comprehensive report compiled by the Reporting Analyst agent.

## Support

For support, questions, or feedback regarding the Devteam Crew or crewAI:

- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.

