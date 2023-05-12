from .catalog import handlers as catalog_handlers
from .start import handlers as start_handlers
from .account import handlers as account_handlers

handlers = start_handlers + catalog_handlers + account_handlers
