FROM hub.c.163.com/sportscool/python3 

MAINTAINER zhxfei <dylan@zhxfei.com>

ENV PATH /usr/bin:$PATH

ADD . /code

WORKDIR /code

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple

CMD scrapy crawl zhihu_redis 
