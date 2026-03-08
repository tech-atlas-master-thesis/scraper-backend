from typing import Union, List

from pipelineFramework import EventType, LocalisationString, UserStepConfig, PipelineConfig, StepConfig, StepUserConfig
from scrapers.FFG import FFG


class FFPScraper(StepConfig):
    async def run(self, user_config: UserStepConfig):
        ffg = FFG(user_config)
        async for event in ffg.get_results():
            yield event

    def user_config(self) -> List[StepUserConfig]:
        return [
            StepUserConfig("EXCEL_REQUEST_URI",
                           LocalisationString("URI to request Excel file", "URI um Excel File zu beantragen"),
                           StepUserConfig.StepUserConfigType.STRING, "https://projekte.ffg.at/projekt/excel"),
            StepUserConfig("SEARCH_REQUEST_URI", LocalisationString("Project Search Request URI", "Projektsuche URI"),
                           StepUserConfig.StepUserConfigType.STRING,
                           "https://projekte.ffg.at/projekt?advanced_search=1&go=1&q={query}&start={page}"),
            StepUserConfig("ID_HREF_REGEX",
                           LocalisationString("RegExp to find href with ID", "RegExp um href mit ID zu finden"),
                           StepUserConfig.StepUserConfigType.STRING, "/projekt/(\d+)"),
            StepUserConfig("FOUND_KEYWORD_COLUMN",
                           LocalisationString("Column for used keyword", "Spalte für benuztes keyword"),
                           StepUserConfig.StepUserConfigType.STRING, "found_keyword"),
            StepUserConfig("COLUMN_TRANSLATIONS", LocalisationString("Columns renaming", "Spalten Umbenennung"),
                           StepUserConfig.StepUserConfigType.MAPPING, {
                               "Projekt-ID": "id",
                               "Kurztitel": "short_title",
                               "Langtitel": "long_title",
                               "Abstract": "abstract",
                               "Programm": "programme",
                               "Ausschreibung": "bidding",
                               "Projektstart": "project_start",
                               "Projektende": "project_end",
                               "Projektstatus": "status",
                               "Keywords": "keywords",
                               "Rolle im Projekt": "role_in_project",
                               "Organisationsname": "organisation_name",
                               "Organisationsart": "organisation_type",
                               "Website": "website",
                               "Staat": "country",
                               "Bundesland": "state",
                               "Stadt": "city",
                               "Adresse (Office)": "address",
                           }),
            StepUserConfig("PROJECT_COLUMNS",
                           LocalisationString("Columns containing project data", "Spalten mit Projektdaten"),
                           StepUserConfig.StepUserConfigType.LIST, ["id",
                                                                    "short_title",
                                                                    "long_title",
                                                                    "abstract",
                                                                    "programme",
                                                                    "bidding",
                                                                    "project_start",
                                                                    "project_end",
                                                                    "status",
                                                                    "keywords", ]),
            StepUserConfig("PROJECT_COLUMNS_ONLY_ON_FIRST_INSTANCE",
                           LocalisationString("Columns containing project data only once",
                                              "Spalten mit Prjektdaten nur einmal vorhanden"),
                           StepUserConfig.StepUserConfigType.LIST, ["abstract"]),
            StepUserConfig("ORGANISATION_COLUMNS",
                           LocalisationString("Columns with organisation data", "Zeilen mit Organisationsdaten"),
                           StepUserConfig.StepUserConfigType.LIST,
                           ["role_in_project",
                            "organisation_name",
                            "organisation_type",
                            "website",
                            "country",
                            "state",
                            "city",
                            "address"]),
            StepUserConfig("ORGANISATIONS_COLUMN_NAME",
                           LocalisationString("Organisations column", "Organistionsspalte"),
                           StepUserConfig.StepUserConfigType.STRING, "organisations"),
        ]

    def name(self) -> str:
        return 'getDataFFG'

    def display_name(self) -> str:
        return LocalisationString("Get Data from FFG", "Daten von FFG laden")

    def description(self) -> str:
        return LocalisationString("Desc", "Desc")

    def dependencies(self) -> Union[List[str], None]:
        return None


class DummyStep(StepConfig):
    async def run(self, _):
        yield 'Dummy Step executed', EventType.INFO

    def name(self) -> str:
        return 'dummyStep'

    def display_name(self):
        return LocalisationString("Dummy Step", "Dummy Step")

    def dependencies(self) -> Union[List[str], None]:
        return ['getDataFFG']


DEMO_PIPELINE = PipelineConfig(
    name='scraper_main',
    display_name=LocalisationString("Scraper Pipeline", "Scraper Pipeline"),
    steps=[FFPScraper(), DummyStep()],
    parallelize=True
)
