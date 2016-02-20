#!/usr/bin/env python2
"""List available machines on all clouds, using mist.io API

This will show all machines on all clouds, no matter if they are
enabled or disabled from the mist.io dashboard
"""

import json
import sys
import time
import json
import multiprocessing.pool

try:
    import requests
except ImportError:
    sys.exit('ERROR: please install requests library')

EMAIL = ''
PASSWORD = ''


def list_all_machines(cloud_ids, headers):
    "Given the cloud ids, runs in parallel queries to get all machines"
    def list_one_cloud(cloud_id):
        cloud_machines = requests.get('https://mist.io/clouds/%s/machines' % cloud_id, headers=headers)
        if cloud_machines.status_code == 200:
            machines = cloud_machines.json()
            for machine in machines:
                machine['cloud'] = cloud_id
            return machines
        return []

    pool = multiprocessing.pool.ThreadPool(8)
    results = pool.map(list_one_cloud, cloud_ids)
    pool.terminate()

    machines = []
    for result in results:
        machines.extend(result)
    return machines


def get_price_from_tags(tags):
    "Gets tags for a machine and checks if a tag price is there"
    price = None
    for tag in tags:
        # Tags are stored as dicts or unicode
        if type(tag) == dict:
            if tag.get('key') == 'price':
                price = tag.get('value')
        elif type(tag) in [unicode, str]:
            try:
                tag = json.loads(tag)
                price = tag.get('price')
            except:
                pass
    return price


def main():
    """Main"""

    start_time = time.time()
    # Authenticate with mist.io using email/password.
    # We get an API token we'll use on all requests from now on
    conn = requests.post('https://mist.io/auth', data={'email': EMAIL, 'password': PASSWORD})
    if conn.status_code != 200:
        sys.exit('ERROR: please provide a valid username and password - aka your mist.io account')
    API = json.loads(conn.text).get('token')
    headers = {'Authorization': API}

    # Get clouds
    clouds = requests.get('https://mist.io/clouds', headers=headers).json()
    cloud_ids = [cloud.get('id') for cloud in clouds]
    # Get machines
    machines = list_all_machines(cloud_ids, headers)

    end_time = int(time.time() - start_time)
    print '*** Received %d clouds and %d machines. Time taken: %d seconds *** ' % (len(clouds), len(machines), end_time)
    print '*** Showing machine name, state, machine cloud provider, machine size, launch time and price *** '
    print '*** size/launch time is EC2 specific but can easily be configured for any other provider *** '
    print '*** machine price is what the machine has as tag price. Could easily be a value on the metadata as well *** \n\n'

    print 'NAME  - STATE  -  CLOUD PROVIDER  -  SIZE  -  LAUNCH TIME  -  PRICE'
    print '--------------------------------------------------------------------\n'

    for machine in machines:
        name = machine.get('name')
        state = machine.get('state')
        cloud = [cloud for cloud in clouds if cloud.get('id') == machine.get('cloud')][0]
        cloud_title = cloud.get('title')
        extra = machine.get('extra', {})

        instance_type = None
        # EC2 has on the metadata instance_type
        if cloud.get('provider').startswith('ec2'):
            instance_type = extra.get('instance_type')

        launch_time = None
        # EC2 has on the metadata launch_time
        if cloud.get('provider').startswith('ec2'):
            launch_time = extra.get('launch_time')

        # Tags are either returned by the provider, or added by user through mist.io
        # If a tag price exists, then show it
        tags = machine.get('tags', [])
        price = get_price_from_tags(tags)

        # Do not show None values
        show_results = [name, state, cloud_title, instance_type, launch_time, price]
        show_results = [result for result in show_results if result is not None]

        print ' '.join(show_results)

if __name__ == "__main__":
    main()
