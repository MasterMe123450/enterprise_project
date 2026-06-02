from ._anvil_designer import Tutor_PageTemplate
from anvil import *
from datetime import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Tutor_Page(Tutor_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)
    if anvil.server.call('tutor_perms'):
      self.tutor_redirect.visible = True
    # Any code you write here will run before the form opens.

  #File Upload
  @handle("file_loader_1", "change")
  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    app_tables.homeworkfiles.add_row(Homework_File=file, Homework_Title=file.name)

#When there is a file in the file upload, and a date in the textbox, it adds/changes a duedate for that file
  @handle("DueDateInput", "pressed_enter")
  def DueDateInput_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    hwrow = app_tables.homeworkfiles.get(Homework_Title = self.file_loader_1.file.name)
    duedate = self.DueDateInput.text
    duedateformat = datetime.strptime(duedate, "%d-%m-%Y")
    hwrow["Due_Date"] = duedateformat
    self.upload_feedback.visible = True

  #Redirects to the dashboard page
  @handle("dashboard_redirect", "click")
  def dashboard_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Dashboard_Page')  # Write Code Here

  #logs the user out
  @handle("Logout_Button", "click")
  def Logout_Button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('LogIn_Page')

  @handle("file_name_input", "pressed_enter")
  def file_name_input_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    hwrow = app_tables.homeworkfiles.get(Homework_Title = self.file_loader_1.file.name)
    hwrow["Homework_Title"] = self.file_name_input.text 
    self.file_name_input_feedback.visible = True

  @handle("delete_button", "click")
  def delete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    hwrow = app_tables.homeworkfiles.get(Homework_Title = self.file_name_input.text)
    for row in app_tables.homeworkfiles.search(): 
      if row == hwrow:
        row.delete()

  @handle("homework_redirect", "click")
  def homework_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Homework_Submit_Page')
