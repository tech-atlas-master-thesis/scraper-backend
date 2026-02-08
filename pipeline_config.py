from typing import Union, List, Dict

from pipelineFramework.server.pipeline.config import PipelineConfig, StepConfig


class TestStep(StepConfig):
    async def run(self):
        yield
        print('This is a test step')

    def name(self) -> str:
        return 'test'

    def display_name(self):
        return 'Test Step'

    def dependencies(self) -> Union[List[str], None]:
        return None


class TestStep2(StepConfig):
    async def run(self):
        yield
        print('This is another test step')

    def name(self) -> str:
        return 'test2'

    def display_name(self):
        return 'Test Step'

    def dependencies(self) -> Union[List[str], None]:
        return None

PIPELINE_CONFIGS: List[PipelineConfig] = [
    {
        'name': 'testConfig',
        'display_name': 'Test Config',
        'steps': [TestStep(), TestStep2()],
    },
]
