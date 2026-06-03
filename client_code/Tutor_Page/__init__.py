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

  


    









  
  @handle("delete_button", "click")
  def delete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    hwrow = app_tables.homeworkfiles.get(Homework_Title = self.file_name_input.text)
    for row in app_tables.homeworkfiles.search(): 
      if row == hwrow:
        row.delete()


  
  @handle("doohickey_button", "click")
  def doohickey_button_click(self, **event_args):
    #File Upload
    hwrow = app_tables.homeworkfiles.add_row(Homework_File=self.file_loader_1.file, Homework_Title=self.file_loader_1.file.name)
    
    #When there is a file in the file upload, and a date in the textbox, it adds/changes a duedate for that file
    duedate = self.DueDateInput.text
    duedateformat = datetime.strptime(duedate, "%d-%m-%Y")
    hwrow["Due_Date"] = duedateformat
    self.upload_feedback.visible = True
    hwrow["Homework_Title"] = self.file_name_input.text 
    hwrow['Total_Marks'] = int(self.marks_input.text) #make this a number check
    for row in app_tables.homework.search():
      if row["Homework_List"] is None:
        row['Homework_List'] = {}
      #idk why you have to write the data in this stupid fucking way but it works so im not changing it  
      newname = hwrow["Homework_Title"]
      currentlist = row["Homework_List"]
      #0 for not done,1 for submitted, 2 for returned
      currentlist[newname] = 0
      row['Homework_List'] = currentlist
    self.file_name_input_feedback.visible = True
  
  #Sidebar Navigation
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
  @handle("homework_redirect", "click")
  def homework_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Homework_Page')

  @handle("Marking_Redirect", "click")
  def Marking_Redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Tutor_Marking_Page')



