from myproject import application

# gunicorn wsgi:application
# gunicorn -w 2 -b 0.0.0.0:8080 myproject:application
if __name__ == "__main__":
    application.run()
