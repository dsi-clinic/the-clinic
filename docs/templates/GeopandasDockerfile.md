### Geopandas and Docker

Currently, installing Geopandas and docker can be a headache because of differences in the underlying operating system (specifically Windows / Unix / Mac). This file contains an example which will install geopandas.


### Dockerfile

```
FROM --platform=linux/amd64 osgeo/gdal:ubuntu-full-3.6.3

WORKDIR /code
RUN apt-get -y update 

RUN apt -y install python3-pip libspatialindex-dev \
    && apt-get install -y --no-install-recommends \
       gdal-bin \
       libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["jupyter", "notebook", "--port=8888", "--no-browser", "--ip=0.0.0.0", "--allow-root"]

```

### requirements.txt 

```
pandas==2.0.3
numpy==1.25.1
requests==2.31.0
GDAL==3.6.3
geopandas==0.12.2
folium==0.14.0
shapely==2.0.1
geopy==2.3.0
notebook==6.5.4
```