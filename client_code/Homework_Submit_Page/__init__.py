from ._anvil_designer import Homework_Submit_PageTemplate
from anvil import *
import anvil.server
from datetime import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Homework_Submit_Page(Homework_Submit_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)
    
    if anvil.server.call('tutor_perms'):
      self.tutor_redirect.visible = True
    # Any code you write here will run before the form opens.

    
    

  @handle("Homework_Upload", "change")
  def Homework_Upload_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    upload_row = app_tables.finishedhomeworkfiles.add_row()
    upload_row['Homework_File'] = self.Homework_Upload.file
    upload_row['Homework_Title'] = self.Homework_Upload.file.name
    upload_row['Uploader'] = anvil.users.get_user()
    
    date = datetime.now()
    upload_row['Upload Date'] = date
  
  @handle("file_name_input", "pressed_enter")
  def file_name_input_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    upload_row = app_tables.finishedhomeworkfiles.get(Homework_Title = self.Homework_Upload.file.name)
    upload_row['Homework_Title'] = self.file_name_input.text

  @handle("homework_dropdown", "show")
  def homework_dropdown_show(self, **event_args):
    """This method is called when the DropDown is shown on the screen"""
    worksheetlist = [""]
    for row in app_tables.homeworkfiles.search():
     worksheetlist.append(row["Homework_Title"])
    self.homework_dropdown.items = worksheetlist

  @handle("homework_dropdown", "change")
  def homework_dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    upload_row = app_tables.finishedhomeworkfiles.get(Homework_Title = self.Homework_Upload.file.name)
    uploadtitle =  self.homework_dropdown.selected_value
    upload_row['Homework_Title'] = uploadtitle
    cuser = anvil.users.get_user()
    hwlistrow = app_tables.homework.get(Student=cuser)
    print(hwlistrow)
    hwlist = hwlistrow["Homework_List"]
    hwlist[uploadtitle] = True
    print(hwlist)
    hwlistrow['Homework_List'] = hwlist
    

  @handle("doohickey", "click")
  def doohickey_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.feedback_label.visible = True

  #Sidebar Navigation
  @handle("homework_redirect", "click")
  def homework_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Homework_Page')

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

    
    
    
