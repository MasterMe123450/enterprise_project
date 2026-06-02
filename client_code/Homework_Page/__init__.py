from ._anvil_designer import Homework_PageTemplate
from anvil import *
import anvil.server
from datetime import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Homework_Page(Homework_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)
    if anvil.server.call('tutor_perms'):
      self.tutor_redirect.visible = True
    # Any code you write here will run before the form opens.

  @handle("dashboard_redirect", "click")
  def dashboard_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Dashboard_Page')

  @handle("tutor_redirect", "click")
  def tutor_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Tutor_Page')

  @handle("Logout_Button", "click")
  def Logout_Button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('LogIn_Page')

  @handle("Homework_Upload", "change")
  def Homework_Upload_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    upload_row = app_tables.finishedhomeworkfiles.add_row()
    upload_row['Homework_File'] = self.Homework_Upload.file
   
    upload_row['Uploader'] = anvil.users.get_user()
    
    date = datetime.datetime.now()
    upload_row['Upload Date'] = date
    
