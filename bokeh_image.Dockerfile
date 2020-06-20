FROM python:3.7.2-slim

# Create MH directory
WORKDIR /Manhattan-Heatmap

# Install app dependencies
COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

ADD myapp/ myapp/

ADD data/ data/

# ENTRYPOINT [ "bokeh", "serve", "myapp", "--port", "5006", "--allow-websocket-origin", "*", "--disable-index-redirect"]
ENTRYPOINT ["python", "myapp/main.py"]

# Create myapp directory
# WORKDIR /myapp



# , , "--use-xheaders"
# ENTRYPOINT ["bash"]