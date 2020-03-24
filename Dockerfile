FROM debian:buster-slim

RUN apt-get update && apt-get -y install \
    ruby-full \
    lighttpd \
    uuid-runtime \
    qrencode \
    imagemagick \
    vim

ENV VIRTUAL_HOST=qr.local

COPY index.html /var/www/html/index.html
COPY cgi-bin/* /usr/lib/cgi-bin/
COPY 10-cgi.conf /etc/lighttpd/conf-enabled/

RUN gem install --no-user-install prawn

CMD ["lighttpd", "-D", "-f", "/etc/lighttpd/lighttpd.conf"]
