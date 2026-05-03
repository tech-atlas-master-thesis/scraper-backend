import pandas as pd
import pytest

from pipelineFramework import EventType
from pipelineFramework.tests.test_helper import get_default_user_config
from pipeline_configs.FFG_steps.ffg_scraper import FFPScraper


@pytest.mark.asyncio
async def test_steps_full_data():
    results = {}

    ffg_step = FFPScraper()
    RESULT_STEP_INDEX = 3

    i = 0
    async for event, event_type in ffg_step.run(get_default_user_config(ffg_step)):
        if i == RESULT_STEP_INDEX:
            with open("./tests/results/scrape_ffg_small_data.csv", "r", newline="\n") as f:
                assert event_type == EventType.RESULT
                assert f.read() == event.to_csv(index=False)
            results["getDataFFG"] = event
        else:
            assert event_type == EventType.INFO
        i += 1
