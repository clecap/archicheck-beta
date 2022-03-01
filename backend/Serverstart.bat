start run_mongo_container.sh -p
.\run_webserver_container.sh
call dbconf.bat
docker run --network archicheck-network -it --rm --name python_web_server -p 8080:80 -e "dbusername=%dbusername%" -e "dbpassword=%dbpassword%" python_server_image
	