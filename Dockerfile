FROM public.ecr.aws/amazonlinux/amazonlinux:2023-minimal AS clamav

RUN dnf update && dnf install -y \
    gcc gcc-c++ make python3 python3-pip valgrind \
    bzip2-devel check-devel json-c-devel libcurl-devel libxml2-devel \
    ncurses-devel openssl-devel pcre2-devel sendmail-devel zlib-devel \
    cmake tar gzip

RUN curl -L https://www.clamav.net/downloads/production/clamav-1.4.1.tar.gz | tar -xvzf -

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="~/.cargo/bin:${PATH}"

WORKDIR /clamav-1.4.1
RUN mkdir build \
    && cd build \
    && cmake .. \
        -D CMAKE_BUILD_TYPE=Release \
        -D CMAKE_INSTALL_PREFIX=/layer \
        -D CMAKE_INSTALL_LIBDIR=/layer/lib \
        -D OPTIMIZE=ON \
        -D ENABLE_SHARED_LIB=ON \
        -D ENABLE_CLAMONACC=OFF \
        -D ENABLE_MILTER=OFF \
        -D ENALBE_SYSTEMD=OFF \
        -D ENABLE_TESTS=OFF \
    && cmake --build . --target install

WORKDIR /layer
RUN zip -r9 clamav-layer.zip .

FROM public.ecr.aws/lambda/python:3.13 AS development
COPY --from=clamav /layer/clamav-layer.zip /opt/
RUN dnf install -y zip \
&& unzip /opt/clamav-layer.zip -d /opt/ \
&& rm /opt/clamav-layer.zip \
&& python3 -m pip install --user pipx \
&& python3 -m pipx ensurepath \
&& python3 -m pip install poetry
