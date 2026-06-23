from ._anvil_designer import Worksheet_PageTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Worksheet_Page(Worksheet_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)
    if anvil.server.call('tutor_perms'):
      self.tutor_redirect.visible = True
      self.tutor_lbl.visible = True
      self.worksheet_file_loader.visible = True
      self.delete_button.visible = True
      self.delete_textbox.visible = True
      self.tutor_upload.visible = True
    # Any code you write here will run before the form opens.



  @handle("worksheet_container", "show")
  def worksheet_container_show(self, **event_args):
    """This method is called when the FlowPanel is shown on the screen"""
    for row in app_tables.permanenthomeworkfiles.search():
      xyp = XYPanel(width=250, height=250, border="solid 2px")
      self.worksheet_container.add_component(xyp)

      titlelbl = Label(text = row["Worksheet_Title"],align = "center")
      xyp.add_component(titlelbl, x=20, y=10)

      dlink = Link(text="Download", align = "left", url=row['Worksheet_File'])
      xyp.add_component(dlink, x=93+8/11, y=202)
  
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

  @handle("tutor_redirect", "click")
  def tutor_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Tutor_Page')

  @handle("worksheet_redirect", "click")
  def worksheet_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Worksheet_Page')

  @handle("statistics_redirect", "click")
  def statistics_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Statistics_Page')
  
  @handle("tutor_upload", "click")
  def tutor_upload_click(self, **event_args):
    """This method is called when the button is clicked"""
    for file in self.worksheet_file_loader.files:
      app_tables.permanenthomeworkfiles.add_row(Worksheet_File=file,Worksheet_Title=file.name)

  @handle("delete_button", "click")
  def delete_button_click(self, **event_args):
    """This method is called when the button is clicked"""
    deletedfilename = self.delete_textbox.text
    for row in app_tables.permanenthomeworkfiles.search():
      if row['Worksheet_Title'] == deletedfilename:
        row.delete()
  
