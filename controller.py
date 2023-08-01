import json

import clean
import interlink
import find_connections
import approve
import filter_vc_list

default_connections_filepath = 'connections.json'

def filter_csv_to_json(csv_path, stage):
    output_filepath = filter_vc_list.filter_vcs(csv_path, stage)
    
    return output_filepath

def find_connections_for_vcs(json_file_path, target_connections_count):

    def export():
        response = input("Would you like to export to approval CSV? (y/n): ")

        responded = False

        #gets the target amout to connect with
        while responded == False:
            if (response.lower() == 'y') or (response.lower() == 'yes'):
                responded = True
                return True

            elif (response.lower() == 'n') or (response.lower() == 'no'):
                responded = True
                return False
            
            else:
                print("Invalid input. Please enter 'y' or 'n'.")


    with open(json_file_path, "r") as json_file:
        data = json.load(json_file)

    driver = None

    try:
        connections_file_path, driver = find_connections.connect_with_vcs(data, False, target_connections_count)

        print ('list of VCs parsed, results in filepath:', connections_file_path)
        
        approval = export()

        if approval:
            export_connections()
 
    except Exception as e:
        print ('linkedin scrape failed, error:', e)

    # Check if driver is assigned and close it if necessary
    if driver is not None:
        driver.quit()



def export_connections(preview = False):

    connections_file_path = 'connections.json'

    try:
        demoticoned_path = clean.clean_json_file(connections_file_path)
        
        try:
            interlinked_filepath = interlink.network(demoticoned_path)

            if preview == False:

                try:
                        approved_people_filepath, approved_vcs_filepath = approve.prepare_approval(interlinked_filepath)

                        final_approved_filepath = approve.compile_approvals(approved_people_filepath, approved_vcs_filepath, interlinked_filepath)

                        return final_approved_filepath

                except Exception as e:
                    print ('error creating approval sheet:', e)

            else:
                with open(interlinked_filepath, "r") as json_file:
                    connections_list = json.load(json_file)

                print ('Preview data in debugger window.')


        except Exception as e:
                print ('error interlinking connections:', e)

    except Exception as e:
        print ('error with saving to demoticon file:', e)




def action_prompt(options):
    for i, option in enumerate(options):
        print(f"{i+1}. {option}")

    choice = None
    while choice is None:
        try:
            user_choice = int(input("Enter your choice (number): ").strip())
            if 1 <= user_choice <= len(options):
                choice = user_choice
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Invalid choice. Please enter a number.")

    return choice


def initialize():

    def get_target_connections_count():
        response = input("Parse entire list? (y/n): ")

        target_connections_count = None

        #gets the target amout to connect with
        if (response.lower() == 'y') or (response.lower() == 'yes'):
            target_connections_count = 0

        elif (response.lower() == 'n') or (response.lower() == 'no'):
            while target_connections_count is None:
                try:
                    target_connections_count = int(input("Please enter target amount of connections (number):"))

                except ValueError:
                    print("Invalid choice. Please enter a number.")
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

        return target_connections_count
    
    options = [
        'Filter new list of VCs', 
        'Continue parsing existing list of VCs', 
        'Preview/Print connections (DEBUGGER ONLY)',
        'Export VC connections to approval CSVs']
    
    
    print ('\n' *2)
    print('*'*60)
    print('*'*60)
    print('*'*60)
    print ('\nINTERLINK\n')
    print('*'*60)
    print('*'*60)
    print('*'*60)
    print ('\n' *2)

    response = action_prompt(options)


    if response == 1:
        #define source file
        csv_path = input("Enter filepath for csv of VCs to parse:")

        #define target investment stage
        stage = input("Enter investment stage (one stage only) to target:")

        #get list of VC's filtered from raw list
        filtered_vc_list_by_stage_json_file = filter_csv_to_json(csv_path, stage)

        #check if user wants to restrict total connections found
        target_connections_count = get_target_connections_count()

        #find connections
        find_connections_for_vcs(filtered_vc_list_by_stage_json_file['output_filepath'], target_connections_count)

    elif response == 2:
        print ('using local file...')

        #check if user wants to restrict total connections found
        target_connections_count = get_target_connections_count()

        #find connections

        find_connections_for_vcs("master_list_vcs---filtered.json", target_connections_count)

    elif response == 3:
        print ('prepping preview of data for view in DEBUGGER...')

        result = export_connections(True)

        print ('Preview data above^^^')

    elif response == 4:
        print ('exporting connections, removing emoticons...')
        
        result = export_connections()

        print ('export finished. output filepath:', result)





if __name__ == "__main__":

    initialize()

    
'''
user can either filter a list of VC's from scratch or
start parsing the VC list from complete or with a total connected VC's goal set
or it can just summarize the connections.json file as is and spit out the remainder

needs to take the approvals already created, and append new companies to those approvals
needs to record which people have already been reached out to, and skip those ones?
or should it be based off which VC's you're trying to reach out to?
should you be able to look at VC's and exclude them?

so a list of VC's to contact that you are connected to, with a approval of bool to connecta
and a list of 1st degree connections that you are connected to, with a approval of bool to connect
then it compiles both lists and decides who to connect to and composes the messages accordingly
'''