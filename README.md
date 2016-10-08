# icinga2-healtcheck
icinga2 cluster node daemon healtcheck

### Description
This script is checking icinga2 daemon which is running at cluster environment,so this means that
if a node taked to offline state, it returns "http 500" unless returning the http 200 response code.
You can either use this script behind of a load balancer to understand which one icinga2 host active role or which one is offline in cluster mode.

### Usage
````
python icinga2-ha-healtcheck.py http://<icinga2-host:8008>/healtcheck
````

### Tested with
````
Icinga2 2.5.4
````
