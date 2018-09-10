#!/usr/bin/env python3

import json
import argparse
import sys

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
    '-c', '--config',
    required=False,
    default=ojoin(Path.home(), '.azure-subscription-loader.json'),
    help='Path to config file, where subscription credentials are saved. '
         'default=~/.azure-sub-loader.json'
)
parser.add_argument(
    '--generate-config',
    required=False,
    action='store_true',
    help='Generates a simple configuration file. Prints to stdout.'
)

if (len(sys.argv) < 2):
    parser.print_help()
    sys.exit(0)

cmd_args = parser.parse_args()
SUBS = cmd_args.subscription
CFG_PATH = odirname(cmd_args.config)
CFG_FILE = osplit(cmd_args.config)[1]
GEN_CFG = cmd_args.generate_config

cfg_templ = {
    "SUBSCRIPTION_NAME": {
        "tenant_id": "id",
        "subscription_id": "id",
        "client_id": "id",
        "client_secret": "id"
    },
    "NEXT_SUBSCRIPTION_NAME": {
        "tenant_id": "id",
        "subscription_id": "id",
        "client_id": "id",
        "client_secret": "id"
    }
}

exp_templ = """export TF_VAR_tenant_id={tenant_id}
export TF_VAR_subscription_id={subscription_id}
export TF_VAR_client_id={client_id}
export TF_VAR_client_secret={client_secret}"""


def main():
    if GEN_CFG:
        # Check if config file already exists and ask to overwrite
        if oisfile(ojoin(CFG_PATH, CFG_FILE)):
            print("Configuration file already exists.")
            answere = input("Do you want to overwrite? Only 'yes' will work. ")
            if answere == "yes":
                with open(ojoin(CFG_PATH, CFG_FILE), 'w') as fh:
                    json.dump(cfg_templ, fh, indent=2)
            else:
                print("No config file generated.")
        else:
            with open(ojoin(CFG_PATH, CFG_FILE), 'w') as fh:
                json.dump(cfg_templ, fh, indent=2)
    else:
        with open(ojoin(CFG_PATH, CFG_FILE), 'r') as fh:
            config = json.load(fh)

        try:
            sub = config[SUBS]
        except KeyError as exc:
            print(f"Subscription {SUBS} does not exist in config file.")
            sys.exit(1)
        else:
            try:
                print(exp_templ.format(
                    tenant_id=sub['tenant_id'],
                    subscription_id=sub['subscription_id'],
                    client_id=sub['client_id'],
                    client_secret=sub['client_secret']))
            except KeyError as exc:
                print(f"Configuration for {SUBS} is missing.")
                print("Please add all neccesary parameters or use"
                      " --generate-config to get a sample configuration.")


if __name__ == "__main__":
    main()
