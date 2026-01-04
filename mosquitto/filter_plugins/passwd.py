"""Script to create a password file for Mosquitto with Ansible."""

# Source: https://shantanoo-desai.github.io/posts/technology/mosquitto_ansible_passgen/

import dataclasses
from ansible.errors import AnsibleError
try:
    import passlib.hash
except Exception as e:
    raise AnsibleError('this script requires the passlib pip package installed') from e

def mosquitto_passwd(passwd):
    """Encrypt a mosquitto password."""

    salt_size_value = 12
    iterations_value = 101

    digest = passlib.hash.pbkdf2_sha512.using(salt_size=salt_size_value, rounds=iterations_value) \
        .hash(passwd) \
        .replace("pbkdf2-sha512", "7") \
        .replace(".", "+")

    return digest + "=="

@dataclasses.dataclass
class FilterModule():
    """Filter Module"""

    @staticmethod
    def filters():
        """List of filters"""
        return {
            'mosquitto_passwd': mosquitto_passwd,
        }
