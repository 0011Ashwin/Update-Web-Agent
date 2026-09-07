import json
import logging
import os

from browser_use.browser.browser import Browser
from browser_use.browser.context import BrowserContext, BrowserContextConfig
from playwright.async_api import Browser as PlaywrightBrowser
from playwright.async_api import BrowserContext as PlaywrightBrowserContext
from typing import Any, Optional

logger = logging.getLogger(__name__)


class CustomBrowserContext(BrowserContext):
    def __init__(
            self,
            browser: 'Browser',
            config: BrowserContextConfig | None = None,
            state: Optional[Any] = None,
    ):
        super(CustomBrowserContext, self).__init__(browser=browser, config=config, state=state)
