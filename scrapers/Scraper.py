from abc import ABCMeta, abstractmethod
from datetime import datetime

import pandas as pd

from pipelineFramework.server.pipeline.status import EventType
from pipelineFramework.server.pipeline.step import Event


class Scraper(metaclass=ABCMeta):
    @abstractmethod
    async def get_results_for_keyword(self, keyword: str) -> pd.DataFrame:
        raise NotImplementedError

    async def get_results(self):
        keywords = ['nano']
        aggregated_csv = pd.DataFrame()
        for keyword in keywords:
            csv = await self.get_results_for_keyword(keyword)
            yield f"{len(csv)} results found for keyword '{keyword}'", EventType.INFO
            print(csv)
            aggregated_csv += csv

        yield aggregated_csv.to_string(), EventType.RESULT
