FROM python:3.6

# because Docker shares permissions of mounted files, we need our user in the container to
# have the same uid as the user outside. Only this way, we can read/write our files from
# inside *and* outside the container without needing global rw-permissions on the files.
ARG userid
RUN useradd -u $userid -ms /bin/bash gwf


RUN curl -sL https://deb.nodesource.com/setup_12.x | bash -
RUN apt-get install -y nodejs

RUN apt-get update && apt-get -y install libgdal-dev
RUN wget http://download.osgeo.org/gdal/2.1.2/gdal212.zip; unzip gdal212.zip; rm gdal212.zip
RUN cd gdal-2.1.2; ./configure --with-python; make -j 32; make install -j 32; cd ..
COPY --chown=gwf . /home/gwf/cuizinart

RUN mkdir /home/gwf/.ssh && mv /home/gwf/cuizinart/.id_rsa /home/gwf/.ssh/id_rsa && chown -R gwf:gwf /home/gwf/.ssh && chmod 700 /home/gwf/.ssh

RUN pip install -r /home/gwf/cuizinart/requirements.txt

USER gwf
WORKDIR /home/gwf/cuizinart/frontend
RUN npm install && npm run build
WORKDIR /home/gwf/

# We need to run the flask commands from the project base folders,
# so we execute the app from there
RUN mv /home/gwf/cuizinart/docker-entrypoint.sh /home/gwf/
RUN chmod +x /home/gwf/docker-entrypoint.sh

HEALTHCHECK --interval=5m --timeout=10s --retries=3 \
 CMD curl -f http://localhost:5000/ || exit 1
CMD ["/bin/bash", "/home/gwf/docker-entrypoint.sh"]
