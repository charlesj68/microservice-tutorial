FROM python:3.6.7-alpine3.8
WORKDIR /home/simulator/
COPY source/* ./
# We need gcc to build the numpy package
RUN ["apk", "add", "build-base"]
# Finally, install the remaining Python requirements
RUN pip install -r requirements.txt
# Run the python script with unbuffed output (-u)
# Without this the various print() outputs will not
# appear in the docker logs
CMD  ["python", "simulator.py"]
