FROM python

RUN apt-get update -y;apt-get upgrade -y
RUN mkdir -p /var/www/html
WORKDIR /var/www/html
COPY . . 
EXPOSE 80
CMD ["python3","myscript.py","-p","80"]
