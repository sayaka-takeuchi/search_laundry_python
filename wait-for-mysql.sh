# #!/bin/bash
# # wait-for-postgres.sh

# set -e

# host="$1"
# shift
# cmd="$@"

# until psql -h "$host" -U "postgres" -c '\l'; do
#   >&2 echo "Postgres is unavailable - sleeping"
#   sleep 1
# done

# >&2 echo "Postgres is up - executing command"
# exec $cmd

#!/bin/sh

set -e

host="$1"
shift
user="$1"
shift
password="$1"
shift
cmd="$@"

echo "Waiting for mysql"
until mysql -h"$host" -u"$user" -p"$password" &> /dev/null
do
        >&2 echo -n "."
        sleep 1
done

>&2 echo "MySQL is up - executing command"
exec $cmd