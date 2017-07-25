from private import *

## POSTGRES CONECTION DETAILS
PS_HOST_NAME = "toronto.cfeeqz1xpx0l.us-west-2.rds.amazonaws.com"
PS_DB_NAME = "parking"
PS_PORT = 5432


# DB COLS

FIELD_MAP = [
    {'name':'date', 'func':'do_none'},
    {'name':'time_of_infraction', 'func':'check_int'},
    {'name':'infraction_code', 'func':'check_int'},
    {'name':'infraction_description', 'func':'check_text'},
    {'name':'set_fine_amount', 'func':'check_int'},
    {'name':'location1', 'func':'check_varchar', 'length': 10},
    {'name':'location2', 'func':'check_varchar', 'length': 50},
    {'name':'province', 'func':'check_varchar', 'length': 5}
]
