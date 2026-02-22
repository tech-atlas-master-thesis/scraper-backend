import asyncio
import requests
from typing import Union, List

from pipelineFramework.server.pipeline.config import PipelineConfig, StepConfig
from pipelineFramework.server.pipeline.status import EventType


class TestStep(StepConfig):
    async def run(self):
        async with aiohttp.ClientSession() as session:
            async with session.post("https://projekte.ffg.at/projekt/excel", data={
                        id:[
                            "4641758",
                            "3327761",
                            "4822637",
                            "3155850",
                            "4641746",
                            "4639662",
                            "4008071",
                            "2920229",
                            "5130677",
                            "3159953",
                            "1767647",
                            "2887881",
                            "4363500",
                            "1410447",
                            "4641713",
                        ]
                        advanced_search:	"1"
                        go:	"1"
                        q:	"nanotechnologie"
                        titel:	""
                        inhalt:	""
                        projektbeginn:	""
                        projektende:	""
                        foerderung:	""
                        foerdernehmer:	""
                        status:	""
                        projects_selected:	"15"
                        projects_total:	"15"
                      }) as response:
                      data = await response.text()
                      print(data)
        getFile = await requests.as("https://projekte.ffg.at/projekt/excel")

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


DEMO_PIPELINE = PipelineConfig(name='demo', display_name='Demo Pipeline', steps=[TestStep(), TestStep2()], parallelize=True)