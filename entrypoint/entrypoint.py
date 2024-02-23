def generate_infrastructure(_app, _config):
    if "resource_group" in _config:
        from components.resource_group import ResourceGroupStack
        ResourceGroupStack(_app, "resource_group")
    else:
        print("### | >>> resource_group <<< not found ignoring!")

    if "virtual_network" in _config:
        from components.virtual_network import NetworkStack
        NetworkStack(_app, "virtual_network")
    else:
        print("### | >>> virtual_network <<< not found ignoring!")