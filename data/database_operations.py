import psycopg2
import psycopg2.extras
import io
import sys
import config
import logging as log

"""
CREATE TABLE tickets (
    infraction_date date,
    time_of_infraction integer,
    infraction_code integer,
    infraction_description text,
    fine_amt integer,
    location1 varchar(10),
    location2 varchar(50),
    province varchar(5)
)

CREATE INDEX tickets_loc ON tickets (location2);
"""


class IteratorFile(io.TextIOBase):
    """ given an iterator which yields strings,
    return a file like object for reading those strings.
    Taken from https://gist.github.com/jsheedy/ed81cdf18190183b3b7d
    """

    def __init__(self, it):
        self._it = it
        self._f = io.StringIO()

    def read(self, length=sys.maxsize):

        try:
            while self._f.tell() < length:
                self._f.write(next(self._it) + "\n")

        except StopIteration as e:
            # soak up StopIteration. this block is not necessary because
            # of finally, but just to be explicit
            pass

        except Exception as e:
            print("uncaught exception: {}".format(e))

        finally:
            self._f.seek(0)
            data = self._f.read(length)

            # save the remainder for next read
            remainder = self._f.read()
            self._f.seek(0)
            self._f.truncate(0)
            self._f.write(remainder)
            return data

    def readline(self):
        return next(self._it)

def postgres_load(conn, tablename, data):
    """
    Function to load data into a Postgres table
    ------
    params
        conn <Pyscopg Connection> : Connection to postgres data base
        data <list> : list of tuples, where each row is a tuple
        tablename <string> : tablename to load data into
    """
    try:
        log.info('Attempting to load data into Postgres table %s' % tablename)
        curs = conn.cursor()
        table_width = len(data[0])
        template_string = "|".join(['{}'] * table_width)
        f = IteratorFile((template_string.format(*x) for x in data))
        results = curs.copy_from(f, tablename, sep="|", null='None')
        curs.close()
        conn.commit()
        log.info('Data succesfully loaded')
        return True
    except Exception as e:
        log.exception("Unable to load data to Postgres due to error: %s"
                        % e)
        return False


def getConnection():
    """
    Function to create a connection to postgres.
    ------
    param
        None
    return
        cnxn <Pyscopg Connection> : Connection to postgres data base
    """
    log.info("Attempting to establish connection to postgres...")
    try:
        cnxn = psycopg2.connect(host=config.PS_HOST_NAME,
                                port=config.PS_PORT,
                                database=config.PS_DB_NAME,
                                user=config.PS_UID,
                                password=config.PS_PWD)
        return cnxn
    except Exception as e:
        log.exception("Unable to connect to postgres due to error: " + e)
        return None


def closeConnection(cnxn):
    """Function to close connection
    ------
    param
        cnxn <PYODBC/pyscog2 Connection> : Connection to postgres data base
    return
        True/False <bool> : Close status
    """
    log.info("Attempting to close connection.... ")
    try:
        cnxn.close()
        return True

    except Exception as e:
        log.exception("Closing postgres connection failed due to error: " + e)
        return False


def query(conn, query, data=False, columns=False):
    """Function to carry out retrieval of records via select queries
    ------
    param
        query <string> : String sql query
        conn <pyscopg Connection> : Connection to postgres data base
        data <tuple> : tuple of parameters that filter sql query. Defaults to False.
        columns <boolean> : If True, returns resultset as a list of dicts with keys as column names. Defaults to False.
    return
        resultset <PYODBC Result> : The result of fetched data from Teradata.
            Returns None on a failed attempt
    """
    log.info('Attempting to run select query')
    try:
        cur = conn.cursor()
        if data:
            if not isinstance(data, tuple): # data should be a single tuple
                data = (data,)
            cur.execute(query, data)
            resultset = cur.fetchall()
        else:
            cur.execute(query)
            resultset = cur.fetchall()
        if columns:
            colnames = tuple([desc[0] for desc in cur.description])
            resultset = [colnames] + resultset
        cur.close()
        return resultset
    except Exception as e:
        log.exception("Unable to run query due to error: " + e)
        return False


def execute_query(conn, query, data=False, multiple=False):
    """
    Function to run insert or update statements on postgres DB
    ------
    param
        conn <Pyscopg Connection> : Connection to postgres data base
        query <string> : Single sql query
        data <list> : List of tuples (if multiple=True) or single tuple (if multiple=False)
        multiple <boolean> : If True, expects data as list of tuples, if False expects data as single tuple
    """
    try:
        log.info('Attempting to execute query')
        cur = conn.cursor()
        if data:
            if multiple:  # data is a list of tuples
                cur.executemany(query, data)
            else:  # data is a single tuple
                cur.execute(query, data)
        else:
            cur.execute(query)
        conn.commit()
        cur.close()
        return True
    except Exception as e:
        log.exception("Unable to execute query due to error: " + e)
        return False
