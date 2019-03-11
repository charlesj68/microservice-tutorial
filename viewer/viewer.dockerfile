FROM python:3.6.7-alpine3.8
# Since we are creating a small web server, let us home it in the /srv treee
WORKDIR /srv/viewer/
# Instead of copying all of the source, we only want to copy what we will need
# to execute container build commands. In this case, thats the Python
# requirements file. The rest of our server code will be mapped in at container
# run time
COPY viewer/requirements.txt .
# Package in a small script that will query the main page of the
# web app. It simply checks that the app responds with a HTTP Status 200,
# but that is enough to give us an indication that the app is up and running.
# We could also implement a more sophisticated check within the API portion
# of the Flask app, and perform deeper inspection of functionality; then use 
# that endpoint in our healthcheck app.
COPY healthcheck.py .
# We need gcc to build the mysqlclient package
RUN ["apk", "add", "build-base"]
# We need mariadb-dev to use the mysqlclient package
RUN ["apk", "add", "mariadb-dev"]
RUN pip install -r requirements.txt
HEALTHCHECK --interval=60s --timeout=30s --start-period=20s --retries=3 CMD [ "python", "healthcheck.py" ]
ENV FLASK_APP="viewer"
ENV FLASK_DEBUG=1
# EXPOSE tells the world what port(s) we are planning on communicating outward
# over, but the actual mapping takes place at container-run time
EXPOSE 5000
CMD  ["python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
