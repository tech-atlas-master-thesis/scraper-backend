import re
from io import BytesIO
from typing import List

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup

from pipelineFramework import UserStepConfig
from scrapers.Scraper import Scraper


class FFG(Scraper):
    PAGE_SIZE = 100

    def __init__(self, user_config: UserStepConfig):
        super().__init__()

        self.KEYWORDS = user_config.get("KEYWORDS")
        self.EXCEL_REQUEST_URI = user_config.get("EXCEL_REQUEST_URI")
        self.SEARCH_REQUEST_URI = user_config.get("SEARCH_REQUEST_URI")
        self.ID_HREF_REGEX = re.compile(user_config.get("ID_HREF_REGEX"))
        self.FOUND_KEYWORD_COLUMN = user_config.get("FOUND_KEYWORD_COLUMN")
        self.COLUMN_TRANSLATIONS = user_config.get("COLUMN_TRANSLATIONS")
        self.PROJECT_COLUMNS = user_config.get("PROJECT_COLUMNS")
        self.PROJECT_COLUMNS_ONLY_ON_FIRST_INSTANCE = user_config.get("PROJECT_COLUMNS_ONLY_ON_FIRST_INSTANCE")
        self.ORGANISATION_COLUMNS = user_config.get("ORGANISATION_COLUMNS")
        self.ORGANISATIONS_COLUMN_NAME = user_config.get("ORGANISATIONS_COLUMN_NAME")

        self.SCRAPE_GROUP = {
            "groupBy": self.PROJECT_COLUMNS,
            "aggregate": {
                self.ORGANISATIONS_COLUMN_NAME: list,
                **dict.fromkeys(self.PROJECT_COLUMNS_ONLY_ON_FIRST_INSTANCE, "first")
            },
            "combine": self.ORGANISATION_COLUMNS,
            "combinedColumn": self.ORGANISATIONS_COLUMN_NAME
        }

        self.AGGREGATE_GROUP = {
            "groupBy": self.SCRAPE_GROUP["groupBy"],
            "aggregate": {
                self.FOUND_KEYWORD_COLUMN: list,
                **dict.fromkeys(self.SCRAPE_GROUP["aggregate"].keys(), "first")
            }
        }

    async def get_results_for_keyword(self, keyword: str) -> pd.DataFrame:
        ids = await self.get_all_ids_for_keyword(keyword)
        async with aiohttp.ClientSession() as session:
            async with session.post(self.EXCEL_REQUEST_URI, ssl=False, data={
                "id[]": ids,
                "projects_selected": str(len(ids)),
                "projects_total": str(len(ids)),
            }) as response:
                excel_file = BytesIO(await response.content.read())
                csv = pd.read_excel(excel_file, engine="calamine", skiprows=4)
        transformed = self._group_scrape_dataframe(csv)
        transformed[self.FOUND_KEYWORD_COLUMN] = keyword.lower()
        return transformed

    def _group_scrape_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        dataframe.rename(columns=self.COLUMN_TRANSLATIONS, inplace=True)
        dataframe[self.SCRAPE_GROUP["combinedColumn"]] = dataframe[self.SCRAPE_GROUP["combine"]].to_dict("records")
        return (dataframe
                .groupby(self.SCRAPE_GROUP["groupBy"], as_index=False)
                .agg(self.SCRAPE_GROUP["aggregate"]))

    async def aggregate_dataframes(self, dataframes: List[pd.DataFrame]) -> pd.DataFrame:
        return (pd.concat(dataframes)
                .groupby(self.AGGREGATE_GROUP["groupBy"], as_index=False)
                .agg(self.AGGREGATE_GROUP["aggregate"]))

    async def get_all_ids_for_keyword(self, keyword: str) -> List[str]:
        page = 0
        ids: List[str] = []
        while True:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.SEARCH_REQUEST_URI.format(query=keyword, page=page), ssl=False) as response:
                    soup = BeautifulSoup(await response.text(), "html.parser")
                    links = soup.find(id="searchresults").find_all("a", href=self.ID_HREF_REGEX)
                    if not links:
                        return ids
                    page += self.PAGE_SIZE
                    for link in links:
                        try:
                            extracted_id = self.ID_HREF_REGEX.search(str(link)).groups()[0]
                            ids.append(extracted_id)
                        except Exception as e:
                            print(e)
