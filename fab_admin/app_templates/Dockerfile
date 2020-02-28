FROM python:3.6.8-alpine3.8

# Copy in your requirements file
COPY ./docker/gosu /usr/local/bin/

# Install build deps, then run `pip install`, then remove unneeded build deps all in a single step. Correct the path to your production requirements file, if needed.
ENV PYTHON_PIP_VERSION 9.0.1
ENV APP_USER {* app_name *}
ENV CONFIG_ENV config_dev.py
ENV GOSU_USER 0:0
ENV GOSU_CHOWN /{* app_name *}
RUN echo https://mirrors.ustc.edu.cn/alpine/v3.8/main > /etc/apk/repositories; \
    echo https://mirrors.ustc.edu.cn/alpine/v3.8/community >> /etc/apk/repositories
RUN set -ex \
    && adduser -D -S -h /{* app_name *} -s /bin/sh -G ping ${APP_USER} \
    && apk add --no-cache --repository https://mirrors.ustc.edu.cn/alpine/v3.8/main --repository https://mirrors.ustc.edu.cn/alpine/v3.8/community  --allow-untrusted  --virtual .build-deps \
            libldap\
            gcc \
            make \
            openldap-dev \
            zlib-dev \
            libc-dev \
            gd-dev\
            musl-dev \
            linux-headers \
            pcre-dev \
            python-dev \
            mariadb-dev \
            mariadb-client \
            libev \
            libxml2-dev \
            libxslt-dev \
    && chmod +x /usr/local/bin/gosu
    #&& gosu nobody true \
COPY ./docker/requirements.txt ./docker/entrypoint.sh ./docker/uwsgi.ini  ./docker/supervisord.conf   /{* app_name *}/
RUN set -ex \
    && LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "pip install --no-cache-dir -r /{* app_name *}/requirements.txt"
COPY  . /{* app_name *}

RUN chmod +x /{* app_name *}/entrypoint.sh
WORKDIR /{* app_name *}
VOLUME /{* app_name *}/logs
VOLUME /{* app_name *}/flask_session
# uWSGI will listen on this port
EXPOSE 8081
ENTRYPOINT ["sh","/{* app_name *}/entrypoint.sh"]
# Start supervisorctl
#CMD ["uwsgi", "--ini", "/{* app_name *}/uwsgi.ini", "--die-on-term"]
CMD ["/usr/local/bin/supervisord"]
