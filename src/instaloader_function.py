import instaloader

def initialize_instaloader() -> instaloader.Instaloader: 
    """
    Initializes an Instaloader instance.

    Returns:
        instaloader.Instaloader: An initialized Instaloader object.
    """
    return instaloader.Instaloader()


def instagram_login(L: instaloader.Instaloader, username: str, password:str) -> None:
    """
    Login to Instagram using Instaloader.

    Args:
        L (instaloader.Instaloader): An initialized Instaloader instance.
        username (str): The Instagram username.
        password (str): The corresponding password.
    """
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
def target_name_input(L: instaloader.Instaloader, profile_name: str) -> instaloader.Profile:
    """
    Fetches an Instagram user profile using Instaloader.

    Args:
        L (instaloader.Instaloader): An initialized Instaloader instance.
        profile_name (str): The username of the target profile.

    Returns:
        instaloader.Profile: The user profile object.
    """
    profile = instaloader.Profile.from_username(L.context, profile_name)
    return profile

