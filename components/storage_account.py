from constructs import Construct
from cdktf import TerraformStack

from cdktf_cdktf_provider_azurerm.data_azurerm_resource_group import DataAzurermResourceGroup
from cdktf_cdktf_provider_azurerm.storage_account import StorageAccount

from functions.azure_provider import prepare_azure_environment
from functions.get_config import get_config
from functions.base import print_info, generate_resource_tags


class StorageAccountStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        print_info(ns)
        config = get_config("config/config.yml")
        prepare_azure_environment(self, ns, config)

        for account in config['storage_account']:
            print("### | [{}] | Creating account {}!".format(ns, account['name']))
            data_resource_group = DataAzurermResourceGroup(
                self,
                "data-{}-{}-{}".format(
                    account['resource_group_name'],
                    account['location'],
                    account['name']
                ),
                name=account['resource_group_name']
            )
            storage_account = StorageAccount(
                self,
                "st-{}-{}-{}".format(
                    account['resource_group_name'],
                    account['location'],
                    account['name']
                ),
                name="st{}".format(account['name']),
                resource_group_name=data_resource_group.name,
                location=data_resource_group.location,
                account_tier=account['account_tier'],
                account_replication_type=account['account_replication_type'],
                tags=generate_resource_tags(account['tags'] if "tags" in account else None),
                cross_tenant_replication_enabled=account['cross_tenant_replication_enabled'] if "cross_tenant_replication_enabled" in account else None,
                access_tier=account['access_tier'] if "access_tier" in account else "Hot",
                enable_https_traffic_only=account['enable_https_traffic_only'] if "enable_https_traffic_only" in account else True,
                min_tls_version=account['min_tls_version'] if "min_tls_version" in account else "TLS1_2",
                allow_nested_items_to_be_public=account['allow_nested_items_to_be_public'] if "allow_nested_items_to_be_public" in account else True,
                shared_access_key_enabled=account['shared_access_key_enabled'] if "shared_access_key_enabled" in account else True,
                public_network_access_enabled=account['public_network_access_enabled'] if "public_network_access_enabled" in account else True,
                default_to_oauth_authentication=account['default_to_oauth_authentication'] if "default_to_oauth_authentication" in account else False,
                nfsv3_enabled=account['nfsv3_enabled'] if "nfsv3_enabled" in account else False
            )