FROM msagency/msa-image-python:1.0.2

# Install the Python dependencies
ADD requirements.txt /opt/ms/

# Installing scipy on alpine is more complicated than anticipated
# from https://github.com/drillan/docker-alpine-scipy/blob/master/Dockerfile
RUN apk update \
&& apk add \
    ca-certificates \
    libstdc++ \
    libgfortran \
    python3 \
&& apk add --virtual=build_dependencies \
    gfortran \
    g++ \
    make \
    python3-dev \
&& ln -s /usr/include/locale.h /usr/include/xlocale.h \
&& mkdir -p /tmp/build \
&& cd /tmp/build/ \
&& wget http://www.netlib.org/blas/blas-3.6.0.tgz \
&& wget http://www.netlib.org/lapack/lapack-3.6.1.tgz \
&& tar xzf blas-3.6.0.tgz \
&& tar xzf lapack-3.6.1.tgz \
&& cd /tmp/build/BLAS-3.6.0/ \
&& gfortran -O3 -std=legacy -m64 -fno-second-underscore -fPIC -c *.f \
&& ar r libfblas.a *.o \
&& ranlib libfblas.a \
&& mv libfblas.a /tmp/build/. \
&& cd /tmp/build/lapack-3.6.1/ \
&& sed -e "s/frecursive/fPIC/g" -e "s/ \.\.\// /g" -e "s/^CBLASLIB/\#CBLASLIB/g" make.inc.example > make.inc \
&& make lapacklib \
&& make clean \
&& mv liblapack.a /tmp/build/. \
&& cd / \
&& export BLAS=/tmp/build/libfblas.a \
&& export LAPACK=/tmp/build/liblapack.a \
&& pip install -r /opt/ms/requirements.txt \
&& apk del --purge -r build_dependencies \
&& rm -rf /tmp/build \
&& rm -rf /var/cache/apk/*

# Override the default endpoints
ADD README.md NAME LICENSE VERSION /opt/ms/
ADD swagger.json /opt/swagger/swagger.json

# Copy all the other application files to /opt/ms
ADD run.sh /opt/ms/
ADD app.py /opt/ms/

# Execute the run script
CMD ["ash", "/opt/ms/run.sh"]
