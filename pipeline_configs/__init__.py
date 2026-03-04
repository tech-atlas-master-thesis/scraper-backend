from typing import List

from pipelineFramework.server.pipeline.config import PipelineConfig
from pipeline_configs.test import TEST_PIPELINE
from pipeline_configs.scraper_main import DEMO_PIPELINE

PIPELINE_CONFIGS: List[PipelineConfig] = [TEST_PIPELINE, DEMO_PIPELINE]
