from ._anvil_designer import LogIn_PageTemplate
from anvil import *
from anvil import tableau
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users


class LogIn_Page(LogIn_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)
    anvil.users.login_with_form()
    if anvil.users.get_user() is not None:
      currentuser = anvil.users.get_user()
      currentuserhwdata = app_tables.homework.get(Student=currentuser)
      if currentuserhwdata is None:
        app_tables.homework.add_row(Student=currentuser)
      open_form('Dashboard_Page')
      
    else: 
      anvil.users.login_with_form()
    # Any code you write here will run before the form opens.
