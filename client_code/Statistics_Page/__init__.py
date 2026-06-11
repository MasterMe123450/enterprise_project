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
          marker = dict(color= 'rgb(139, 116, 204)')
        )
      ]
      self.score_plot.layout = {
        'xaxis': {
          'title': {'text': 'Task'},
        },
        'yaxis': {
          'title': {'text': 'Average Mark as %'},
          'range': (0,100)
        }
      }


  
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

    #Rank, system literally checks if anyone has a higher average 
    rank = 1
    for row in app_tables.homework.search():
      if row['Average Mark'] > currentuserhwdata['Average Mark']: rank +=1
    self.Class_Rank_KPI.text = "Class Rank: " + str(rank)

  #Show average plot when clicked
  @handle("Show_Average_Plot", "click")
  def Show_Average_Plot_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.score_plot.visible:
      self.score_plot.visible = False
    else:
      self.score_plot.visible = True
  
  #somehow create a topic by topic graph
  @handle("Show_TBT_plot", "click")
  def Show_TBT_plot_click(self, **event_args):
    """This method is called when the button is clicked"""
    #Create topic by topic data
    userhwrow = app_tables.homework.get(Student=currentuser)
    hwlist = userhwrow['Homework_List']
    topiclist = []
    for key in hwlist.keys():
      topic = app_tables.homeworkfiles.get(Homework_Title=key)
      topiclist.append(topic['Topic'])
      if topic['Topic'] == "mixed":
        mixedtopiclist = topic["Topics_Marks"]
        for key in mixedtopiclist.keys():
          topiclist.append(key)
    topics = list(dict.fromkeys(topiclist))
    topicbreakdown = {}
    for topic in topics:
      if topic == "mixed": continue
      topictotal = 0
      totaltasks = 0
      for row in app_tables.homeworkfiles.search():
        #Mixed worksheet
        if row['Topic'] == "mixed":
          mixeddict = row["Topics_Marks"]
          for key in mixeddict.keys():
            if key == topic:
              userhwrow = app_tables.finishedhomeworkfiles.get(Homework_Title=row['Homework_Title'], Uploader=currentuser)
              if userhwrow is not None:
                totalmark = mixeddict[key]
                usermarkdict = userhwrow['Topics_Marks']
                topicmark = usermarkdict[key]
                topictotal += topicmark/totalmark
                totaltasks += 1

        #Single topic worksheet
        if row['Topic'] == topic:
          hwrow = app_tables.finishedhomeworkfiles.get(Homework_Title=row['Homework_Title'], Uploader=currentuser)
          if hwrow is not None:
            if hwrow['Marks'] is not None:
              topicmark = hwrow['Marks']
              totalmarkrow = app_tables.homeworkfiles.get(Homework_Title=hwrow["Homework_Title"])
              totalmark = totalmarkrow["Total_Marks"]
              topictotal += topicmark/totalmark
              print(topicmark/totalmark)
              totaltasks += 1
      if totaltasks != 0:
        topicaverage = topictotal/totaltasks*100
        if topic is not None:
          topicbreakdown[topic] = str(topicaverage) + "%"
        else:
          topicbreakdown["No Topic"] = str(topicaverage) + "%"
    #anything from a "mixed" worksheet that wasn't originally a topic on the topic list is literally just lying just letting you know!

    #Toggle the graph
    if self.TBT_Plot.visible:
      self.TBT_Plot.visible = False
    else:
      self.TBT_Plot.visible = True
      
    #create graph 
    xdata = []
    ydata = []
    for key in topicbreakdown.keys():
      xdata.append(key)
    for value in topicbreakdown.values():
      ydata.append(value)
    print(xdata)
    print(ydata)
    if xdata is not None and ydata is not None:
      self.TBT_Plot.data = [ 
        go.Bar(
          x = xdata,
          y = ydata,
          marker = dict(color= 'rgb(139, 116, 204)')
        )
      ]
      self.TBT_Plot.layout = {
        'xaxis': {
          'title': {'text': 'Topic'},
          
        },
        'yaxis': {
          'title': {'text': 'Average Mark as %'},
          'range': (0,100)
        }
      }


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






