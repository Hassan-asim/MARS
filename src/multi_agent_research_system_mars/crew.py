import os
from dotenv import load_dotenv

from crewai import LLM
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import (
	SerperDevTool,
	VisionTool
)

from .tools.gmail_tool import gmail_tool
from .tools.pdf_generator_tool import pdf_generator_tool

# Load environment variables
config_path = os.path.join(os.path.dirname(__file__), '..', '..', 'config.env')
load_dotenv(config_path)



@CrewBase
class MultiAgentResearchSystemMarsCrew:
    """MultiAgentResearchSystemMars crew"""

    
    @agent
    def research_coordinator(self) -> Agent:

        
        return Agent(
            config=self.agents_config["research_coordinator"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def technology_research_agent(self) -> Agent:

        
        return Agent(
            config=self.agents_config["technology_research_agent"],
            
            
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def market_research_agent(self) -> Agent:

        
        return Agent(
            config=self.agents_config["market_research_agent"],
            
            
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def technical_feasibility_agent(self) -> Agent:

        
        return Agent(
            config=self.agents_config["technical_feasibility_agent"],
            
            
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def documentation_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["documentation_specialist"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def visualization_specialist(self) -> Agent:

        
        return Agent(
            config=self.agents_config["visualization_specialist"],
            
            
            tools=[

            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def validation_agent(self) -> Agent:

        
        return Agent(
            config=self.agents_config["validation_agent"],
            
            
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def patent_ip_research_agent(self) -> Agent:

        
        return Agent(
            config=self.agents_config["patent_ip_research_agent"],
            
            
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def financial_analysis_agent(self) -> Agent:

        
        return Agent(
            config=self.agents_config["financial_analysis_agent"],
            
            
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def user_experience_research_agent(self) -> Agent:

        
        return Agent(
            config=self.agents_config["user_experience_research_agent"],
            
            
            tools=[
				VisionTool(),
				SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def regulatory_compliance_agent(self) -> Agent:

        
        return Agent(
            config=self.agents_config["regulatory_compliance_agent"],
            
            
            tools=[
				SerperDevTool()
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    
    @agent
    def pdf_document_generator(self) -> Agent:
        return Agent(
            config=self.agents_config["pdf_document_generator"],
            
            
            tools=[
                pdf_generator_tool
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )

    @agent
    def email_distribution_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["email_distribution_agent"],
            
            
            tools=[
				gmail_tool
            ],
            reasoning=False,
            max_reasoning_attempts=None,
            inject_date=True,
            allow_delegation=False,
            max_iter=25,
            max_rpm=None,
            max_execution_time=None,
            llm=LLM(
                model="gpt-4o-mini",
                temperature=0.7,
            ),
            
        )
    

    
    @task
    def research_planning_and_coordination(self) -> Task:
        return Task(
            config=self.tasks_config["research_planning_and_coordination"],
            markdown=False,
            
            
        )
    
    @task
    def technology_research_and_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["technology_research_and_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def market_analysis_and_competitive_research(self) -> Task:
        return Task(
            config=self.tasks_config["market_analysis_and_competitive_research"],
            markdown=False,
            
            
        )
    
    @task
    def patent_and_ip_landscape_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["patent_and_ip_landscape_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def technical_feasibility_assessment(self) -> Task:
        return Task(
            config=self.tasks_config["technical_feasibility_assessment"],
            markdown=False,
            
            
        )
    
    @task
    def financial_analysis_and_business_model_validation(self) -> Task:
        return Task(
            config=self.tasks_config["financial_analysis_and_business_model_validation"],
            markdown=False,
            
            
        )
    
    @task
    def user_experience_and_design_analysis(self) -> Task:
        return Task(
            config=self.tasks_config["user_experience_and_design_analysis"],
            markdown=False,
            
            
        )
    
    @task
    def visual_documentation_and_diagrams(self) -> Task:
        return Task(
            config=self.tasks_config["visual_documentation_and_diagrams"],
            markdown=False,
            
            
        )
    
    @task
    def regulatory_and_compliance_assessment(self) -> Task:
        return Task(
            config=self.tasks_config["regulatory_and_compliance_assessment"],
            markdown=False,
            
            
        )
    
    @task
    def comprehensive_documentation_creation(self) -> Task:
        return Task(
            config=self.tasks_config["comprehensive_documentation_creation"],
            markdown=False,
            
            
        )
    
    @task
    def research_validation_and_final_report(self) -> Task:
        return Task(
            config=self.tasks_config["research_validation_and_final_report"],
            markdown=False,
            
            
        )
    
    @task
    def professional_pdf_document_generation(self) -> Task:
        return Task(
            config=self.tasks_config["professional_pdf_document_generation"],
            markdown=False,
            
            
        )

    @task
    def email_research_package_distribution(self) -> Task:
        return Task(
            config=self.tasks_config["email_research_package_distribution"],
            markdown=False,
            
            
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the MultiAgentResearchSystemMars crew"""
        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
        )

    def _load_response_format(self, name):
        with open(os.path.join(self.base_directory, "config", f"{name}.json")) as f:
            json_schema = json.loads(f.read())

        return SchemaConverter.build(json_schema)
