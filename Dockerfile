FROM python:3
COPY . .
RUN pip install -r Frames.txt
CMD [ "python", "./main.py" ]