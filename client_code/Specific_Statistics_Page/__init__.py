from ._anvil_designer import Specific_Statistics_PageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
import operator
from anvil.tables import app_tables


class Specific_Statistics_Page(Specific_Statistics_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)
    if anvil.server.call('tutor_perms'):
      self.tutor_redirect.visible = True
    # Any code you write here will run before the form opens.



  @handle("Load_Button", "click")
  def Load_Button_click(self, **event_args):
    """This method is called when the button is clicked"""
    tablecontents = []
    for row in app_tables.finishedhomeworkfiles.search():
      if row['Homework_Title'] == self.Selection_Dropdown.selected_value:
        contentdict = {}
        user = row['Uploader']
        contentdict["Uploader"] = user['Name']
        contentdict["Marks"] = row['Marks']
        tablecontents.append(contentdict)
    tablecontents.sort(key=lambda contentdict: contentdict["Marks"], reverse=True)
    self.repeating_panel_1.items = tablecontents

  @handle("Selection_Dropdown", "show")
  def Selection_Dropdown_show(self, **event_args):
    """This method is called when the DropDown is shown on the screen"""
    worklist = []
    for row in app_tables.homeworkfiles.search():
      worklist.append(row['Homework_Title'])
    self.Selection_Dropdown.items = worklist

  
  @handle("dashboard_redirect", "click")
  def dashboard_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Dashboard_Page')

  @handle("tutor_redirect", "click")
  def tutor_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form(('Tutor_Page'))

  @handle("homework_redirect", "click")
  def homework_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Homework_Page')

  @handle("worksheet_redirect", "click")
  def worksheet_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Worksheet_Page')

  @handle("statistics_redirect", "click")
  def statistics_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Statistics_Page')

  @handle("Statistics_Redirect2", "click")
  def Statistics_Redirect2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Statistics_Page')

