# az-sub-loader

This script provides an easy to use interface to set the right variables
for using [Terraform](https://terraform.io).

## Requirements

`Python >= 3`

## Example usage

If you are using this script for the first time. You have to generate a basic
configuration.

```bash
./az-sub-loader.py --generate-config
```

This will generate the configuration file under your `$HOME/.az-sub-loader.json`

### Sample configuration file

```json
{
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
```

You should edit this configuration file appropriate.
It is a good advice to use the subscription name as the root object but it is not mandatory.

To generate those ID's please consult the Microsoft Azure documentation.

 [Create an Azure service principal with Azure CLI 2.0](https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli)

## ToDos

- Generation of new Service Principals
- Adding Service Principals to config file
