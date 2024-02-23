from constructs import Construct
from cdktf import TerraformStack, Token, TerraformResourceLifecycle
from cdktf_cdktf_provider_azurerm.data_azurerm_resource_group import DataAzurermResourceGroup
from cdktf_cdktf_provider_azurerm.container_registry import ContainerRegistry, ContainerRegistryIdentity

from functions.base import print_info, generate_resource_tags
from functions.azure_provider import prepare_azure_environment
from functions.get_config import get_config


class RegistryStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        print_info(ns)
        config = get_config("config/config.yml")
        prepare_azure_environment(self, ns, config)
        null_value = Token.as_string(Token.null_value())

        for registry in config['container_registry']:
            data_resource_group = DataAzurermResourceGroup(
                self,
                "data-{}-{}-{}".format(
                    registry['resource_group_name'],
                    registry['location'],
                    registry['name']
                ),
                name=registry['resource_group_name']
            )

            ContainerRegistry(
                self,
                "cr-{}-{}-{}".format(
                    registry['resource_group_name'],
                    registry['location'],
                    registry['name']
                ),
                name="cr{}{}".format(
                    config['general']['environment'],
                    registry['name']
                ),
                resource_group_name=data_resource_group.name,
                location=data_resource_group.location,
                sku=registry['sku'],
                admin_enabled=registry['admin_enabled'],
                identity=ContainerRegistryIdentity(
                    type="SystemAssigned"
                ),
                tags=generate_resource_tags(registry['tags'] if "tags" in registry else None),
                lifecycle=TerraformResourceLifecycle(
                    ignore_changes=['tags', 'identity']
                )
            )
