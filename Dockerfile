FROM python:3.4
MAINTAINER leishi <lei.shi.10151@gmail.com>

# install requirements
RUN pip install -U pip setuptools
ADD requirements /opt/zhihuCrawler/requirements
RUN pip install -r /opt/zhihuCrawler/requirements

# add all repo
ADD ./ /opt/zhihuCrawler

WORKDIR /opt/zhihuCrawler

VOLUME ["/opt/zhihuCrawler"]
ENTRYPOINT ["python", "run.py"]

CMD ["all"]