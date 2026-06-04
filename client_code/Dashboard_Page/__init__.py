from ._anvil_designer import Dashboard_PageTemplate
from anvil import *
from datetime import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users

class Dashboard_Page(Dashboard_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)
    #check and give special tutor access 
    if anvil.server.call('tutor_perms'):
      self.tutor_redirect.visible = True

    #Top dashboard summary info
    #get the user hwtables
    currentuser = anvil.users.get_user()
    currentuserhwdata = app_tables.homework.get(Student=currentuser)
    hwlist = currentuserhwdata["Homework_List"]
    #count the number of submissions and overdue
    notdonecounter = 0
    overduecounter = 0
    donecounter = 0
    returnedcounter = 0
    #first, check if true, if it is, the work is done!
    
    if hwlist is None: return #THIS IS JUST SO WHEN TESTING/EXCEPTION IT DOESN'T THROW AN ERROR
    for key, value in hwlist.items():
      if value == 1:
        donecounter +=1
      elif value == 2:
        returnedcounter +=1        
      else: #buuuuuut, if its false, check its date to see if its upcoming or overdue
        hwdd = app_tables.homeworkfiles.get(Homework_Title=key)
        duedate = hwdd['Due_Date']
        currentdate = datetime.now(timezone.utc)
        if duedate < currentdate:
          overduecounter+=1
        else:
          notdonecounter+=1

    
    currentuserhwdata['Work Overdue'] = overduecounter
    currentuserhwdata['Work Pending Marks'] = donecounter
    currentuserhwdata['Work Due Soon'] = notdonecounter
    currentuserhwdata['Work Returned'] = returnedcounter
    #each text box displays data
    if currentuserhwdata["Work Returned"] > 1:
      self.Homework_Returned.text = str(currentuserhwdata["Work Returned"]) + " tasks returned!"
    else:
       self.Homework_Returned.text = str(currentuserhwdata["Work Returned"]) + " task returned!"

    if currentuserhwdata["Work Overdue"] > 1:
      self.Homework_Overdue.text = str(currentuserhwdata["Work Overdue"]) + " tasks overdue!"
    else:
      self.Homework_Overdue.text = str(currentuserhwdata["Work Overdue"]) + " task overdue!"

    if currentuserhwdata["Work Due Soon"]  > 1:
      self.Homework_Due_Soon.text = str(currentuserhwdata["Work Due Soon"]) + " tasks due soon!"
    else:
      self.Homework_Due_Soon.text = str(currentuserhwdata["Work Due Soon"]) + " task due soon!" 

    if currentuserhwdata["Work Pending Marks"]  > 1:
      self.Homework_Pending.text = str(currentuserhwdata["Work Pending Marks"]) + " tasks pending!"
    else:
      self.Homework_Pending.text = str(currentuserhwdata["Work Pending Marks"]) + " task pending!"
      
    #Change colour of overdue label if there is work to be done!
    if currentuserhwdata["Work Overdue"] > 0:
      self.Homework_Overdue.background = "crimson"
    if currentuserhwdata["Work Returned"]>0:
      self.Homework_Returned.background = "#90EE90"
    #Displays a preview of the lastest things uploaded
    #maybe max of 3?
    dbcap = 3
    dbcount = 1
    for row in app_tables.homeworkfiles.search():
      if dbcount > dbcap: return #if at cap do not show
        
      donecheckrow = app_tables.homework.get(Student=currentuser)
      donechecklist = donecheckrow['Homework_List']
      hwtitle = row['Homework_Title']
      donecheck = donechecklist[hwtitle]
      if donecheck != 0: continue #if done do not show
      self.templbl2.visible = False
      self.Work_Preview.add_component(Label(text= "Homework Task: " + row["Homework_Title"], align="center"))
      date = str(row["Due_Date"])
      shortdate = date.split(" ") #space to omit time, + to include time
      self.Work_Preview.add_component(Label(text="Due: " +shortdate[0], align="center"))
      self.Work_Preview.add_component(Link(url=row["Homework_File"], align="center",text="Download"))
      dbcount += 1
    
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

  @handle("Homework_Returned_Container", "show")
  def Homework_Returned_Container_show(self, **event_args):
    """This method is called when the FlowPanel is shown on the screen"""
    for row in app_tables.homeworkfiles.search():
      currentuser = anvil.users.get_user()
      donecheckrow = app_tables.homework.get(Student=currentuser)
      donechecklist = donecheckrow['Homework_List']
      hwtitle = row['Homework_Title']
      donecheck = donechecklist[hwtitle]
      if donecheck != 2: continue #if not done do not show
      self.templbl.visible = False
      markedrow = app_tables.finishedhomeworkfiles.get(Homework_Title=hwtitle, Uploader=currentuser)
      self.Homework_Returned_Container.add_component(Label(text= "Homework Task Returned: " + hwtitle, align= "center"))
      self.Homework_Returned_Container.add_component(Link(url = markedrow["Marked_File"], align="center",text="Download Marked Work"))
      self.Homework_Returned_Container.add_component(Label(text="Check the homework page to see your total mark.", align="center"))