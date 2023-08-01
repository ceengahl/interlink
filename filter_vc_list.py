import csv
import json

def filter_vcs(csv_file_path, target_stage, exclude_state_specific=True):
    def contains_state_name(string):
        state_names = [
            'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida',
            'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine',
            'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska',
            'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
            'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas',
            'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming'
        ]

        for state in state_names:
            if state.lower() in string.lower():
                return True
        return False

    output_filepath = csv_file_path[:csv_file_path.find('.csv')] + '---filtered.json'

    vc_raw = []
    # Read CSV file and convert rows to a list of dictionaries
    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            vc_raw.append(row)

    qualified = []
    c = 0
    for r in vc_raw:
        if exclude_state_specific:
            if not contains_state_name(r['description']):
                if target_stage.lower() in r['stage'].lower():
                    c += 1
                    print(r['name'])
                    qualified.append(r)
        else:
            if target_stage.lower() in r['stage'].lower():
                c += 1
                print(r['name'])
                qualified.append(r)


    with open(output_filepath, "w") as json_file:
        json.dump(qualified, json_file, indent=4)

    print(c, "VCs qualified. Initial VC list saved to json.")
    return {
        'response': 'ok',
        'output_filepath': output_filepath
    }

if __name__ == "__main__":
    results = filter_vcs("master_list_vcs.csv", 'pre-seed')
    print (results)