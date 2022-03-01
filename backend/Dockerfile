FROM pymongo_base_image
COPY python-web-server.py ./python-web-server.py
COPY backendFunctions.py ./backendFunctions.py
EXPOSE 80
CMD ["python", "python-web-server.py"]
