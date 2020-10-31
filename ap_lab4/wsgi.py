from myproject import application

# gunicorn wsgi:application
if __name__ == "__main__":
    application.run()
