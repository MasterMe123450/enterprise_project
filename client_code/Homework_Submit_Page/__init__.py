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

    
    


    
  

    

  @handle("homework_dropdown", "show")
  def homework_dropdown_show(self, **event_args):
    """This method is called when the DropDown is shown on the screen"""
    worksheetlist = [""]
    for row in app_tables.homeworkfiles.search():
     worksheetlist.append(row["Homework_Title"])
    self.homework_dropdown.items = worksheetlist

    

  @handle("doohickey", "click")
  def doohickey_click(self, **event_args):
    """This method is called when the button is clicked"""
    #FILE UPLOAD
    upload_row = app_tables.finishedhomeworkfiles.add_row()
    upload_row['Homework_File'] = self.Homework_Upload.file
    upload_row['Homework_Title'] = self.Homework_Upload.file.name
    print(upload_row['Homework_Title'])
    upload_row['Uploader'] = anvil.users.get_user()

    date = datetime.now()
    upload_row['Upload Date'] = date

    #TITLE
    upload_row['Homework_Title'] = self.file_name_input.text

    #SELECTED 
    uploadtitle = self.homework_dropdown.selected_value
    print(uploadtitle)
    upload_row['Homework_Title'] = uploadtitle
    cuser = anvil.users.get_user()
    hwlistrow = app_tables.homework.get(Student=cuser)
    print(hwlistrow)
    hwlist = hwlistrow["Homework_List"]
    hwlist[uploadtitle] = 1
    print(hwlist)
    hwlistrow['Homework_List'] = hwlist

    
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

    
    
    
