from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor

from ai.services.llm_service.deepseek import deepseek_llm
from ai.utilities import get_data_path, read_from_file
from ai.workflows.base_builder.base_builder import BaseBuilder


class ResumeBuilder(BaseBuilder):
    def invoke(self):
        workflow = self._initialize_supervisor()
        app = workflow.compile()
        resume_data = self._load_experience()
        for data in app.stream(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
                            Create impressive resume based on below data:
                            {resume_data}
                        """,
                    }
                ]
            }
        ):
            print(data)

    def _load_experience(self):
        return read_from_file(get_data_path("resume/data.txt"))

    def _initialize_resume_writer_agent(self):
        return create_react_agent(
            model=deepseek_llm,
            tools=[],
            name="resume_writer",
            prompt=(
                "You have to write an impressive resume to get hired"
                "You have to improve resume based on feedback from critique"
            ),
        )

    def _initialize_resume_critique_agent(self):
        return create_react_agent(
            model=deepseek_llm,
            tools=[],
            name="resume_critique",
            prompt="You have to critique resume and provide detailed feedback to improve resume",
        )

    def _initialize_supervisor(self):
        resume_critique = self._initialize_resume_critique_agent()
        resume_writer = self._initialize_resume_writer_agent()
        return create_supervisor(
            [resume_writer, resume_critique],
            model=deepseek_llm,
            name="supervisor",
            prompt=(
                "You are a team supervisor managing a resume writer and a resume critique. "
                "Get feedback from critique once resume is written"
                "Make 2 feedback rounds"
            ),
        )
