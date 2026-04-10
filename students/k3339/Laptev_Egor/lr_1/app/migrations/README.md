"""
Alembic configuration file for database migrations.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from alembic import config

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:123@localhost:5432/hackathon_db")

# Create migrations INI file content
alembic_ini_content = f"""# Alembic Configuration

[alembic]
# path to migration scripts
sqlalchemy.url = {SQLALCHEMY_DATABASE_URL}

# template used to generate migration file names; The default value is %%(rev)s_%%(slug)s
# Uncomment the line below if you want the files to be prepended with date and time
# file_template = %%(rev)s_%%(slug)s_%%(ts)s

# sys.path path, will be prepended to sys.path if present
# defaults to the current directory
prepend_sys_path = .

# timezone to use when rendering the date
# within the migration file as well as the filename.
# string value is passed to datetime.datetime.now().astimezone() to select an appropriate timezone.
# leave blank for localtime
# timezone =

# max length of characters to apply to the
# "slug" field
# truncate_slug_len = 40

# set to 'true' to run the environment during
# the 'revision' command, regardless of autogenerate
# revision_environment = false

# set to 'true' to allow .pyc and .pyo files without
# a source .py file to be detected as revisions in the
# versions/ directory
# sourceless = false

# version location specification; This defaults
# to alembic/versions.  When using multiple version
# paths, the initial alembic.version_path_separator here should be used
# to separate the files from the directories
# version_path_separator = :
# version_locations = %(here)s/bar:%(here)s/bat:alembic/versions

# version path separator; As mentioned above, this is the character used to split
# version_path_separator. The default value is ":" for *nix, ";" for windows
# version_path_separator = ;

# the output encoding used when revision files
# are written from script.py.mako
# output_encoding = utf-8

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
"""
