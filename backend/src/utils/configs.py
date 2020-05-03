from configparser import ConfigParser


def get_auth0_variables(filename='config.properties'):
    config = ConfigParser()
    config.read(filename)
    config_vars = dict(config.items('AUTH_0'))
    return config_vars