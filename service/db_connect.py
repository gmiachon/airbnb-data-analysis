import ibm_db
import os

# Setting variables for DB connection
dsn_hostname = os.environ["IBM_DB2_HOSTNAME"]
dsn_uid = os.environ["IBM_DB2_UID"]
dsn_pwd = os.environ["IBM_DB2_PWD"]
dsn_port = os.environ["IBM_DB2_PORT"]
dsn_driver = "{IBM DB2 ODBC DRIVER}"
dsn_database = "bludb"
dsn_protocol = "TCPIP"
dsn_security = "SSL"

dsn = (f"DRIVER={dsn_driver};DATABASE={dsn_database};HOSTNAME={dsn_hostname};PORT={dsn_port};" +
       f"PROTOCOL={dsn_protocol};UID={dsn_uid};PWD={dsn_pwd};SECURITY={dsn_security};")


def connect_ibmdb2():
    """
    This function returns an IBM DB2 connection element which points to the database used in this project
    """

    try:
        conn = ibm_db.connect(dsn, "", "")
        print("Successfuly connected to database")
        return conn
    except:
        print(f"Unable to connect to database: {ibm_db.conn_errormsg()}")
        return -1

conn = connect_ibmdb2()
print(type(conn))
client = ibm_db.client_info(conn)
print(client.DRIVER_NAME)
ibm_db.close(conn)
