
mist.io API examples
====================

Examples of scripts created with the mist.io API. More info can be found on http://docs.mist.io/article/94-mist-io-rest-api


How to run the scripts
----------------------

To run the scripts the only dependency needed is python and virtualenv. Clone this repository, create a virtualenv, install python requests lib, edit the script that interests you and set the email/password credentials you use to login to mist.io, and then you'll be able to run the scripts::

    git clone https://github.com/mistio/mist.io-api-examples # clone the repository
    cd mist.io-api-examples
    virtualenv . # create a python virtualenv
    ./bin/pip install requests # install requests dependency
    vi list_machines.py # add EMAIL and PASSWORD
    ./bin/python list_machines.py # run script list_machines.py


SCRIPTS
-------

list_machines.py
~~~~~~~~~~~~~~~~

prints machines for all cloud added to mist.io .Shows machine name, state, machine cloud provider, machine size, launch time and price
Example output::

    *** Received 17 clouds and 10 machines. Time taken: 12 seconds ***
    *** Showing machine name, state, machine cloud provider, machine size, launch time and price ***
    *** size/launch time is EC2 specific but can easily be configured for any other provider ***
    *** machine price is what the machine has as tag price. Could easily be a value on the metadata as well ***


    NAME  - STATE  -  CLOUD PROVIDER  -  SIZE  -  LAUNCH TIME  -  PRICE
    --------------------------------------------------------------------

    timebit running EC2 N. Virginia 2013-06-15T19:51:26.000Z
    testingmachine running EC2 Tokyo 2015-12-18T18:05:17.000Z
    kvm-staging running Packet.net $37
    monitor.mgogoulos.gr running DigitalOcean $10
    lamp.mgogoulos.gr running DigitalOcean $10
    mean.mgogoulos.gr running DigitalOcean $10
    mean.mgogoulos.gr running DigitalOcean $10
    docker-server running EC2 AP Sydney 2015-05-23T13:07:41.000Z $44
    centos7-monitoring running EC2 AP Sydney 2015-05-24T13:40:11.000Z $44
    liveinspector.gr running KVM
    unweb.me running KVM
    redmine.engagemedia.org running KVM
    mgogoulos-dev.mist.io running EC2 Ireland 2014-05-23T13:07:22.000Z $44
    mgogoulos-azure.mist.io running Azure mgogoulos
    ubuntu-monitoring running GCE $11
    ansible-dev running OpenStack Athens
    test stopped OpenStack Athens
