#FROM debian:bullseye
FROM debian:bullseye-slim

LABEL MAINTAINER="https://github.com/muslih-DIY"

ENV ASTERISK_VERSION=18.14.0
RUN mkdir /usr/src/asterisk
WORKDIR /usr/src/asterisk

ADD http://downloads.asterisk.org/pub/telephony/asterisk/releases/asterisk-${ASTERISK_VERSION}.tar.gz asterisk.tar.gz
#COPY asterisk-${ASTERISK_VERSION}.tar.gz ./asterisk.tar.gz
COPY ./third-party/tmp/* /tmp/

RUN tar --strip-components 1 -xzf asterisk.tar.gz
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive \
    apt-get install -y --no-install-recommends \
            autoconf \
	    file \
            binutils-dev \
            build-essential \
            ca-certificates \
            curl \
	    less \
        aptitude\
        libjansson-dev \
            libcurl4-openssl-dev \
            libedit-dev \
            patch \
            libnewt-dev \
            libgsm1-dev \
            libogg-dev \
            libpopt-dev \
            libresample1-dev \
            libspandsp-dev \
            libspeex-dev \
            libspeexdsp-dev \
            libsqlite3-dev \
            sqlite3 \
            libncurses5-dev \
            subversion\
            libssl-dev \
            libvorbis-dev \
            libxml2-dev \
            libxslt1-dev \
	    libncurses5 ncurses-bin ncurses-term \
            portaudio19-dev \
	    procps \
            python3-pip \
	    python-setuptools \
	    tcpdump \
            unixodbc-dev \
            uuid \
            uuid-dev \
	    vim-tiny \
        xmlstarlet \
        odbcinst1debian2 libodbc1 odbcinst unixodbc libsqliteodbc odbc-postgresql && \
        DEBIAN_FRONTEND=noninteractive ./contrib/scripts/install_prereq install &&\
        apt-get purge -y --auto-remove && \
        rm -rf /var/lib/apt/lists/* && \
        useradd --system asterisk && \
        pip install j2cli && \
        ./configure   --with-resample --with-pjproject --with-jansson-bundled && \
        make menuselect/menuselect menuselect-tree menuselect.makeopts && \
        # disable BUILD_NATIVE to avoid platform issues
        menuselect/menuselect --disable BUILD_NATIVE menuselect.makeopts && \
        menuselect/menuselect --enable BETTER_BACKTRACES menuselect.makeopts && \
        menuselect/menuselect --enable codec_opus menuselect.makeopts && \
        make all && \
        make install && \
        make samples && \
        # make basic-pbx && \
        # make progdocs
        chown -R asterisk:asterisk /var/*/asterisk && \
        chmod -R 750 /var/spool/asterisk && \
        # Uncomment this if you want to remove the asterisk source files.
        rm -rf /usr/src/asterisk 

# COPY get_sounds.sh get_sounds.sh
# RUN ./get_sounds.sh

WORKDIR /etc/asterisk/
# USER asterisk

#// if need to expose ports you and change the user uncomment following lines
USER root
EXPOSE 5060
EXPOSE 5060/udp
EXPOSE 10000-10099/udp
# RUN echo 'root:Droot' | chpasswd

## any of the service you can use to start the container
# CMD ["bash"]
# CMD ["asterisk", "-cvv"]
CMD ["bash", "/entrypoint.sh"]