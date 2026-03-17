from abc import ABCMeta, abstractmethod
from typing import List

import pandas as pd

from pipelineFramework import EventType


class Scraper(metaclass=ABCMeta):
    @abstractmethod
    async def get_results_for_keyword(self, keyword: str) -> pd.DataFrame:
        raise NotImplementedError

    async def aggregate_dataframes(self, dataframes: List[pd.DataFrame]) -> pd.DataFrame:
        raise NotImplementedError

    async def get_results(self):
        keywords = ["Nano", "Artificial Intelligence", "vaccine"]
        dfs = []
        for keyword in keywords:
            csv = await self.get_results_for_keyword(keyword)
            yield f"{len(csv)} results found for keyword '{keyword}'", EventType.INFO
            dfs.append(csv)

        aggregated_csv = await self.aggregate_dataframes(dfs)
        yield aggregated_csv, EventType.RESULT
