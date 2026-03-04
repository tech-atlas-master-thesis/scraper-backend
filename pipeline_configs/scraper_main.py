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
        return 'getDataFFG'

    def display_name(self):
        return 'Get Data from FFG'

    def dependencies(self) -> Union[List[str], None]:
        return None


class DummyStep(StepConfig):
    async def run(self):
        yield 'Dummy Step executed', EventType.INFO

    def name(self) -> str:
        return 'dummyStep'

    def display_name(self):
        return 'Dummy Step'

    def dependencies(self) -> Union[List[str], None]:
        return ['getDataFFG']


DEMO_PIPELINE = PipelineConfig(
    name='scraper_main',
    display_name='Scraper Pipeline',
    steps=[FFPScraper(), DummyStep()],
    parallelize=True
)
