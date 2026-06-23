
from ._anvil_designer import Tutor_PageTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
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
    if hwrow is None:
      return
    for row in app_tables.homeworkfiles.search(): 
      if row == hwrow:
        row.delete()
    for row in app_tables.finishedhomeworkfiles.search():
      if row["Homework_Title"] == hwrow['Homework_Title']:
        row.delete()
    for row in app_tables.homework.search():
      hwlist = row['Homework_List']
      if hwrow in hwlist:
        hwlist.pop(hwrow['Homework_Title'])
        row['Homework_List'] = hwlist

  
  @handle("doohickey_button", "click")
  def doohickey_button_click(self, **event_args):
    #File Upload
    if self.file_loader_1.file is None or self.file_loader_1.file.name is None: 
      self.errorlbl.visible = True
      return
    hwrow = app_tables.homeworkfiles.add_row(Homework_File=self.file_loader_1.file, Homework_Title=self.file_loader_1.file.name)
    phwrow = app_tables.permanenthomeworkfiles.add_row(Worksheet_File= self.file_loader_1.file)
    #When there is a file in the file upload, and a date in the textbox, it adds/changes a duedate for that file
    duedate = self.DueDateInput.text
    duedateformat = datetime.strptime(duedate, "%d-%m-%Y")
    hwrow["Due_Date"] = duedateformat
    self.upload_feedback.visible = True
    hwrow["Homework_Title"] = self.file_name_input.text 
    if self.file_name_input.text is  None: self.file_name_input_feedback.text = "The work has been uploaded with no title"
    self.file_name_input_feedback.visible = True
    phwrow["Worksheet_Title"] = self.file_name_input.text
    if self.marks_input.text is not None: hwrow['Total_Marks'] = int(self.marks_input.text)
    if self.marks_input.text is None:self.mark_input_feedback.text = "The work has been uploaded with no mark. If this was not your intention, delete the file and try again"
    self.mark_input_feedback.visible = True
    hwrow['Topic'] = self.Topic_Dropdown.selected_value
    if self.Topic_Dropdown.selected_value == "mixed":
      topicbreakdown = {}
      topic1 = self.topic_dropdown_1.selected_value
      topic1marks = self.topic1_markinput.text
      topic2 = self.topic_dropdown_2.selected_value
      topic2marks = self.topic2_markinput.text
      if topic1 is None or topic2 is None or topic1marks is None or topic2marks is None:
        self.topic_input_feedback.text = "Missing values in topic selection. The work has been uploaded with no topic."
      else:
        topicbreakdown[topic1] = topic1marks
        topicbreakdown[topic2] = topic2marks
        hwrow['Topics_Marks'] = topicbreakdown
    if self.Topic_Dropdown.selected_value is None: self.topic_input_feedback.text = "The work has been uploaded with no topic"
    self.topic_input_feedback.visible = True
    for row in app_tables.homework.search():
      if row["Homework_List"] is None:
        row['Homework_List'] = {}
      #idk why you have to write the data in this stupid fucking way but it works so im not changing it  
      newname = hwrow["Homework_Title"]
      currentlist = row["Homework_List"]
      #0 for not done,1 for submitted, 2 for returned
      currentlist[newname] = 0
      row['Homework_List'] = currentlist
    self.send_feedback.visible = True
    

  @handle("topic_adder", "pressed_enter")
  def topic_adder_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    app_tables.topics.add_row(Topic=self.topic_adder.text)

  @handle("Topic_Dropdown", "show")
  def Topic_Dropdown_show(self, **event_args):
    """This method is called when the DropDown is shown on the screen"""
    topics = []
    for row in app_tables.topics.search():
      topics.append(row["Topic"])
    self.Topic_Dropdown.items = topics

  @handle("Topic_Dropdown", "change")
  def Topic_Dropdown_change(self, **event_args):
    """This method is called when an item is selected"""
    if self.Topic_Dropdown.selected_value == "mixed":
      self.topic_dropdown_1.visible = True
      self.topic1lbl1_1.visible = True
      self.topiclbl1_2.visible = True
      self.topic1_markinput.visible = True
      self.topic_dropdown_2.visible = True
      self.topiclbl2_1.visible = True
      self.topiclbl2_2.visible = True
      self.topic2_markinput.visible = True
    else:
      self.topic_dropdown_1.visible = False
      self.topic1lbl1_1.visible = False
      self.topiclbl1_2.visible = False
      self.topic1_markinput.visible = False
      self.topic_dropdown_2.visible = False
      self.topiclbl2_1.visible = False
      self.topiclbl2_2.visible = False
      self.topic2_markinput.visible = False

  @handle("topic_dropdown_1", "show")
  def topic_dropdown_1_show(self, **event_args):
    """This method is called when the DropDown is shown on the screen"""
    topics = []
    for row in app_tables.topics.search():
      topics.append(row["Topic"])
    topics.remove("mixed")
    self.topic_dropdown_1.items = topics

  @handle("topic_dropdown_1", "show")
  def topic_dropdown_2_show(self, **event_args):
    """This method is called when the DropDown is shown on the screen"""
    topics = []
    for row in app_tables.topics.search():
      topics.append(row["Topic"])
    topics.remove("mixed")
    self.topic_dropdown_2.items = topics


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

  @handle("worksheet_redirect", "click")
  def worksheet_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Worksheet_Page')
    
  @handle("Marking_Redirect", "click")
  def Marking_Redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Tutor_Marking_Page')

  @handle("statistics_redirect", "click")
  def statistics_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Statistics_Page')




  



