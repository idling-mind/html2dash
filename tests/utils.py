from dash.development.base_component import Component


def dash_to_dict(dash_component: Component) -> dict:
    """function to recursively convert dash components to dicts"""
    if isinstance(dash_component, Component):
        return_dict = {}
        for k, v in dash_component.to_plotly_json().items():
            if k == "props":
                return_dict[k] = {k: dash_to_dict(v) for k, v in v.items()}
            elif k == "children":
                return_dict[k] = [dash_to_dict(child) for child in v]
            else:
                return_dict[k] = v
        return return_dict
    elif isinstance(dash_component, list):
        return [dash_to_dict(child) for child in dash_component]
    return dash_component
