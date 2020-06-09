FROM python:3.7.2-slim

# Create MH directory
WORKDIR /Manhattan-Heatmap

# Install app dependencies
COPY requirements.txt .

RUN pip install -r requirements.txt

# Create myapp directory
WORKDIR /myapp

# ADD myapp myapp/

# EXPOSE 5006
ENTRYPOINT [ "bokeh", "serve", "myapp", "--port", "5100", "--allow-websocket-origin", "*", "--disable-index-redirect"]
# , , "--use-xheaders"