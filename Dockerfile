FROM python:3.10 as builder
COPY requirments.txt ./

RUN pip install --user -r requirments.txt

FROM python:3.10
WORKDIR /code

COPY --from=builder /root/.local /root.local

EXPOSE 443/tcp

ENV PATH=/root/.local:$PATH

CMD ["python","-u","./Skeleton_parse.bot.py"]