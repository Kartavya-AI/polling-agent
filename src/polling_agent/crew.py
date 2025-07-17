from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from .tools.serper_tool import serper_tool
from .models.output import TwitterPost,LinkedInPost,PollsOutput

@CrewBase
class PollingAgent():
    """Poll and Post Creation Crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def trending_topic_searcher(self) -> Agent:
        return Agent(
            config=self.agents_config['trending_topic_searcher'],
            tools=[serper_tool],
            verbose=True
        )

    @agent
    def trend_relevance_verifier(self) -> Agent:
        return Agent(
            config=self.agents_config['trend_relevance_verifier'],
            verbose=True
        )

    @agent
    def content_structurer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_structurer'],
            verbose=True
        )

    @agent
    def engagement_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config['engagement_optimizer'],
            verbose=True
        )

    @agent
    def seo_optimizer(self) -> Agent:
        return Agent(
            config=self.agents_config['seo_optimizer'],
            verbose=True
        )

    @agent
    def content_drafter(self) -> Agent:
        return Agent(
            config=self.agents_config['content_drafter'],
            verbose=True
        )

    @agent
    def twitter_post_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['twitter_post_creator'],
            verbose=True
        )

    @agent
    def poll_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['poll_creator'],
            verbose=True
        )

    @agent
    def linkedin_post_creator(self) -> Agent:
        return Agent(
            config=self.agents_config['linkedin_post_creator'],
            verbose=True
        )

    @task
    def trending_topic_search_task(self) -> Task:
        return Task(
            config=self.tasks_config['trending_topic_search_task'],
            output_file="trendy_topic.md"
        )

    @task
    def trend_relevance_verification_task(self) -> Task:
        return Task(
            config=self.tasks_config['trend_relevance_verification_task'],
            context=[self.trending_topic_search_task()],
            output_file="trendy_relev.md"
        )

    @task
    def content_structuring_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_structuring_task'],
            context=[self.trend_relevance_verification_task()],
            output_file="conten_struc.md"
        )

    @task
    def engagement_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['engagement_optimization_task'],
            context=[self.content_structuring_task()],
            output_file="engag_opt.md"
        )

    @task
    def seo_optimization_task(self) -> Task:
        return Task(
            config=self.tasks_config['seo_optimization_task'],
            context=[self.engagement_optimization_task()],
            output_file="seo_opt.md"
        )

    @task
    def content_drafting_task(self) -> Task:
        return Task(
            config=self.tasks_config['content_drafting_task'],
            context=[self.content_structuring_task(),self.engagement_optimization_task(),self.seo_optimization_task()],
            output_file="cont_draft.md"
        )


    @task
    def twitter_post_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['twitter_post_creation_task'],
            context=[self.content_drafting_task()],
            output_json=TwitterPost
        )

    @task
    def poll_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['poll_creation_task'],
            context=[self.content_drafting_task(),self.twitter_post_creation_task()],
            output_json=PollsOutput
        )

    @task
    def linkedin_post_creation_task(self) -> Task:
        return Task(
            config=self.tasks_config['linkedin_post_creation_task'],
            context=[self.content_drafting_task()],
            output_json=LinkedInPost
        )

    @crew
    def crew(self) -> Crew:
        """Creates the PollingAgent Crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
