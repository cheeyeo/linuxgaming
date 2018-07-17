from linuxgaming import create_app

# Work around for AWS EBS
# Set WSGI to run.py
application = create_app()