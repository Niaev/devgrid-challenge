FROM python:3

WORKDIR /usr/src/app

COPY reqs.txt ./
RUN pip install --no-cache-dir -r reqs.txt

COPY . .

#RUN chmod +x ./start.sh
#CMD [ "./start.sh" ] 

CMD [ "python3", "./index.py" ]