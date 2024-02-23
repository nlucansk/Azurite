def generate_infrastructure(_app, _config):
    if "resource_group" in _config:
        from components.resource_group import ResourceGroupStack
        ResourceGroupStack(_app, "resource_group")
    else:
        print("### | >>> resource_group <<< not found ignoring!")

    if "storage_account" in _config:
        from components.storage_account import StorageAccountStack
        StorageAccountStack(_app, "storage_account")
    else:
        print("### | >>> storage_account <<< not found ignoring!")

    if "virtual_network" in _config:
        from components.virtual_network import NetworkStack
        NetworkStack(_app, "virtual_network")
    else:
        print("### | >>> virtual_network <<< not found ignoring!")

    if "container_registry" in _config:
        from components.container_registry import RegistryStack
        RegistryStack(_app, "container_registry")
    else:
        print("### | >>> container_registry <<< not found ignoring!")

    if "app_service_plan" in _config:
        from components.app_service_plan import AppServicePlanStack
        AppServicePlanStack(_app, "app_service_plan")
    else:
        print("### | >>> app_service_plan <<< not found ignoring!")