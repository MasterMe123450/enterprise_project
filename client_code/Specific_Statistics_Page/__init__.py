from ._anvil_designer import Specific_Statistics_PageTemplate
from anvil import *
import plotly.graph_objects as go
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
    marklist = []
    self.data_grid_1.visible = True
    self.Distribution_Plot.visible = True
    self.flow_panel_1.visible = True

    #The marklist(tm)
    for row in app_tables.finishedhomeworkfiles.search():
      if row['Homework_Title'] == self.Selection_Dropdown.selected_value:
        userrow = row['Uploader']
        user = userrow['email']
        if anvil.server.call('remove_tutors', user): continue
        contentdict = {}
        user = row['Uploader']
        contentdict["Uploader"] = user['Name']
        contentdict["Marks"] = row['Marks']
        marklist.append(row['Marks'])
        tablecontents.append(contentdict)
    tablecontents.sort(key=lambda contentdict: contentdict["Marks"], reverse=True)
    self.repeating_panel_1.items = tablecontents

    #The KPIs
    marklist.sort()
    averagemark = 0
    if len(marklist) == 0:
      print("This task does not exist!
    else:
      for i in marklist:
        averagemark += i
      averagemark/=len(marklist)
      if len(marklist) % 2 == 0:
        index = len(marklist)/2 
        medianmark = marklist[int(index)]
        index = len(marklist)/2 - 1 
        medianmark += marklist[int(index)]
        medianmark /= 2
      elif len(marklist) != 1:
        index = len(marklist)/2 - 0.5
        medianmark = marklist[int(index)]
      else:
        medianmark = marklist[0]
      self.n_KPI.text = "Number of Students: " + str(len(marklist))
      self.Average_Mark_KPI.text = "Average Mark: " + str(round(averagemark,2))
      self.Median_KPI.text = "Median Mark: " + str(medianmark)
      modecheck = 0
      for mark in marklist:
        if mark == max(set(marklist), key = marklist.count):
          modecheck +=1
      if modecheck > 1:
        self.Mode_KPI.text= "Mode: " + str(max(set(marklist), key = marklist.count))
      else:
        self.Mode_KPI.text= "Mode: No Mode" 
  
      #The distribution plot
      self.Distribution_Plot.data = [
        go.Box(x = marklist)
      ]
    
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

  @handle("Logout_Button", "click")
  def Logout_Button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('LogIn_Page')

