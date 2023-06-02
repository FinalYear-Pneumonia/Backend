from API import create_application
from API.config import DevelopmentConfig

app = create_application(DevelopmentConfig)


if __name__ == '__main__':
    app.run()