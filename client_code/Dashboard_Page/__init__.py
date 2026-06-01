from ._anvil_designer import Dashboard_PageTemplate
from anvil import *
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
    currentuser = anvil.users.get_user()
    currentuserhwdata = app_tables.homework.get(Student=currentuser)
  
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

  @handle("Logout_Button", "click")
  def Logout_Button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('LogIn_Page')
