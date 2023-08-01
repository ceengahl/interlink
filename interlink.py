# opens the json
# looks at the mutual connections
# compiles a list of all the people that they are connected to at different VC's
# composes a message with a list of the VC's and people we are trying to connect
# inputs the message in a cell the message should say (1. I feel like you know me well enough to do this 2. if you don't know about ruck, I can tell you about it 3. which of the following peoples are a good fit for ruck to reach out to for funding and that you're comfortable with.)
# creates 1. a familiar message 2. an unfamiliar message 3. a no message option.
# stores a json record of those that have been outreached to and prevents repeat message. CRITICAL


import json
import os

def network(json_file_path):

    with open(json_file_path, "r") as json_file:
        connect_map = json.load(json_file)

    first_degree_connectors = []
    first_degree_targets = []

    for vc in connect_map:
        if vc['people and connections'] != None:
            for target in vc['people and connections']:
                if target['degree'] == 2:
                    mutual_connections = target['connections']['1st connections']
                    for m in mutual_connections:
                        f_found = False
                        f_c  = -1
                        for f in first_degree_connectors:
                            f_c += 1
                            if m['name'] == f['name']:
                                f_found = True
                                break
                        if f_found == False:
                            first_degree_connectors.append({
                                'name': m['name'],
                                'info': m,
                                'connected vcs':[{
                                    'vc name': vc['vc']['name'],
                                    'info': {
                                        'linkedin': vc['vc']['linkedin'],
                                        'tagline': vc['vc tagline'],
                                        'overview': vc['vc overview']
                                    },
                                    '2nd degree connections':[
                                        target
                                    ]
                                }]
                                
                            })
                        else:
                            vc_found = False
                            f_vc_c = -1
                            for f_vc in first_degree_connectors[f_c]['connected vcs']:
                                f_vc_c += 1
                                if vc['vc']['name'] == f_vc['vc name']:
                                    vc_found = True
                                    break
                            if vc_found == False:
                                first_degree_connectors[f_c]['connected vcs'].append({
                                        'vc name': vc['vc']['name'],
                                        'info': {
                                            'linkedin': vc['vc']['linkedin'],
                                            'tagline': vc['vc tagline'],
                                            'overview': vc['vc overview']
                                        },
                                        '2nd degree connections':[
                                            target
                                        ]
                                    })
                            else:
                                first_degree_connectors[f_c]['connected vcs'][f_vc_c]['2nd degree connections'].append(target)

                elif target['degree'] == 1:
                    first_degree_targets.append(target)

    network = {
        'first degree connectors': sorted(first_degree_connectors, key=lambda x: x['name']),
        'first degree targets': sorted(first_degree_targets, key=lambda x: x['primary target']['name'])
    }

    output_file_path = json_file_path[:json_file_path.find('__emoticons')] + '__final_network_map.json'

    with open(output_file_path, 'w') as f:
        json.dump(network, f, indent=4)

    #remove previous file
    os.remove(json_file_path)

    print ('final network map saved to', output_file_path)

    
    return output_file_path

if __name__ == "__main__":
    network('connections.json')