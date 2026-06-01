from ._anvil_designer import LogIn_PageTemplate
from anvil import *


class LogIn_Page(LogIn_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)

    # Any code you write here will run before the form opens.
