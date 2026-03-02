import asyncio
from typing import Union, List

from pipelineFramework.server.pipeline.config import PipelineConfig, StepConfig
from pipelineFramework.server.pipeline.status import EventType

from scrapers.FFG import FFG


class FFPScraper(StepConfig):
    async def run(self):
        ffg = FFG()
        async for event in ffg.get_results():
            yield event

    def name(self) -> str:
        return 'get'

    def display_name(self):
        return 'Test Step'

    def dependencies(self) -> Union[List[str], None]:
        return None


class TestStep2(StepConfig):
    async def run(self):
        yield "Sleep for 1 second", EventType.INFO
        await asyncio.sleep(1)
        yield "Test Warning", EventType.WARNING
        await asyncio.sleep(1)
        print('This is another test step')

    def name(self) -> str:
        return 'test2'

    def display_name(self):
        return 'Test Step'

    def dependencies(self) -> Union[List[str], None]:
        return None


DEMO_PIPELINE = PipelineConfig(name='demo', display_name='Demo Pipeline', steps=[FFPScraper(), TestStep2()],
                               parallelize=True)
