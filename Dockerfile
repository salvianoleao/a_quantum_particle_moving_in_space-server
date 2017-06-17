FROM ubuntu:latest
RUN apt-get update && apt-get install -y python3 apache2 python3-matplotlib
RUN a2enmod cgid
COPY ./html/ /var/www/html/
COPY ./cgi-bin/ /usr/lib/cgi-bin/
EXPOSE 80
ENV NAME "A QUANTUM PARTICLE MOVING IN SPACE"
CMD service apache2 start; sleep infinity
