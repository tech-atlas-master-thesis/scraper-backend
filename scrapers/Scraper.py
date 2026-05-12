from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any

import pandas as pd

from pipelineFramework import EventType


class Scraper(metaclass=ABCMeta):
    @dataclass
    class Keyword:
        name: str
        search: List[str]

    @abstractmethod
    def get_keywords(self) -> List[Keyword]:
        pass

    @abstractmethod
    async def get_results_for_keyword(self, keyword: Keyword) -> pd.DataFrame | None:
        raise NotImplementedError

    async def aggregate_dataframes(self, dataframes: List[pd.DataFrame]) -> pd.DataFrame:
        raise NotImplementedError

    async def get_results(self):
        dfs = []
        for keyword in self.get_keywords():
            yield f"Searching for keyword \"{keyword.name}\" with search terms [{', '.join(keyword.search)}]", EventType.INFO
            csv = await self.get_results_for_keyword(keyword)
            if csv is None:
                yield f'No results found for keyword "{keyword.name}"', EventType.WARNING
                continue
            yield f'{len(csv)} results found for keyword "{keyword.name}"', EventType.INFO
            dfs.append(csv)

        aggregated_csv = await self.aggregate_dataframes(dfs)
        yield aggregated_csv, EventType.RESULT
