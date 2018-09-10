#!/usr/bin/env python3

import json
import argparse
import sys
import getpass

from os.path import split as osplit
from os.path import join as ojoin
from os.path import dirname as odirname
from os.path import isfile as oisfile
from pathlib import Path

parser = argparse.ArgumentParser(description="""This script helps you to
export environment variables, using Terraform with different Subscriptions.
If you directly want to export variables use follwoing syntax:
eval `azure-sub-loader.py -s SUBSCRIPTION`""")
parser.add_argument(
    '-s', '--subscription',
    help='Subscription must be the same as in azure-sub-loader.json.'
)
parser.add_argument(
    '--show',
    required=False,
    action='store_true',
    help='Shows available subscriptions in config file.'
)
parser.add_argument(
    '-c', '--config',
    required=False,
    default=ojoin(Path.home(), '.az-sub-loader.json'),
    help='Path to config file, where subscription credentials are saved. '
         'default=~/.azure-sub-loader.json'
)
parser.add_argument(
    '-a', '--add-subscription',
    required=False,
    action='store_true',
    help='Adds new subscription to config file.'
)
parser.add_argument(
    '-d', '--delete-subscription',
    required=False,
    metavar="Subscription Name",
    help='Adds new subscription to config file.'
)

if (len(sys.argv) < 2):
    parser.print_help()
    sys.exit(0)

cmd_args = parser.parse_args()
SUBS = cmd_args.subscription
CFG_PATH = odirname(cmd_args.config)
CFG_FILE = osplit(cmd_args.config)[1]
SHOW = cmd_args.show
ADD_SUB = cmd_args.add_subscription
DEL_SUB = cmd_args.delete_subscription

exp_templ = """export TF_VAR_tenant_id={tenant_id}
export TF_VAR_subscription_id={subscription_id}
export TF_VAR_client_id={client_id}
export TF_VAR_client_secret={client_secret}"""


def _get_config(cfg_file_path):
    if oisfile(cfg_file_path):
        with open(cfg_file_path, 'r') as fh:
            return json.load(fh)
    return {}


def get_avail_subs(cfg_file_path):
    return _get_config(cfg_file_path).keys()


def get_sub_secrets(sub_name, cfg_file_path):
    config = _get_config(cfg_file_path)
    try:
        return config[sub_name]
    except KeyError as exc:
        return False


def add_sub_cfg(sub_name, tenant_id, sub_id,
                client_id, client_secret, cfg_file_path):
    config = _get_config(cfg_file_path)
    config[sub_name] = {
        "tenant_id": tenant_id,
        "subscription_id": sub_id,
        "client_id": client_id,
        "client_secret": client_secret
    }
    return config


def del_sub_cfg(sub_name, cfg_file_path):
    config = _get_config(cfg_file_path)
    config.pop(sub_name, None)
    return config


def main():
    config_file = ojoin(CFG_PATH, CFG_FILE)
    if SHOW:
        subs = get_avail_subs(config_file)
        print("Following subscriptions are availabe in your config:")
        print("\n".join(subs))
    elif ADD_SUB:
        print("New configuration entry will be created.")
        print("Please provide appropriate information:")
        sub_name = input("Subscription name: ")
        sub_id = input("Subscription ID: ")
        tenant_id = input("Tenant ID: ")
        client_id = input("Client ID: ")
        client_secret = getpass.getpass("Client Secret: ")
        new_cfg = add_sub_cfg(sub_name, tenant_id, sub_id,
                              client_id, client_secret, config_file)
        with open(config_file, 'w') as fh:
            json.dump(new_cfg, fh, indent=2)
    elif DEL_SUB:
        new_cfg = del_sub_cfg(DEL_SUB, config_file)
        with open(config_file, 'w') as fh:
            json.dump(new_cfg, fh, indent=2)

        print(f"{DEL_SUB} deleted.")
    else:
        variables = get_sub_secrets(SUBS, config_file)
        if variables:
            print(exp_templ.format(**variables))
        else:
            print(f"Subscription {SUBS} does not exist in config file.")


if __name__ == "__main__":
    main()
