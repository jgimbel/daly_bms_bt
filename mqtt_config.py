import json
from time import sleep

def handleCellVoltages (name, topic, val):
    vals = []
    for key, value in val.items():
        vals.append({
            'name': f'Cell {key}',
            'device_class': 'voltage',
            'state_topic': f'{topic}/state',
            'force_update': True,
            'unit_of_measurement': 'v',
            'value_template': f"{{{{value_json['{key}']}}}}",
            'uniq_id': f'{topic}-cell-{key}',
            'device': device
        })
    return vals

device = {
    'identifiers': ['76:67:02:01:14:56'],
    'name': 'Smart BMS'
}

topics = {
'Status': [
    lambda topic: {
        'name': 'Battery Cycles',
        'state_topic': f'{topic}/state',
        'force_update': True,
        'value_template': '{{value_json.cycles}}',
        'uniq_id': f'{topic}-cycles',
        'device': device
    }
],
'SOC': [
    lambda topic: {
        'name': 'Battery State of Charge',
        'device_class': 'battery',
        'state_topic': f'{topic}/state',
        'force_update': True,
        'unit_of_measurement': '%',
        'value_template': '{{value_json.soc_percent}}',
        'uniq_id': f'{topic}-soc',
        'device': device
    }, 
    lambda topic: {
        'name': 'Total Voltage',
        'device_class': 'voltage',
        'state_topic': f'{topic}/state',
        'force_update': True,
        'unit_of_measurement': 'v',
        'value_template': '{{value_json.total_voltage}}',
        'uniq_id': f'{topic}-total-voltage',
        'device': device
    }, 
    lambda topic: {
        'name': 'Power Use',
        'device_class': 'power',
        'state_topic': f'{topic}/state',
        'force_update': True,
        'unit_of_measurement': 'a',
        'value_template': '{{value_json.current}}',
        'uniq_id': f'{topic}-current',
        'device': device
    }
],
'CellVoltages': handleCellVoltages
}




def config(cmd, name, topic, val, base):
    if name in topics:
        if callable(topics[name]):
            topics[name] = topics[name](name, topic, val)
        for device in topics[name]:
            d = device(topic) if callable(device) else device
            msg = json.dumps(d)
            id = d['uniq_id']
            config_topic = f'{id}/config'
            cmd(config_topic, msg)

