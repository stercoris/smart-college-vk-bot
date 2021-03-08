# set base image (host OS)
FROM python:3.7.5

# set the working directory in the container
WORKDIR /vk-bot

# copy the dependencies file to the working directory
COPY requirements.txt .

# copy project
COPY . /vk-bot

# install dependencies
RUN pip install -r requirements.txt

# set timezone
ENV TZ=Europe/Samara
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# command to run on container start
CMD [ "python", "logic.py" ]