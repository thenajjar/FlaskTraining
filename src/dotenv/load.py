from dotenv import load_dotenv, find_dotenv
from os import getenv

# Load the enviornment variables file
load_dotenv(find_dotenv())

def get_var(var):
    """loads the needed variable from the system enviroment variables file

    Args:
        var (str): the enviroment variable key to be loaded

    Raises:
        SystemExit: if variable is not found in the system enviroment variables file
    """    
    try:
        # Load the variable from the system enviroments .env file
        var = getenv(str(var))
        return var
    except:
        raise SystemExit("Could not find the variable: "+var+" inside environment variables file.")