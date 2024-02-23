from cdktf import AzurermBackend
from cdktf_cdktf_provider_azurerm.provider import AzurermProvider
import os


def prepare_azure_environment(_self, _ns, _config):
    AzurermProvider(
        _self,
        id="azure_provider",
        features={},
        tenant_id=os.environ['TENANT_ID'],
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET'],
        subscription_id=os.environ['SUBSCRIPTION_ID']
    )

    AzurermBackend(
        _self,
        tenant_id=os.environ['TENANT_ID'],
        client_id=os.environ['CLIENT_ID'],
        client_secret=os.environ['CLIENT_SECRET'],
        subscription_id=os.environ['SUBSCRIPTION_ID'],
        resource_group_name=_config['remote_backend']['resource_group_name'],
        storage_account_name=_config['remote_backend']['storage_account_name'],
        container_name=_config['remote_backend']['container_name'],
        key="{}-{}-{}.tfstate".format(
            _config['remote_backend']['key'],
            _config['general']['environment'],
            _ns
        )
    )