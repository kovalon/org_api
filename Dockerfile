FROM centos:centos7

WORKDIR /usr/src/org_api

COPY . .

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN yum -y install epel-release
RUN yum -y install python36
RUN pip3 install --upgrade pip
# RUN python3 -m venv venv
# RUN source venv/bin/activate

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt
RUN cp -a sources/fields.py /usr/local/lib/python3.6/site-packages/flask_restplus/fields.py
RUN cp -a sources/api.py /usr/local/lib/python3.6/site-packages/flask_restplus/api.py

EXPOSE 8080

ENTRYPOINT python3 app.py
