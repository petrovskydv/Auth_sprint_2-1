FROM python:3.10

COPY . /code

RUN  pip install --upgrade pip && pip install -r /code/requirements.txt

WORKDIR /code
RUN chmod +x entrypoint.sh
RUN sed -i 's/\r//' entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]