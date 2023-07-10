### This is a starting point for a dockerfile. 
### Note that it is only using python 3.8 and expects there to be a 
### a requirements.txt file

FROM python:3.8-buster
WORKDIR /tmp
RUN apt update
RUN apt install -y python3-pip python3-dev
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]
