import re
from io import BytesIO
from typing import List

import aiohttp
import pandas as pd
from bs4 import BeautifulSoup

from scrapers.Scraper import Scraper


class FFG(Scraper):
    PAGE_SIZE=100
    EXCEL_REQUEST_URI = "https://projekte.ffg.at/projekt/excel"
    SEARCH_REQUEST_URI = "https://projekte.ffg.at/projekt?advanced_search=1&go=1&q={query}&start={page}"
    ID_HREF_REGEX = re.compile(r'/projekt/(\d+)')

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
        return csv

    async def get_all_ids_for_keyword(self, keyword: str) -> List[str]:
        page = 0
        ids: List[str] = []
        while True:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.SEARCH_REQUEST_URI.format(query=keyword, page=page), ssl=False) as response:
                    soup = BeautifulSoup(await response.text(), 'html.parser')
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