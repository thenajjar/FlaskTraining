from os import getenv

from dotenv import load_dotenv, find_dotenv

# Load the environment variables file
load_dotenv(find_dotenv())


def get_var(var):
    """loads the needed variable from the system environment variables file

    Args:
        var (str): the environment variable key to be loaded

    Raises:
        SystemExit: if variable is not found in the system environment variables file
    """
    try:
        # Load the variable from the system environment .env file
        var = getenv(str(var))
        return var
    except Exception as error:
        raise SystemExit("Could not find the variable: " + var + " inside environment variables file.", error)
