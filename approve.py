'''
read from output file from interlink
identify all the VC's and their summarizing data from the interlinked list
save list and description to CSV, looking for approval.

then gets the list of people from interlink
save list to csv with info and have approval column

take both VC list and individuals list and compile them together and create request message
user is to copy and paste into linkedin messages or where ever, then mark as completed.
'''

import json
import csv



def save_json_to_csv(json_data, csv_file_path):
    keys = json_data[0].keys()

    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(json_data)


def csv_to_json(csv_file_path):

    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        data = [row for row in reader]

    return data


def prepare_approval(interlinked_filepath):

    print ('prepping approval lists of interlinked VCs and First Degrees')
    with open(interlinked_filepath, "r") as json_file:
            connections_list = json.load(json_file)

    vcs = []
    people = []

    for connection in connections_list['first degree connectors']:
        p = {
                'name': connection['name'],
                'li_url': connection['info']['profile_url'],
                'title': connection['info']['title'],
                'approved': ''
        }   

        if p not in people:
            people.append(p)

        for vc in connection['connected vcs']:
            v = {
                'name': vc['vc name'],
                'tagline': vc['info']['tagline'],
                'overview': vc['info']['overview'],
                'li_url': vc['info']['linkedin'],
                'approved': ''
            }

            if v not in vcs:
                vcs.append(v)
    
    approved_people_filepath = 'approve_people.csv'
    approved_vcs_filepath = 'approve_vcs.csv'

    save_json_to_csv(people, approved_people_filepath)
    save_json_to_csv(vcs, approved_vcs_filepath)

    print (f"approval CSVs have been prepared, please open both `{approved_people_filepath}` and `{approved_vcs_filepath}` to mark the people and VCs you would like to approve outreach to.")

    return approved_people_filepath, approved_vcs_filepath


def compose(f):

    print (f"composing message for {f['name'].title()}")

    first_name = f['name'][:f['name'].find(' ')].title()
    intro_msg = f"{first_name}, I have been building Ruck for a bit now, and I think we are ready to raise a solid pre-seed round. I have been diving through LinkedIn to find all the different funds and the people that can connect me into those funds. Basically, I found connections that you may be able to help me with. \n\nI know that a lot of your LinkedIn connections may not be people you have actually met, but would you be opposed to looking at this list of and seeing if you're in a position to help me get in contact to start schedule a pitch for mid August?\n\nAlso, I'm not sure if these are the best people to contact. I just programmatically when through and found people that seemed to be decision makers at funds in a huge list. If you think these are not good contacts, please let me know!\n\n"

    contact_list_msg = ''

    tempstring = ''
    for r in f['approved vc requests']:
        tempstring = f"{r['target vc']} - {r['target 2nd connection']['name'].title()}"
        contact_list_msg += f'\n{tempstring}'

    result = intro_msg + contact_list_msg

    return result


def compile_approvals(approved_people_filepath, approved_vcs_filepath, interlinked_filepath):

    try:

        approved_people = csv_to_json(approved_people_filepath)
        approved_vcs = csv_to_json(approved_vcs_filepath)

        with open(interlinked_filepath, "r") as json_file:
            data = json.load(json_file)

    except Exception as e:
        print ('error opening files: ', e)
        return None

    list_of_1sts = []
    all_keys = []

    approved_first_degrees = []

    for c in data['first degree connectors']:
        name = c['name']
        approved_vc_requests = []
        for p in approved_people:
            if name.lower() == p['name'].lower():
                # p['approved'] = True #testing only
                if p['approved'] == True:
                    for vc in c['connected vcs']:
                        vc_name = vc['vc name']
                        for v in approved_vcs:
                            if vc_name.lower() == v['name'].lower():
                                # v['approved'] = True #testing only
                                if v['approved'] == True:
                                    target = vc['2nd degree connections'][0]['primary target']
                                    try:
                                        role = target['role'].title()
                                    except:
                                        role = ''
                                    approved_vc_requests.append({
                                        'target vc': vc['vc name'],
                                        'target 2nd connection': {
                                            'name': target['name']['name'].title(),
                                            'role': role
                                        }
                                    })

                    if len(approved_vc_requests) > 0:
                        p['approved vc requests'] = approved_vc_requests
                        approved_first_degrees.append(p)

    if len(approved_first_degrees) > 0:
        for q in approved_first_degrees:
            q['message'] = compose(q)

        final_filepath = 'final_approved_outbound_requests.csv'

        save_json_to_csv(approved_first_degrees, final_filepath)


        print (f"Final outbound CSV has been exported successfully to `{final_filepath}`. You may use the CSV to copy and paste outbound messages to your first degree connections.")

        return final_filepath
    
    else:

        print (f'''
               {'*'*10} ERROR {'*'*10}
               No approved outbound requests were found, please check approval CSVs, `{approved_people_filepath}` and `{approved_vcs_filepath}`, to ensure that you marked TRUE or FALSE under the `approved` columns.
               {'*'*20}
               ''')

if __name__ == '__main__':
    # prepare_approval()
    # compile_approvals()()
    print ('debug complete')