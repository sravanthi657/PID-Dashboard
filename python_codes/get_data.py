from oneM2M_functions import *

server = "https://esw-onem2m.iiit.ac.in"
cse = "/~/in-cse/in-name/"
ae = "Test-1"
container_name = "Data"

# ------------------------------------------
# Fill code here to get latest content_instance
# specified by the URI
# ------------------------------------------
ret_code, latest_data = get_data(server+cse+ae+"/Data/la")
print(latest_data)
# ------------------------------------------

# ------------------------------------------
# Fill code here to get oldest content_instance
# specified by the URI
# ------------------------------------------
# ret_code, oldest_data = get_data(server+cse+ae+"/Data/ol")
# print(oldest_data)
# ------------------------------------------

# ------------------------------------------
# Fill code here to get all content_instances
# specified by the URI
# Note: change the return statement as given in get_data function inside the oneM2M_functions.py
# ------------------------------------------
# ret_code, all_data = get_data(server+cse+ae+"/Data?rcn=4")
# print(all_data)
# ------------------------------------------
