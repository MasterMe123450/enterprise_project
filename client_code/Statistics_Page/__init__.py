from ._anvil_designer import Statistics_PageTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Statistics_Page(Statistics_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)

    # Any code you write here will run before the form opens.
  

  
  
  
  
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

  @handle("score_plot", "show")
  def score_plot_show(self, **event_args):
    """This method is called when the Plot is shown on the screen"""
    xdata = []
    ydata = []
    for row in app_tables.finishedhomeworkfiles.search():
      xdata.append(str(row['Homework_Title']))
      markgiven = int(row['Marks'])
      theotherrow = app_tables.homeworkfiles.get(Homework_Title=row['Homework_Title'])
      totalmarks = int(theotherrow["Total_Marks"])
      percentage = round(markgiven/totalmarks, 1)
      ydata.append(percentage)
    if xdata is not None and ydata is not None:
      self.score_plot.data = [
        go.Scatter(
          x = xdata,
          y = ydata,
          marker = dict(color= 'rgb(16, 32, 77)'), x0=1, dx=1
        )
      ]
