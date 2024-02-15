# Anaconda.io公式のminiconda3イメージ
FROM continuumio/miniconda3
# pythonの出力表示をDocker用に調整
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY env.yaml* ./

# env.yamlが存在する場合、condaでライブラリをインストール
RUN conda env create -f env.yaml -n v_env

# uvicornのサーバーを起動
CMD ["conda", "run", "-n", "v_env", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--reload"]