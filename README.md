# Ansible script to provision a raspberry Pi

This is my first ansible project, it was created in order to learn a bit of ansible while configuring my new raspberi pi 5.
While not tested, most likely this will work just as wel on older models. All services run in Docker (compose).
This project is mostly a big note to my future self, in case my raspberry pi would die on me.

## Features

- [Pi Hole](#pi-hole)
- [Home Assistant](#home-assistant)
- [Mosquitto](#mosquitto)
- [Unify Network Application](#unify-network-application)
- [Minecraft Server](#minecraft-server)
- [Frigate NVR](#frigate-nvr)
- [Home Assistant + Mosquitto migration script](#home-assistant--mosquitto-migration-script)

### Pi Hole

- Web interface: http://10.0.0.53:1080/admin
- See https://pi-hole.net/
- See https://github.com/pi-hole/docker-pi-hole
- Starts on (re)boot

### Home Assistant

- Web interface: http://10.0.0.53:8123
- See https://www.home-assistant.io/
- See https://www.home-assistant.io/installation/raspberrypi/#docker-compose
- Starts on (re)boot

### Mosquitto

- See https://mosquitto.org/
- Used for IOT devices, used by to Home Assistant
- Provision users for my different IOT devices
- Starts on (re)boot

### Unify Network Application

- Web interface: https://10.0.0.53:8443
- See https://github.com/linuxserver/docker-unifi-network-application
- Starts on (re)boot

### Minecraft server

- See https://github.com/itzg/docker-minecraft-bedrock-server
- Must be started and stopped manually

```shell
# Start minecraft server
cd /data/minecraft server && docker compose up -d

# Stop minecraft server
cd /data/minecraft server && docker compose down
```

### Frigate (NVR)

- http://10.0.0.53:5000/
- https://docs.frigate.video/

### Home Assistant + Mosquitto migration script

The `migrate.yml` playbook will copy all data from an old pi (p4) to a new pi (p5)
It has to run as `root`, as some files (like HA's auth file) are owner by root on the source system.
As it was created after the whole playbook, I did not add this step to  playbook.yml.

### Traefik (WIP)

- See https://traefik.io/

End goal here is to use domains instead of ip addresses and portnumbers, one day.

## Prerequisites

### Install Ubuntu Server on the Pi

This script assumes:

- Ubuntu 24.04 is already installed on your Pi
- Next to root, you have an addtional user/group (and password) we can configure a `system_user` and `system_group` 
which can become `root`.
- You have SSH access to your Pi

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

Create an ansible secrets file containing the following entries:

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
```

e.g: ./secrets/vault.yml

## Usage

```shell
 ansible-playbook playbook.yml \
    -e @.secrets/vault.yml
```

This will then ask for the sudo password of the user and the password for your vault file.
If you trust yourself saving these in plain text on your local machine you can also execute the playbooks like this:

```shell
 ansible-playbook playbook.yml \
    -e @.secrets/vault.yml \
    --become-password-file ~/.secrets/sudo.pass \
    --vault-password-file ~/.secrets/vault.pass
```

## Known issues

- Default network now uses WIFI as I don't have a network cable to where my PI is located (yet).
- Traefik is WIP.
- Different services should probably use different users and networks.
- MongoDB for Unify should have secret password.
- I once ran into an issue when PiHole was not started some domains could not be resolved (which was fixed by manually starting pihole).
- When a compose file is updated services should be manually restarted.
- Have not tested the full playbook "from scratch".
- Using `latest` versions of docker images is never recommended, I should know better.

## Wishlist / TODO

- Install my custom PiHole blocklist (or latest backup).
- Install my custom Unify configuration (or latest backup).
- Install letsencrypt SSL certificate(s).
- Finish Traefik.
- Scheduled backup for data directory to other server.
- Enable / configure firewall.
- Install some camera's for Frigate