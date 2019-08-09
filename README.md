# python-e3dc [![Build Status](https://travis-ci.com/MatrixCrawler/python-e3dc-module.svg?token=sAxTLMta2moxv8TwsFJ2&branch=master)](https://travis-ci.com/MatrixCrawler/python-e3dc-module)

A Python library for querying [E3/DC](https://www.e3dc.com/en/) systems trough an RSCP connection.  
This library aims to provide an interface to query an [E3/DC](https://www.e3dc.com/en/) solar power management system through the RSCP connection provided by the system.

## What do i need?

You'll need:

- Your username
- Your password
- The IP address of the E3/DC system
- The encryption key as set in the system preferences

## Usage
### Request single stat
    e3dc = E3DC('username', 'password', 192.168.1.123, 'my_secret_key')
    # request the current power that is produced by the pv system
    response = e3dc.send_request(RSCPTag.EMS_REQ_POWER_PV)
    print("Current power "+str(response.data))

### Send multiple requests at once
    e3dc = E3DC('username', 'password', 192.168.1.123, 'my_secret_key')
    responses = e3dc.send_requests(
                    [RSCPTag.EMS_REQ_BAT_SOC, RSCPTag.EMS_REQ_POWER_PV, RSCPTag.EMS_REQ_POWER_BAT,
                    RSCPTag.EMS_REQ_POWER_GRID, RSCPTag.EMS_REQ_POWER_WB_ALL])
    for response in responses:
        print("Response Tag: "+str(response.tag)+", response type: "+str(response.type)+",
            response data: "+str(response.data))

## Copyright notice
This module is based on https://github.com/fsantini/python-e3dc and distributed under a MIT License
