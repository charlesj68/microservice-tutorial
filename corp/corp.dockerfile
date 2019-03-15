FROM python:3.6.7-alpine3.8
WORKDIR /srv/corp/

# If mounting the source as a volume, then we only need
# to copy the requirements.txt; in that case uncomment next line.
# COPY source/requirements.txt .
# Otherwise, copy the source into the container image 
COPY source .

# We need gcc to build the mysqlclient package
RUN ["apk", "add", "build-base"]
# We need mariadb-dev to use the mysqlclient package
RUN ["apk", "add", "mariadb-dev"]
# Finally, install the remaining Python requirements
RUN pip install -r requirements.txt
ENV FLASK_APP="corp.py"
ENV FLASK_DEBUG=1
# Run the python script with unbuffered output (-u)
# Without this the various print() outputs will not
# appear in the docker logs
EXPOSE 5000
CMD  ["python", "-u", "-m", "flask", "run", "--host=0.0.0.0"]
