FROM python:3.6.7-alpine3.8
WORKDIR /srv/locations/
COPY source/requirements.txt .
# Finally, install the remaining Python requirements
RUN pip install -r requirements.txt
ENV FLASK_APP="locations.py"
ENV FLASK_DEBUG=1
# Run the python script with unbuffed output (-u)
# Without this the various print() outputs will not
# appear in the docker logs
# TODO Update to run under nginx
# TODO During dev we are mapping the scripts into the container via volumes,
# but in the end we'll copy the script in to make a self-contained package
EXPOSE 5000
CMD  ["python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
