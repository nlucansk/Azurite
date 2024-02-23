from constructs import Construct
from cdktf import TerraformStack, TerraformResourceLifecycle
from cdktf_cdktf_provider_azurerm.data_azurerm_resource_group import DataAzurermResourceGroup
from cdktf_cdktf_provider_azurerm.service_plan import ServicePlan
from cdktf_cdktf_provider_azurerm.app_service_certificate import AppServiceCertificate
from cdktf_cdktf_provider_azurerm.data_azurerm_key_vault import DataAzurermKeyVault
from cdktf_cdktf_provider_azurerm.data_azurerm_key_vault_secret import DataAzurermKeyVaultSecret

# Custom Logic
from functions.base import print_info, generate_resource_tags
from functions.azure_provider import prepare_azure_environment
from functions.get_config import get_config


class AppServicePlanStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        print_info(ns)
        config = get_config("config/config.yml")
        prepare_azure_environment(self, ns, config)

        if "app_service_plan" in config:
            for asp in config['app_service_plan']:
                data_resource_group = DataAzurermResourceGroup(
                    self,
                    "data-{}-{}-{}".format(
                        asp['resource_group_name'],
                        asp['location'],
                        asp['name']
                    ),
                    name=asp['resource_group_name']
                )

                asp_plan = ServicePlan(
                    self,
                    "plan-{}-{}-{}".format(
                        config['general']['environment'],
                        asp['location'],
                        asp['name'],
                    ),
                    name="plan-{}-{}".format(
                        config['general']['environment'],
                        asp['name'],
                    ),
                    location=data_resource_group.location,
                    resource_group_name=data_resource_group.name,
                    os_type=asp['os_type'],
                    sku_name=asp['sku_name'],
                    per_site_scaling_enabled=asp['per_site_scaling_enabled'],
                    worker_count=asp['worker_count'],
                    tags=generate_resource_tags(asp['tags'] if "tags" in asp else None),
                    lifecycle=TerraformResourceLifecycle(
                        ignore_changes=['tags']
                    ),
                    depends_on=[
                        data_resource_group
                    ]
                )

                if "certificates" in asp:
                    for certificate in asp['certificates']:
                        print("### | [{}] | Adding certificate [{}] from [{}]".format(
                            ns,
                            certificate['key_vault_secret'],
                            certificate['key_vault_name']
                        ))
                        data_keyvault = DataAzurermKeyVault(
                            self,
                            "data-keyvault-{}-{}-{}-{}".format(
                                config['general']['environment'],
                                asp['location'],
                                asp['name'],
                                certificate['key_vault_secret']
                            ),
                            name=certificate['key_vault_name'],
                            resource_group_name=certificate['key_vault_resource_group_name']
                        )

                        data_keyvault_secret = DataAzurermKeyVaultSecret(
                            self,
                            "data-keyvaultsecret-{}-{}-{}-{}".format(
                                config['general']['environment'],
                                asp['location'],
                                asp['name'],
                                certificate['key_vault_secret']
                            ),
                            name=certificate['key_vault_secret'],
                            key_vault_id=data_keyvault.id
                        )

                        AppServiceCertificate(
                            self,
                            "plan-cert-{}-{}-{}-{}".format(
                                config['general']['environment'],
                                asp['location'],
                                asp['name'],
                                certificate['key_vault_secret']
                            ),
                            name=data_keyvault_secret.name,
                            resource_group_name=asp_plan.resource_group_name,
                            location=asp_plan.location,
                            key_vault_secret_id=data_keyvault_secret.id,
                            depends_on=[
                                asp_plan
                            ],
                            lifecycle=TerraformResourceLifecycle(
                                ignore_changes=['key_vault_secret_id']
                            )
                        )
