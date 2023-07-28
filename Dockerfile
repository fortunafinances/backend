#Download Python from DockerHub and use it
FROM python:3.11.4

#Set the working directory in the Docker container
WORKDIR /code

#Copy the dependencies file to the working directory
COPY requirements.txt .

#Install the dependencies
RUN pip install -r requirements.txt

#Copy the Flask app code to the working directory
#COPY server/ .
#COPY mockData/ .
#COPY genAi/ .
#COPY database/ .
#COPY authentication/ .
COPY . ./

WORKDIR /code/server


# go to the correct directory
#RUN cd server

#Run the container
CMD [ "python", "server.py" ]