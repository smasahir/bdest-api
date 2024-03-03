# Anaconda.io公式のminiconda3イメージ
FROM continuumio/miniconda3
# pythonの出力表示をDocker用に調整
ENV PYTHONUNBUFFERED=1

WORKDIR /src

RUN apt update -y && apt upgrade -y
RUN mkdir /usr/lib/jvm
RUN wget -P /usr/lib/jvm https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u402-b06/OpenJDK8U-jdk_x64_linux_hotspot_8u402b06.tar.gz
RUN tar zxvf /usr/lib/jvm/OpenJDK8U-jdk_x64_linux_hotspot_8u402b06.tar.gz -C /usr/lib/jvm
RUN rm /usr/lib/jvm/OpenJDK8U-jdk_x64_linux_hotspot_8u402b06.tar.gz

ENV JAVA_HOME=/usr/lib/jvm/jdk8u402-b06
ENV PATH=/usr/lib/jvm/jdk8u402-b06/bin:${PATH}
ENV CLASSPATH=.:/usr/lib/jvm/jdk8u402-b06/lib

RUN conda create -y -n v_env python==3.10
SHELL ["conda", "run", "-n", "v_env", "/bin/bash", "-c"]
RUN conda install -y -c conda-forge matplotlib pandas numpy scikit-learn xgboost pyarrow fastapi uvicorn sqlalchemy psycopg2
RUN conda install -y -c conda-forge rdkit

# uvicornのサーバーを起動
CMD ["conda", "run", "-n", "v_env", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]
