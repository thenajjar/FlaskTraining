from configparser import ConfigParser


def db_config(filename='src\\database\\database.ini', section='postgresql'):
    """_summary_

    Args:
        filename (str, optional): File that stores database settings. Defaults to 'src\database\database.ini'.
        section (str, optional): Specify section that stores the data in the congig file. Defaults to 'postgresql'.

    Raises:
        Exception: if section is not found in the configuration file

    Returns:
        dictionary: database settings
    """    
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)

    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        # convert the settings file to a python dictionary
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} not found in the {1} file'.format(section, filename))

    return db
