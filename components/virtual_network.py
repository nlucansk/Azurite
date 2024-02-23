from constructs import Construct
from cdktf import TerraformStack, TerraformResourceLifecycle, Token

from cdktf_cdktf_provider_azurerm.data_azurerm_resource_group import DataAzurermResourceGroup
from cdktf_cdktf_provider_azurerm.virtual_network import VirtualNetwork
from cdktf_cdktf_provider_azurerm.subnet import Subnet, SubnetDelegation, SubnetDelegationServiceDelegation


from functions.azure_provider import prepare_azure_environment
from functions.get_config import get_config
from functions.base import print_info, generate_resource_tags


class NetworkStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        print_info(ns)
        config = get_config("config/config.yml")
        prepare_azure_environment(self, ns, config)

        for network in config['virtual_network']:
            print("### | [{}] | Creating network {}!".format(ns, network['name']))
            data_resource_group = DataAzurermResourceGroup(
                self,
                "data-{}-{}-{}".format(
                    network['resource_group_name'],
                    network['location'],
                    network['name']
                ),
                name=network['resource_group_name']
            )
            virtual_network = VirtualNetwork(
                self,
                "vnet-{}-{}-{}".format(
                    config['general']['environment'],
                    network['location'],
                    network['name']
                ),
                name="vnet-{}-{}-{}".format(
                    config['general']['environment'],
                    network['location'],
                    network['name']
                ),
                location=data_resource_group.location,
                resource_group_name=data_resource_group.name,
                address_space=network['address_space'],
                dns_servers=network['dns_servers'] if "dns_servers" in network else None,
                tags=generate_resource_tags(network['tags'] if "tags" in network else None),
                lifecycle=TerraformResourceLifecycle(
                    ignore_changes=['tags']
                )
            )
            if "subnets" in network:
                for subnet in network['subnets']:
                    print("### | [{}] | Creating subnet {}!".format(ns, subnet['name']))
                    subnet_delegation = []
                    if "delegations" in subnet:
                        for delegation in subnet['delegations']:
                            print("### | [{}] | Creating subnet delegation {}!".format(ns, delegation['name']))
                            subnet_delegation.append(
                                SubnetDelegation(
                                    name=delegation['name'],
                                    service_delegation=SubnetDelegationServiceDelegation(
                                        name=delegation['service_delegation']
                                    )
                                )
                            )
                    Subnet(
                        self,
                        "subnet-{}-{}-{}".format(
                            config['general']['environment'],
                            network['location'],
                            subnet['name']
                        ),
                        name=subnet['name'],
                        resource_group_name=data_resource_group.name,
                        virtual_network_name=virtual_network.name,
                        address_prefixes=subnet['address_space'],
                        delegation=subnet_delegation if subnet_delegation else None,
                    )
