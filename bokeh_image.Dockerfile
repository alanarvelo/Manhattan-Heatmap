FROM python:3.7.2-slim

# Create MH directory
WORKDIR /Manhattan-Heatmap

# Install app dependencies
COPY requirements.txt .

RUN pip install -r requirements.txt

ADD myapp/ myapp/

ENTRYPOINT [ "bokeh", "serve", "myapp", "--port", "5100", "--allow-websocket-origin", "*", "--disable-index-redirect"]

# Create myapp directory
# WORKDIR /myapp

# ADD data/ data/

# , , "--use-xheaders"
# ENTRYPOINT ["bash"]