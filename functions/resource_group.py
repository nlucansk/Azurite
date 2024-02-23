#!/usr/bin/env python
from cdktf import TerraformResourceLifecycle
# Resource Group Logic
from cdktf_cdktf_provider_azurerm.resource_group import ResourceGroup
from cdktf_cdktf_provider_azurerm.data_azurerm_resource_group import DataAzurermResourceGroup


def create_resource_group(_self, _environment, _location, _name, _tags=None):
    return ResourceGroup(
        _self,
        "rg-{}-{}-{}".format(
            _environment,
            _location,
            _name
        ),
        name="rg-{}-{}-{}".format(
            _environment,
            _location,
            _name
        ),
        location=_location,
        tags=_tags,
        lifecycle=TerraformResourceLifecycle(
            ignore_changes=['tags']
        )
    )


def get_resource_group(_self, _resource, _resource_group_name):
    return DataAzurermResourceGroup(
        _self,
        "data-{}-{}".format(_resource, _resource_group_name),
        name=_resource_group_name
    )