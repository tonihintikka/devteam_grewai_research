import http.client
import json
import os
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task, before_kickoff
from crewai.tools import BaseTool
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class SerperSearchTool(BaseTool):
    """
    Serper.dev search tool for the CrewAI agent.
    """

    name: str = "serper_search"
    description: str = "A tool to search for information using Serper.dev."
    api_key: str

    def _run(self, query: str) -> dict:
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        try:
            conn.request("POST", "/search", payload, headers)
            res = conn.getresponse()
            data = res.read()
            return json.loads(data.decode("utf-8"))
        except Exception as e:
            return {"error": str(e)}


@CrewBase
class Devteam():
    """Devteam crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.inputs = kwargs.get('inputs', {})

    @before_kickoff
    def pull_data_example(self, inputs):
        """
        Performs a Google search using Serper.dev and saves the results in Markdown format.
        """
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"q": inputs['topic']})
        headers = {
            'X-API-KEY': os.getenv("SERPER_API_KEY"),
            'Content-Type': 'application/json'
        }
        try:
            conn.request("POST", "/search", payload, headers)
            res = conn.getresponse()
            data = res.read()
            search_results = json.loads(data.decode("utf-8"))
            inputs['extra_data'] = search_results.get('organic', [])

            # Save results to a Markdown file
            with open('intermediate_research_results.md', 'w') as f:
                f.write(f"# Research Results for {inputs['topic']}\n\n")
                for i, result in enumerate(inputs['extra_data'], start=1):
                    f.write(f"## {i}. {result['title']}\n")
                    f.write(f"{result['snippet']}\n")
                    f.write(f"[Link]({result['link']})\n\n")
        except Exception as e:
            print(f"Error during Serper.dev search: {e}")

        # Update self.inputs with any changes
        self.inputs.update(inputs)
        return inputs

    def serper_search_tool(self):
        api_key = os.getenv("SERPER_API_KEY")
        if not api_key:
            raise ValueError("SERPER_API_KEY is not set in the environment.")
        return SerperSearchTool(api_key=api_key)

    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=[self.serper_search_tool()],
            inputs=self.inputs,
            verbose=True
        )

    @agent
    def reporting_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['reporting_analyst'],
            inputs=self.inputs,
            verbose=True
        )

    @task
    def research_task(self) -> Task:
        return Task(
            config=self.tasks_config['research_task'],
            agent=self.researcher(),
            inputs=self.inputs,
            output_file='intermediate_research_results.md'
        )

    @task
    def reporting_task(self) -> Task:
        return Task(
            config=self.tasks_config['reporting_task'],
            agent=self.reporting_analyst(),
            inputs=self.inputs,
            output_file='final_report.md'
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            inputs=self.inputs,
            verbose=True,
        )