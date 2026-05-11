from pipelineFramework import LocalisationString, PipelineConfig
from pipeline_configs.FFG_steps.ffg_scraper import FFPScraper
from pipelineFramework import get_dummy_step
from pipeline_configs.tech_config import TechConfigStep

DEMO_PIPELINE = PipelineConfig(
    type="scraper_main",
    display_name=LocalisationString("Scraper Pipeline", "Scraper Pipeline"),
    steps=[
        TechConfigStep(),
        FFPScraper(),
        get_dummy_step(
            "getDataFWF",
            LocalisationString("[DUMMY_STEP] Get Data from FWF", "[DUMMY_STEP] Daten von FWF laden"),
        ),
    ],
    parallelize=True,
)
