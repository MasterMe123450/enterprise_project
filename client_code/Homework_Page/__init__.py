from ._anvil_designer import Homework_PageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Homework_Page(Homework_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)

    if anvil.server.call('tutor_perms'):
      self.tutor_redirect.visible = True
    
    # Any code you write here will run before the form opens.

  @handle("dashboard_redirect", "click")
  def dashboard_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Dashboard_Page')

  @handle("tutor_redirect", "click")
  def tutor_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Tutor_Page")

  @handle("Logout_Button", "click")
  def Logout_Button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('LogIn_Page')

  @handle("Homework_Container", "show")
  #NOT DONE
  def Homework_Container_show(self, **event_args):
    """This method is called when the FlowPanel is shown on the screen"""
    for row in app_tables.homeworkfiles.search():
      currentuser = anvil.users.get_user()
      donecheckrow = app_tables.homework.get(Student=currentuser)
      donechecklist = donecheckrow['Homework_List']
      hwtitle = row['Homework_Title']
      donecheck = donechecklist[hwtitle]
      if donecheck != 0: continue #if done do not show
        
      xyp = XYPanel(width=250, height=250, border="solid 1px")
      self.Homework_Container.add_component(xyp)
      
      titlelbl = Label(text = row["Homework_Title"],align = "center")
      xyp.add_component(titlelbl, x=20, y=10)

      dd = str(row['Due_Date']) 
      dd = dd.split(" ")
      ddlbl = Label(text = "Due: " + str(dd[0]), align="center")
      xyp.add_component(ddlbl, x=20, y=30)

      btn = Button(text="Submit", align="right", background="#EADDFF")
      btn.set_event_handler('click', self.redirect)
      xyp.add_component(btn, x=10, y=200)
      
      dlink = Link(text="Download", align = "left", url=row['Homework_File'])
      xyp.add_component(dlink, x=150, y=202)


  #DONE
  @handle("Homework_Complete_Container", "show")
  def Homework_Complete_Container_show(self, **event_args):
    """This method is called when the FlowPanel is shown on the screen"""
    for row in app_tables.homeworkfiles.search():
      currentuser = anvil.users.get_user()
      donecheckrow = app_tables.homework.get(Student=currentuser)
      donechecklist = donecheckrow['Homework_List']
      hwtitle = row['Homework_Title']
      donecheck = donechecklist[hwtitle]
      if donecheck != 1: continue #if not done do not show

      xyp = XYPanel(width=250, height=250, border="solid 1px")
      self.Homework_Complete_Container.add_component(xyp)

      titlelbl = Label(text = row["Homework_Title"],align = "center")
      xyp.add_component(titlelbl, x=20, y=10)

      dd = str(row['Due_Date']) 
      dd = dd.split(" ")
      ddlbl = Label(text = "Due: " + str(dd[0]), align="center")
      xyp.add_component(ddlbl, x=20, y=30)

      clbl = Label(text = "Congrats!", align= "center")
      xyp.add_component(clbl, x=20, y=202)
      
      dlink = Link(text="Download", align = "left", url=row['Homework_File'])
      xyp.add_component(dlink, x=150, y=202)





  def redirect(self, **event_args):
    open_form('Homework_Submit_Page')