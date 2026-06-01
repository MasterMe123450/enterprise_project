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
#
@anvil.server.callable
def tutor_perms():
  tutor = 'ethan.tay1@education.nsw.gov.au'
  if anvil.users.get_user() is None:
    print("Nobody is logged in.")
    return False
  elif anvil.users.get_user()['email'] == tutor:
    print(f"{tutor} is allowed to see this.")
    return True
  else:
    print("The user is a student.")
    return False