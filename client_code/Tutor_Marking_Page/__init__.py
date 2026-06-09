from ._anvil_designer import Tutor_Marking_PageTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Tutor_Marking_Page(Tutor_Marking_PageTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    super().__init__(**properties)
    if anvil.server.call('tutor_perms'):
      self.tutor_redirect.visible = True
    # Any code you write here will run before the form opens.



  @handle("Homework_Marking_Container", "show")
  def Homework_Marking_Container_show(self, **event_args):
    hwlist = []
    #CREATE boxes for unique titles 
    for row in app_tables.finishedhomeworkfiles.search():
      hwlist.append(row['Homework_Title'])
    uniquehw = list(dict.fromkeys(hwlist))
    #this is genuinely some bullshit i do not fully comprehend, but it works.
    self.tag = {'hwfp':{}, 'cardf':{}, 'cardt':{}, 'cardb':{}}
    for i in uniquehw:
      hwrow = app_tables.homeworkfiles.get(Homework_Title=i)
      title = Label(text= "Worksheet: " + str(i) +" Marked /" + str(hwrow['Total_Marks']), bold = True, font_size= 24)
      fp = FlowPanel(border= "solid 2px purple")
      self.add_component(title)
      self.tag['hwfp'][i] = fp
      self.add_component(fp)
    
    #CREATE instances for each hw submission, for each unique hw
    for row in app_tables.finishedhomeworkfiles.search():
      self.tmplbl_1.visible = False
      xyp = XYPanel(width=250, height=250, border="solid 1px")
      self.tag['hwfp'][row['Homework_Title']].add_component(xyp)

      ud = str(row["Upload Date"])
      ud = ud.split(" ")
      titlelbl = Label(text = "Uploaded: " + ud[0],align = "center")
      xyp.add_component(titlelbl, x=20, y=30)

      uid = row['Uploader']["Name"]
      uidlbl = Label(text = "Uploader: " + uid, align="center")
      xyp.add_component(uidlbl, x=20, y=10)

      fl = FileLoader(text="Upload marked work", border="solid 1px")
      xyp.add_component(fl, x=15, y=80)
      self.tag['cardf'][row] = fl
      
      txt = TextBox(text="input mark here", border="solid 1px", type= "number")
      xyp.add_component(txt, x=15, y=140)
      self.tag['cardt'][row] = txt
      
      btn = Button(text="Return", align="right", background="#EADDFF")
      self.tag['cardb'][row] = btn
      btn.add_event_handler('click',self.sendmarkedwork)
      xyp.add_component(btn, x=140, y=200)

      dlink = Link(text="Download", align = "left", url=row['Homework_File'])
      xyp.add_component(dlink, x=20, y=202)

  def sendmarkedwork(self, **event_args):
    for row in app_tables.finishedhomeworkfiles.search():
      markupload = self.tag['cardt'][row] 
      fileupload = self.tag['cardf'][row]
      if markupload.text is not None and fileupload.file is not None:
        row['Marked_File'] = fileupload.file
        cuser = row['Uploader'] 
        cuserhw = app_tables.homework.get(Student=cuser)
        cuserhwlist = cuserhw['Homework_List']
        cuserhwlist[row["Homework_Title"]] = 2
        cuserhw['Homework_List'] = cuserhwlist
      
      if markupload.text is not None and fileupload.file is not None:
        row['Marks'] = markupload.text
  
  @handle("dashboard_redirect", "click")
  def dashboard_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Dashboard_Page')

  @handle("homework_redirect", "click")
  def homework_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Homework_Page')

  @handle("tutor_redirect", "click")
  def tutor_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Tutor_Page')

  @handle("Logout_Button", "click")
  def Logout_Button_click(self, **event_args):
    """This method is called when the button is clicked"""
    anvil.users.logout()
    open_form('LogIn_Page')

  @handle("worksheet_redirect", "click")
  def worksheet_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Worksheet_Page')
    
  @handle("tutor1_redirect", "click")
  def tutor1_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Tutor_Page')

  @handle("statistics_redirect", "click")
  def statistics_redirect_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Statistics_Page')