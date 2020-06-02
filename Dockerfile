FROM python:3.7.2-slim

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt /app

RUN pip install -r requirements.txt

# Bundle app source
COPY . /app

EXPOSE 8080
CMD [ "bokeh", "serve", "--show", "--allow-websocket-origin", "*", "heatmap_mockup.py"]