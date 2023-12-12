FROM python:3.10

RUN mkdir /opt/madi_api
# 
WORKDIR /opt/madi_api
#
COPY ./requirements.txt .
# 
RUN pip install --user --no-cache-dir --upgrade -r requirements.txt
# 
COPY . .
#
WORKDIR ./src
# 
CMD ["uvicorn", "main:app", "--port", "8080"]
