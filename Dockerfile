FROM centos:centos7

WORKDIR /usr/src/org_api

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN yum -y install epel-release
RUN yum -y install python36
RUN pip3 install --upgrade pip

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
RUN cp -a sources/fields.py /usr/local/lib/python3.6/site-packages/flask_restplus/fields.py
RUN cp -a sources/api.py /usr/local/lib/python3.6/site-packages/flask_restplus/api.py

EXPOSE 5000

ENTRYPOINT python3 app.py
