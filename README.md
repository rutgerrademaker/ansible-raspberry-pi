# Ansible script to provision a raspberry Pi

This is my first ansible project, it was created in order to learn a bit of ansible while configuring my new raspberry pi 5.
While not tested, most likely this will work just as wel on older models. All services run in Docker (compose).
This project is mostly a big note to my future self, in case my raspberry pi would die on me.

## Features

- [Ansible script to provision a raspberry Pi](#ansible-script-to-provision-a-raspberry-pi)
  - [Features](#features)
    - [Adminer](#adminer)
    - [Frigate NVR](#frigate-nvr)
    - [Grafana](#grafana)
    - [Gpodder](#gpodder)
    - [Home Assistant](#home-assistant)
    - [Immich](#immich)
    - [Minecraft server](#minecraft-server)
    - [Mosquitto](#mosquitto)
    - [Pi Hole](#pi-hole)
    - [Portainer CE](#portainer-ce)
    - [Prometheus](#prometheus)
      - [Node Exporter](#node-exporter)
    - [Traefik](#traefik)
    - [Unifi Network Application](#unifi-network-application)
  - [Miscellaneous](#miscellaneous)
    - [Coral TPU packages \& drivers](#coral-tpu-packages--drivers)
    - [Home Assistant + Mosquitto migration script](#home-assistant--mosquitto-migration-script)
  - [Prerequisites](#prerequisites)
    - [Install Ubuntu Server on the Pi](#install-ubuntu-server-on-the-pi)
    - [Inventory](#inventory)
    - [Secrets](#secrets)
  - [Usage](#usage)
  - [Wishlist / TODO](#wishlist--todo)
  - [Known issues](#known-issues)

### Adminer

Database management in a single PHP file (but then in docker).

- Web interface:
  - <http://adminer.pi4.home/>
  - <http://adminer.pi5.home/>

For now this only has access to the `immich` network.
It can be started from the `/data/adminer` directory with the `docker compose up -d` command.

### Frigate NVR

Monitor your security cameras with locally processed AI.

- Web interface: <http://frigate.home/>
- Docs: <https://docs.frigate.video/>

### Grafana

Media aggregator and podcast client/

- Web interface: <http://grfana.home/>
- Docs:
  - <https://grafana.com/>
  - <https://hub.docker.com/r/grafana/grafana>

### Gpodder

Media aggregator and podcast client/

- Web interface: <http://gpodder.home/>
- Docs:
  - <https://gpodder.github.io/>
  - <https://github.com/xthursdayx/gpodder-docker>

### Home Assistant

Open source home automation that puts local control and privacy first.

- Web interface: <http://hass.home/>
- Docs: <https://www.home-assistant.io/>
- Docs: <https://www.home-assistant.io/installation/raspberrypi/#docker-compose>
- Starts on (re)boot

### Immich

Self-hosted photo and video management solution.

- Web interface: <http://immich.home/>
- Docs: <https://immich.app/>

### Minecraft server

- See <https://github.com/itzg/docker-minecraft-bedrock-server>

### Mosquitto

An open source MQTT broker.

- See <https://mosquitto.org/>
- Used for IOT devices, used by to Home Assistant
- Provision users for my different IOT devices
- Starts on (re)boot

### Pi Hole

Network-wide Ad Blocking.
Urls are based on the configured `server_number` in the ansible inventory.

- Web interface:
  - <http://pihole.pi5.home/admin/>
  - <http://pihole.pi4.home/admin/>
- Docs: <https://pi-hole.net/>
- Docs: <https://github.com/pi-hole/docker-pi-hole>

### Portainer CE

Simplify Container Management Across Kubernetes and Docker

- Web interface:
  - <http://portainer.pi4.home/>
  - <http://portainer.pi5.home/>
- Docs: <https://www.portainer.io/>

### Prometheus

Monitoring system & time series database.

- Web interface:
  - <http://prometheus.home/>
- Docs: <https://hub.docker.com/u/prom>

#### Node Exporter

- Docs: <https://grafana.com/docs/grafana-cloud/send-data/metrics/metrics-prometheus/prometheus-config-examples/docker-compose-linux/>

### Traefik

Reverse proxy and ingress controller.

- Web interface:
  - <http://traefik.pi4.home/>
  - <http://traefik.pi5.home/>
- Docs: <https://traefik.io/>

### Unifi Network Application

Self-Hosted a UniFi Network Server.

- Web interface: <https://unifi.home:8443/>
- Docs <https://github.com/linuxserver/docker-unifi-network-application>

## Miscellaneous

### Coral TPU packages & drivers

Used for object detection in Frigate.

- <https://coral.ai/docs/accelerator/get-started/#runtime-on-linux>

### Home Assistant + Mosquitto migration script

The `migrate.yml` playbook will copy all data from an old pi (p4) to a new pi (p5)
It has to run as `root`, as some files (like HA's auth file) are owner by root on the source system.
As it was created after the whole playbook, I did not add this step to  playbook.yml.

## Prerequisites

### Install Ubuntu Server on the Pi

This script assumes:

- Ubuntu 24.04 is already installed on your Pi
- Next to root, you have an additional user/group (and password) we can configure a `system_user` and `system_group`
which can become `root`.
- You have SSH access to your Pi
- (local) DNS entries are created for the traefik domains

I used [Raspbery PI imager](https://ubuntu.com/download/raspberry-pi) but other methods should also work.

### Inventory

The repository assumes your `etc/ansible/hosts` file looks like e.g:

```yaml
homeserver:
  hosts:
    pi5:
      ansible_host: 10.0.0.53
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

More info: <https://docs.ansible.com/ansible/latest/vault_guide/vault_managing_passwords.html>

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

## Wishlist / TODO

- Install my custom Pi Hole blocklist (or latest backup).
- Install my custom Unifi configuration (or latest backup).
- Install letsencrypt SSL certificate(s).
- Scheduled backup for data directory to other server.
- Enable / configure ufw firewall.
- Finalize Automate creating DNS records in OpenWRT.
- Provision Home Assistant configuration files for solar / mqtt / modbus etc.
- Generalize DNS configuration (maybe local and/or public?).
- [WIP] Dynamically generate DNS records based on configured hosts
- Allow unifi to adopt devices via traefik on <http://unifi.home:8080> instead of IP address.
- Add Nextcloud?
- Add Jellyfin? (<https://jellyfin.org/>)
- Add Bitwarden? (<https://hub.docker.com/r/bitwarden/server>)
- Elk stack for logs (or prometheus?)
- Uptime kuma?
- Start minecraft server if someone tries to connect (or visits some website with a button to start it).
- Stop minecraft server at if no users are connected for x time.
- [WIP] Stop modifying docker compose (and other config) files on the target server by preparing them locally.
- Prometheus authentication.
- Install Prometheus node exporter on all hosts?

## Known issues

- Different services should probably use different users.
- MongoDB for Unifi should have secret password.
- I once ran into an issue when PiHole was not started some domains could not be resolved (which was fixed by manually starting pihole).
- Have not tested the full playbook "from scratch".
- Using `latest` versions of docker images is never recommended, I should know better.
- Quotes are not (yet) used consistent.
- immich .env file van not have $ in value, even if between " quotes
- Gpodder does not yet work as expected (using it as a sync server does not yet work)
- Portainer and Adminer might be to powerful to expose directly, maybe add extra/basic auth (via Traefik?)
- Parsing variables and secrets on the target each time is quite slow, and prone to error if a process is killed half way.
