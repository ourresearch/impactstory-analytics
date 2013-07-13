import json
import collections

def base():
    return {
        'chart': {
            'renderTo': 'container',
            'plotBackgroundColor': None,
            'backgroundColor': None,
            'spacingTop': 5,
            'legend': {
                'enabled': False
            }
        },
        'title': {'text': None},
        'subtitle': {'text': None},
        'yAxis': {
            'min': 0,
            'title':{
                'text': None
            },
            'gridLineColor': 'rgba(255, 255, 255, .1)'
        },
        "xAxis": {
          "lineColor": "rgba(0,0,0,0)"
        },
        'credits': {
            'enabled': False
        },
        'plotOptions': {
            'series': {
                'marker': {
                    'enabled': False
                }
            }
        },
    }


def timeseries_line():
    local_configs = {
        "chart": {
            "type": "line"
        },
        "xAxis": {
            "type": "datetime",
            "dateTimeLabelFormats": {
                "day": "%a"
            }
        },
        "series": []
    }

    return extend_base_configs(local_configs)


def streamgraph():
    local_configs = {
        "chart": {
            "type": "areaspline"
        },
        "plotOptions": {
            "series": {
                "pointPadding": 0,
                "groupPadding": 0,
                "shadow": False
            },
            "areaspline": {
                "stacking": "normal",
                "marker": {"enabled": False}
            }
        },
        "series": []
    }

    return extend_base_configs(local_configs)


def extend_base_configs(local_configs):
    configs = base()

    update_recursive(configs, local_configs)

    return configs


def update_recursive(d, u):
    """
    from http://stackoverflow.com/a/3233356/226013

    :param d: the orig dict; it'll be updated
    :param u: the new dict; will overwrite keys from d
    :return: the updated dict
    """
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update_recursive(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = u[k]
    return d


def as_js(dict):
    json_dirty = json.dumps(dict, indent=4)
    resp_lines = json_dirty.split("\n")
    resp_lines_clean = []
    for line in resp_lines:
        if "Date.UTC" in line:
            clean_line = line.replace('"', '')
        else:
            clean_line = line

        resp_lines_clean.append(clean_line)

    json_clean = "\n".join(resp_lines_clean)
    return json_clean
