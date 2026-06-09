from ._anvil_designer import Statistics_PageTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

currentuser = anvil.users.get_user()
class Statistics_Page(Statistics_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)
    
    if anvil.server.call('tutor_perms'):
      self.tutor_redirect.visible = True
      
  

  @handle("score_plot", "show")
  def score_plot_show(self, **event_args):
    """This method is called when the Plot is shown on the screen"""
    xdata = []
    ydata = []
    for row in app_tables.finishedhomeworkfiles.search():
      if row['Uploader'] != currentuser: continue
      if row['Marks'] is None: continue
      xdata.append(str(row['Homework_Title']))
      markgiven = int(row['Marks'])
      tmarkrow = app_tables.homeworkfiles.get(Homework_Title=row['Homework_Title'])
      totalmarks = int(tmarkrow["Total_Marks"])
      percentage = round(markgiven/totalmarks, 1) * 100
      ydata.append(str(percentage) + "%")
    if xdata is not None and ydata is not None:
      self.score_plot.data = [
        go.Scatter(
          x = xdata,
          y = ydata,
          marker = dict(color= 'rgb(155, 155, 0)')
        )
      ]

  @handle("flow_panel_1", "show")
  def flow_panel_1_show(self, **event_args):
    """This method is called when the FlowPanel is shown on the screen"""
    #Work returned KPI
    currentuserhwdata = app_tables.homework.get(Student=currentuser)
    self.Homework_Returned.text = "Homework Returned: " + str(currentuserhwdata['Work Returned'])

    #Average mark KPI
    marklist = 0
    totalwork = 0
    for row in app_tables.finishedhomeworkfiles.search():
      if row['Uploader'] != currentuser: continue
      if row['Marks'] is None: continue
      markgiven = int(row['Marks'])
      tmarkrow = app_tables.homeworkfiles.get(Homework_Title=row['Homework_Title'])
      totalmarks = int(tmarkrow["Total_Marks"])
      percentage = round(markgiven/totalmarks, 1) * 100
      marklist += percentage
      totalwork+=1
    
    if totalwork!= 0: marklist/=totalwork
    else: marklist = 0
    currentuserhwdata['Average Mark'] = marklist
    self.Average_Mark_KPI.text = "Average Mark: " + str(marklist) + "%"

    #Homework Completion Rate KPI
    homeworklistrow = app_tables.homework.get(Student=currentuser)
    total = homeworklistrow["Work Due Soon"] + homeworklistrow["Work Overdue"] + homeworklistrow["Work Pending Marks"] + homeworklistrow["Work Returned"]
    uncompleted = homeworklistrow['Work Overdue']
    completed = total - uncompleted
    if total != 0:
      completionrate = completed/total * 100
    else: completionrate = 0
    self.Homework_Completion_Rate_KPI.text = "Homework Completion Rate: " + str(round(completionrate,2)) + "%"

    #Rank
    rank = 1
    for row in app_tables.homework.search():
      if row['Average Mark'] > currentuserhwdata['Average Mark']: rank +=1
    self.Class_Rank_KPI.text = "Class Rank: " + str(rank)

    
  @handle("Logout_Button", "click")
  def Logout_Button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('LogIn_Page')

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