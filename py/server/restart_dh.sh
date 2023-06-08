dh_monit restart db_query_server
dh_monit restart db_merge_server
sudo -E -u irisadmin monit stop web_api_service
sudo -E -u irisadmin monit start web_api_service
