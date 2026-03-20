from pipelineFramework import LocalisationString, PipelineConfig
from pipeline_configs.FFG_steps.ffg_scraper import FFPScraper
from pipeline_configs.dummy_step_factory import get_dummy_step

DEMO_PIPELINE = PipelineConfig(
    type="scraper_main",
    display_name=LocalisationString("Scraper Pipeline", "Scraper Pipeline"),
    steps=[
        FFPScraper(),
        get_dummy_step(
            "getDataFWF",
            LocalisationString("[DUMMY_STEP] Get Data from FWF", "[DUMMY_STEP] Daten von FWF laden"),
        ),
    ],
    parallelize=True,
)
