FROM wenbo1188/ubuntu:1.0
MAINTAINER WENBO

#INSTALL PYTHON
RUN apt-get update -y
RUN apt-get install -y python

ADD agent.py /etc/
ADD server_comm.py /etc/
ADD server_comm.pyc /etc/
ENV TYPE None
ENV PROBLEM None
ENV CUSTOMERIP None
ENV DISTRIBUTEIP None
ENV NAME None
ENV ADDRESS None
ENV SKILLS None

CMD python /etc/agent.py --type ${TYPE} --problem ${PROBLEM} --customerip ${CUSTOMERIP} --distributeip ${DISTRIBUTEIP} --name ${NAME} --address ${ADDRESS} --skills ${SKILLS}
