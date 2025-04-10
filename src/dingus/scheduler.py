"""scheduler.py

This module handles the scheduling of periodic tasks.
"""

import asyncio
import logging
from datetime import datetime, timedelta

from dingus.llm_clients import OpenAIChatClient
from dingus.settings import KUBE_CONFIG_PATH
from dingus.tools.k8 import KubernetesClient
from dingus.tools.report_generator import LogReportGenerator

logger = logging.getLogger(__name__)


class ReportScheduler:
    def __init__(self, report_generator: LogReportGenerator):
        self.report_generator = report_generator
        self._task = None
        self._running = False

    async def start(self):
        """Start the hourly report generation scheduler."""
        if self._running:
            logger.warning("Scheduler is already running")
            return

        self._running = True
        self._task = asyncio.create_task(self._run_scheduler())
        logger.info("Report scheduler started")

    async def stop(self):
        """Stop the scheduler."""
        if not self._running:
            logger.warning("Scheduler is not running")
            return

        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Report scheduler stopped")

    async def _run_scheduler(self):
        """Run the scheduler loop."""
        while self._running:
            try:
                # Generate report
                report = self.report_generator.generate_report()
                logger.info(f"Generated report at {datetime.now()}")

                # TODO: Store report in database or send to notification system

                # Wait for next hour
                await asyncio.sleep(3600)  # 1 hour in seconds
            except Exception as e:
                logger.error(f"Error in scheduler: {e}")
                await asyncio.sleep(60)  # Wait 1 minute before retrying


def get_report_scheduler() -> ReportScheduler:
    """Get or create a ReportScheduler instance."""
    if not hasattr(get_report_scheduler, "instance"):
        openai_client = OpenAIChatClient()
        kube_client = KubernetesClient(kube_config_path=KUBE_CONFIG_PATH)
        report_generator = LogReportGenerator(openai_client, kube_client)
        get_report_scheduler.instance = ReportScheduler(report_generator)
    return get_report_scheduler.instance
