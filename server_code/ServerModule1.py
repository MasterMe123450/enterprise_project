import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
tutor = ['ethan.tay1@education.nsw.gov.au']
@anvil.server.callable
def tutor_perms():
  if anvil.users.get_user() is None:
    return False
  elif anvil.users.get_user()['email'] in tutor:
    return True
  else:
    return False

@anvil.server.callable
def remove_tutors(user):
  if user in tutor:
    return True
  else:
    return False
