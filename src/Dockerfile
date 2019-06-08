# Dockerfile for Sample Device Status Monitoring Application.
#
# AUTHOR(s): Vinay Kini <vikini@cisco.com>
#            Lakshmi Jayanthi <ljayanth@cisco.com>
#            Kabiraj Sethi <kasethi@cisco.com>
#

# Base rootfs.
FROM centos:centos7

# Install Apache web server, pip and other supporting packages.
RUN yum -y --nogpgcheck install epel-release; \
    yum -y --nogpgcheck install python-pip net-tools httpd

# Install ncclient (Python Netconf client library) and
# dependencies, and XML/json parsers.
RUN pip install --upgrade pip; \
    pip install setuptools -U; \
    pip install ncclient==0.6.0 \
                xmltodict json2html

# Copy container startup script that starts web server.
COPY run_server.sh /
EXPOSE 80

# Copy sample application files.
COPY device_status.py /var/www/cgi-bin/

ENTRYPOINT ["/run_server.sh"]

