FROM python:3.6.7-alpine3.8
WORKDIR /srv/locations/
COPY source/requirements.txt .
RUN pip install -r requirements.txt
ENV FLASK_APP="locations.py"
ENV FLASK_DEBUG=1
# Run the python script with unbuffered output (-u)
# Without this the various print() outputs will not
# appear in the docker logs
EXPOSE 5000
CMD  ["python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
