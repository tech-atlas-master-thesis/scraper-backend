from pipelineFramework import LocalisationString, PipelineConfig, GetConfiguration, get_dummy_step
from pipeline_configs.FFG_steps.ffg_scraper import FFPScraper

DEMO_PIPELINE = PipelineConfig(
    type="scraper_main",
    display_name=LocalisationString("Scraper Pipeline", "Scraper Pipeline"),
    steps=[
        GetConfiguration(
            "technologies",
            "getTechnologyConfiguration",
            LocalisationString("Get Technology Configuration", "Technologie Konfiguration Laden"),
            LocalisationString("Desc", "Desc"),
            LocalisationString("Technology Configuration", "Technologie Konfiguration"),
        ),
        FFPScraper(),
        get_dummy_step(
            "getDataFWF",
            LocalisationString("[DUMMY_STEP] Get Data from FWF", "[DUMMY_STEP] Daten von FWF laden"),
        ),
    ],
    parallelize=True,
)
