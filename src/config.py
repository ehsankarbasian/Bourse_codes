from dotenv import dotenv_values, load_dotenv
load_dotenv()

config = dotenv_values()


AGAH_USERNAME = (config['USERNAME'])
AGAH_PASSWORD = (config['PASSWORD'])
