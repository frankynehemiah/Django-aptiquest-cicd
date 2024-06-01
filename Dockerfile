FROM python:3
RUN pip install django
RUN pip install django-widget-tweaks
RUN pip install requests
RUN pip install Pillow

Copy . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
