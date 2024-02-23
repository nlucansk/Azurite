#!/usr/bin/env python
from constructs import Construct
from cdktf import TerraformStack
# Custom Logic
from functions.azure_provider import prepare_azure_environment
from functions.get_config import get_config
from functions.base import print_info
from functions.resource_group import create_resource_group, generate_resource_tags


class ResourceGroupStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        print_info(ns)
        config = get_config("config/config.yml")
        prepare_azure_environment(self, ns, config)

        for rg in config['resource_group']:
            print("### | [{}] | Creating resource group [rg-{}-{}-{}].".format(
                ns,
                config['general']['environment'],
                rg['location'],
                rg['name']
            ))
            create_resource_group(
                self,
                config['general']['environment'],
                rg['location'],
                rg['name'],
                generate_resource_tags(rg['tags'] if "tags" in rg else None)
            )