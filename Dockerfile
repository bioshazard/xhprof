FROM alpine:latest
RUN apk update && \
    apk add graphviz apache2 php7-apache2 php7-ctype

RUN mkdir -p /run/apache2/
RUN ln -s /dev/stdout /var/log/apache2/access.log && \
    ln -s /dev/stdout /var/log/apache2/error.log

RUN apk --no-cache add msttcorefonts-installer fontconfig && update-ms-fonts && fc-cache -f

RUN echo '<?php phpinfo(); ?>' > /var/www/localhost/htdocs/info.php

COPY xhprof_html/ /var/www/localhost/htdocs/xhprof_html/
COPY flamegraph/ /opt/flamegraph/

CMD httpd -k start -D FOREGROUND
