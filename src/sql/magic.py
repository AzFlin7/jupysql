import sys

from IPython.core.magic import Magics, magics_class, cell_magic, line_magic
from IPython.core.plugin import Plugin
from IPython.utils.traitlets import Instance

import connection
import parse
import run

def execute(line, cell=''):
    parsed = parse.parse('%s\n%s' % (line, cell))
    conn = connection.Connection.get(parsed['connection'])
    result = run.run(conn, parsed['sql'])
    return result    

@magics_class
class SQLMagics(Magics):
    """Runs SQL statement on a database, specified by SQLAlchemy connect string.
    
    Provides the %%sql magic."""
    
    @line_magic('sql')
    @cell_magic('sql')
    def execute(self, line, cell=''):
        """Runs SQL statement against a database, specified by SQLAlchemy connect string.
    
        If no database connection has been established, first word
        should be a SQLAlchemy connection string, or the user@db name
        of an established connection.

        Examples::

          %%sql postgresql://me:mypw@localhost/mydb
          SELECT * FROM mytable

          %%sql me@mydb
          DELETE FROM mytable
          
          %%sql
          DROP TABLE mytable
          
        SQLAlchemy connect string syntax examples:
            
          postgresql://me:mypw@localhost/mydb
          sqlite://
          mysql+pymysql://me:mypw@localhost/mydb
          
        """
        return execute(line, cell)
   
class SQLMagic(Plugin):
    """%%sql <SQLAlchemy connection string> <sql statement> runs SQL against a database."""
    shell = Instance('IPython.core.interactiveshell.InteractiveShellABC')
    
    def __init__(self, shell, config):
        super(SQLMagic, self).__init__(shell=shell, config=config)
        shell.register_magics(SQLMagics)
        
_loaded = False

def load_ipython_extension(ip):
    """Load the extension in IPython."""
    global _loaded
    if not _loaded:
        plugin = SQLMagic(shell=ip, config=ip.config)
        ip.plugin_manager.register_plugin('sqlmagic', plugin)
        _loaded = True    
