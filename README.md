# Ansible script to provision a raspberry Pi

This is my first ansible project, it was created in order to learn a bit of ansible while configuring my new raspberi pi 5.
While not tested, most likely this will work just as wel on older models. All services run in Docker (compose).
This project is mostly a big note to my future self, in case my raspberry pi would die on me.

## Features

- [Ansible script to provision a raspberry Pi](#ansible-script-to-provision-a-raspberry-pi)
  - [Features](#features)
    - [Adminer](#adminer)
    - [Pi Hole](#pi-hole)
    - [Home Assistant](#home-assistant)
    - [Mosquitto](#mosquitto)
    - [Unifi Network Application](#unifi-network-application)
    - [Minecraft server](#minecraft-server)
    - [Frigate NVR](#frigate-nvr)
    - [Traefik](#traefik)
    - [Immich](#immich)
  - [Miscellaneous](#miscellaneous)
    - [Coral TPU packages \& drivers](#coral-tpu-packages--drivers)
    - [Home Assistant + Mosquitto migration script](#home-assistant--mosquitto-migration-script)
  - [Prerequisites](#prerequisites)
    - [Install Ubuntu Server on the Pi](#install-ubuntu-server-on-the-pi)
    - [Inventory](#inventory)
    - [Secrets](#secrets)
  - [Usage](#usage)
  - [Known issues](#known-issues)
  - [Wishlist / TODO](#wishlist--todo)

### Adminer

Database management in a single PHP file.
Urls are based on the configured `server_name` in the ansible inventory.
- Web interface:
  - http://adminer.pi5.home/

For now this only has access to the `immich` network.

### Pi Hole

Network-wide Ad Blocking. 
Urls are based on the configured `server_number` in the ansible inventory.

- Web interface:
  - http://pihole.pi5.home/admin/
  - http://pihole.pi4.home/admin/
  - http://pihole.pi1.home/admin/
- Docs: https://pi-hole.net/
- Docs: https://github.com/pi-hole/docker-pi-hole

### Home Assistant

Open source home automation that puts local control and privacy first.

- Web interface: http://hass.local/
- Docs: https://www.home-assistant.io/
- Docs: https://www.home-assistant.io/installation/raspberrypi/#docker-compose
- Starts on (re)boot

### Mosquitto

An open source MQTT broker.

- See https://mosquitto.org/
- Used for IOT devices, used by to Home Assistant
- Provision users for my different IOT devices
- Starts on (re)boot

### Unifi Network Application

Self-Hosted a UniFi Network Server.

- Web interface: http://unifi.local/
- Docs https://github.com/linuxserver/docker-unifi-network-application
- Starts on (re)boot

### Minecraft server

- See https://github.com/itzg/docker-minecraft-bedrock-server

### Frigate NVR

Monitor your security cameras with locally processed AI.

- Web interface: http://frigate.local/
- Docs: https://docs.frigate.video/

### Traefik

Reverse proxy and ingress controller.

- Web interface: http://traefik.local/
- Docs: https://traefik.io/

### Immich

Self-hosted photo and video management solution.

- Web interface: http://immich.local/
- Docs: https://immich.app/

## Miscellaneous

### Coral TPU packages & drivers

Used for object detection in Frigate.

- https://coral.ai/docs/accelerator/get-started/#runtime-on-linux

### Home Assistant + Mosquitto migration script

The `migrate.yml` playbook will copy all data from an old pi (p4) to a new pi (p5)
It has to run as `root`, as some files (like HA's auth file) are owner by root on the source system.
As it was created after the whole playbook, I did not add this step to  playbook.yml.

## Prerequisites

### Install Ubuntu Server on the Pi

This script assumes:

- Ubuntu 24.04 is already installed on your Pi
- Next to root, you have an addtional user/group (and password) we can configure a `system_user` and `system_group` 
which can become `root`.
- You have SSH access to your Pi
- (local) DNS entries are created for the traefik domains

I used [Raspbery PI imager](https://ubuntu.com/download/raspberry-pi) but other methods should also work.

### Inventory

The repository assumes your `etc/ansible/hosts` file looks like e.g:

```yaml
pi5:
  hosts:
    10.0.0.53:
      system_user: rutger
      system_group: rutger
      dns_1: "1.1.1.1"
      dns_2: "1.0.0.1"      
      eth0_ip: "10.0.0.53/24"
      wlan0_ip: "10.0.0.54/24"
      gateway_ip: "10.0.0.1"
      usb_modbus_id: "usb-FTDI_FT232R_USB_UART_xxxxxx-if00-port0"
      usb_p1_id: "usb-FTDI_FT232R_USB_UART_xxxxxx-if00-port0"
      usb_zigbee_id: "usb-ITead_Sonoff_Zigbee_3.0_USB_Dongle_Plus_xxxxx-port0"
```

### Secrets

Create an ansible vault file containing the following entries:

```yaml
network_wifi_ssid: "your_wifi_ssid"
network_wifi_password: "your wifi password"

mosquitto_mosquitto_pass: "YourSecretMosquittoPassword"
mosquitto_homeassistant_pass: "YourSecretMosquittoHomeAssistantPassword"
mosquitto_shelly_pass: "YourSecretMosquittoShellyPassword"
mosquitto_opendtu_pass: "YourSecretMosquittoOpenDTUPassword"
mosquitto_frigate_pass: "YourSecretMosquittoFrigatePassword"

frigate_rtsp_password: "YourSecretFrigateRtspPassword"

pihole_webpassword: "YourSecretPiHolePassword"

immich_db_username: "immich"
immich_db_password: "YourSecretImmichDbPassword"
```

```shell
# To create a vault
ansible-vault create ./.secrets/vault.yml 

# To add/edit secrets
ansible-vault edit ./.secrets/vault.yml
```

More info: https://docs.ansible.com/ansible/latest/vault_guide/vault_managing_passwords.html

## Usage

```shell
 ansible-playbook \
     --ask-become-pass \
     --ask-vault-pass \
     -e @.secrets/vault.yml \
    playbook.yml
```

This will then ask for the sudo password of the user and the password for your vault file.
If you trust yourself saving these in plain text on your local machine you can also execute the playbooks like this:

```shell
 ansible-playbook \
    --become-password-file .secrets/sudo.pass \
    --vault-password-file .secrets/vault.pass \
    -e @.secrets/vault.yml \
    playbook.yml
```

## Known issues

- Different services should probably use different users.
- MongoDB for Unifi should have secret password.
- I once ran into an issue when PiHole was not started some domains could not be resolved (which was fixed by manually starting pihole).
- Have not tested the full playbook "from scratch".
- Using `latest` versions of docker images is never recommended, I should know better.
- Quotes are not (yet) used consistent.
- Unifi users can nog log in via unifi.local
- .local domains should change as this is a reserver tld.
- immich .env file van not have $ in value, even if between " quotes
- Gpodder does not yet work as expected (using it as a sync server does not yet work)
- Portainer and Adminer might be to powerful to expose directly, maybe add exta/basic auth (via Traefik?)

## Wishlist / TODO

- Install my custom Pi Hole blocklist (or latest backup).
- Install my custom Unifi configuration (or latest backup).
- Install letsencrypt SSL certificate(s).
- Scheduled backup for data directory to other server.
- Enable / configure firewall.
- Automate creating DNS records in OpenWRT.
- Provison Home Assistant configuration files for solar / mqtt / modbus etc.
- Generalize DNS configuration (maybe local and/or public?).
- Allow unifi to adopt devices via traefik on http://unifi.local:8808 instead of IP address.
- Add Nextcloud?