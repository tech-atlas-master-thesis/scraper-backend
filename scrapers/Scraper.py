from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from typing import List, Dict, Any, Tuple

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
    async def get_results_for_keyword(self, keyword: Keyword) -> Tuple[pd.DataFrame | None, List[str]]:
        raise NotImplementedError

    async def aggregate_dataframes(self, dataframes: List[pd.DataFrame]) -> pd.DataFrame:
        raise NotImplementedError

    @abstractmethod
    async def get_data_identifier(self) -> str:
        return ""

    async def get_results(self):
        dfs = []
        keywords = self.get_keywords()
        for i, keyword in enumerate(keywords):
            yield f"({i}/{len(keywords)}) Searching for keyword \"{keyword.name}\" with search terms [{', '.join(keyword.search)}]", EventType.INFO
            csv, warnings = await self.get_results_for_keyword(keyword)
            if warnings:
                yield "\n".join(warnings), EventType.WARNING
            if csv is None:
                yield f'No results found for keyword "{keyword.name}"', EventType.WARNING
                continue
            yield f'{len(csv)} results found for keyword "{keyword.name}"', EventType.INFO
            dfs.append(csv)

        aggregated_csv = await self.aggregate_dataframes(dfs)
        aggregated_csv["data_source"] = self.get_data_identifier()
        yield aggregated_csv, EventType.RESULT
