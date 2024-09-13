import instaloader
import time

# a class to define your own data fetching speed for instaloader
class MyRateController(instaloader.RateController):
    def sleep(self):
        time.sleep(5) # fetch data per 5s


# Initialize Instaloader 
def initialize_instaloader():
    return instaloader.Instaloader()


# Login to Instagram
def instagram_login(L, username, password):
    try:
        L.context.log("Logging in")
        L.load_session_from_file(username)
        L.context.log("Logged in scuessfully!")
        if not L.context.is_logged_in:
            L.context.log("login credentials are invalid")
            L.interactive_login(username)
            L.save_session_to_file()
        
    except FileNotFoundError as e:
        L.login(username, password)
        L.save_session_to_file()
        print("saved session files and successfully login!")

    except Exception as e:
        L.context.log("Error during login: %s" % str(e))


# Input the target name
def target_name_input(L, profile_name):
    profile = instaloader.Profile.from_username(L.context, profile_name)
    return profile

