import json
import sys
import random
import time
from selenium import webdriver
import pyperclip
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

import getpass
import re

# json_file_path = "tier1-vcs.json"
connection_maps_path = 'connections.json'

# Set the path to your Chrome WebDriver
webdriver_path = "./chromedriver"

#load existing list of connections
with open(connection_maps_path, "r") as json_file:
    connections_list = json.load(json_file)



#roles we target
target_roles_list = [
    'founder',
    'manager',
    'partner',
    'president',
    'vp',
    'director',
    'investor',
    'principal'
]

def spinning_loading_line():
    symbols = ['|', '/', '-', '\\', '|', '/', '-', '\\']
    while True:
        for symbol in symbols:
            sys.stdout.write('\r' + symbol)
            sys.stdout.flush()
            time.sleep(0.1)


def clean_emoticons(input):
    tempstring = input
    try:
        emoji_removed_string = re.sub(r'[^\x00-\x7F]+', '', tempstring)
        return emoji_removed_string
    except Exception as e:
        print (e)
        return tempstring


# def random_pause(a, b):
#     # pauses for random amount of time between an upper and lower bound
#     pause_duration = random.randint(a, b)
#     # print(f"Pausing for {pause_duration} seconds...")

#     # Countdown timer
#     for i in range(pause_duration, 0, -1):
#         print(f"Hesitating for {i} seconds...", end='\r')
#         time.sleep(1)

#     return


def random_pause(a, b, start_string = 'hesitating', end_string = 'continuing...'):
    # pauses for random amount of time between an upper and lower bound
    pause_duration = random.randint(a, b)

    # Countdown timer
    for i in range(pause_duration, 0, -1):
        symbols = ['|', '/', '-', '\\', '|', '/', '-', '\\']
        for symbol in symbols:
            sys.stdout.write('\r' + f"{start_string} for {i} seconds... {symbol}")
            sys.stdout.flush()
            time.sleep(0.1)

    
    sys.stdout.write('\r' + ' ' * 40 + '\r')
    sys.stdout.flush()

    print (f'finished hesitating for {b} seconds')

    conts = list(end_string)
    for cont in conts:
        print (cont, end='', flush=True)
        time.sleep(0.1)

    return


# pre-log into linkedin
def li_login(driver, li_email, li_pw):

    #initializing driver
    driver.get('https://www.linkedin.com/login')

    print ('logging into linkedin, please stand by...')

    random_pause(3, 10)
    
    username_field = driver.find_element_by_id("username")
    password_field = driver.find_element_by_id("password")

    #entering user email
    pyperclip.copy(li_email)
    username_field.send_keys(Keys.COMMAND, 'v')

    print ('simulating username entry')
    random_pause(3, 10)

    #entering user pw
    pyperclip.copy(li_pw)
    password_field.send_keys(Keys.COMMAND, 'v')

    print ('simulating password entry')
    random_pause(3, 10)

    submit_btn = driver.find_element_by_css_selector("[aria-label='Sign in']")
    submit_btn.click()

    print ('\nloading homepage...')
    random_pause(3, 14)

    print ('successfully logged in')
    

    return 'ok'



#get company info first
def check_company_info(li_company_url, driver):
    driver.get(li_company_url)

    print ('checking company info...')
    random_pause(4,10)
    
    tagline=''
    overview = ''

    try:
        tagline = clean_emoticons(driver.find_element_by_xpath(
                "//*[contains(@class, 'org-top-card-summary')]").text)
    except:
        pass

    try:
        overview = clean_emoticons(driver.find_element_by_xpath(
            "//*[contains(@class, 'break-words white-space-pre-wrap')]").text)
    except:
        pass

    return {
        'qualified': True,
        'tagline': tagline,
        'overview': overview
    }
    

#check people at the company
def check_people(li_people_url, driver):
    
    # separates the first and last name from a block name string
    def separate_fname_lname(name):
        fname = name[0:name.find(' ')].strip()
        lname = name[name.find(' ')+1:].strip()
        return{
            'fname': fname,
            'lname': lname,
        }

    # extract the person's name from black text info
    def extract_primary_name(info):
        name = info[0:info.find("\n")].strip()

        split_names = separate_fname_lname(name)
        return{
            'name': name,
            'fname': split_names['fname'],
            'lname': split_names['lname']
        }

    #check if the person is a decision maker at the VC
    def check_decision_maker(info):
        role = info.split('\n')[3]

        for r in target_roles_list:
            if r in role.lower():
                return {
                    'result':True,
                    'role': role
                }
            
        return {
                    'result':False,
                    'role': None
                }
    
    xpath_expr = f'//a[contains(@href, "/people/")]'
    people_page_el = driver.find_elements_by_xpath(xpath_expr)

    try:

        for el in people_page_el:
            if el.text.lower() == 'people':
                el.click()
                break
        
        # driver.get(li_people_url)
        print ('navigating to people info...')
        random_pause(3, 7)

        driver.find_element_by_tag_name('body').send_keys(Keys.END)
        random_pause(3, 5)

        # Scroll until the window stops scrolling
        last_height = driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            driver.find_element_by_tag_name('body').send_keys(Keys.END)
            random_pause(8, 15)
            new_height = driver.execute_script("return document.documentElement.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        
        people_el = driver.find_elements_by_xpath(
            "//*[contains(@class, 'grid grid__col--lg-8 block')]")
        
        people = []
        for p_el in people_el:
            info = clean_emoticons(p_el.text)
            try:
                profile_link = p_el.find_element_by_xpath(".//*[contains(@class, 'app-aware-link')]").get_attribute("href")
                decision_maker = check_decision_maker(info)
                if decision_maker['result'] == True:
                    people.append({
                        'info': info,
                        'profile link': profile_link,
                        'decision maker': decision_maker
                    })
            except:
                pass
        
        connectable_people = []
        for p in people:
            if p['decision maker']['result'] == True:
                name_info = extract_primary_name(p['info'])
                
                if ('2nd' in p['info'].lower()):
                    try:
                        driver.get(p['profile link'])
                        print (f"2nd connection decision maker identified: {name_info['name']}")
                        print (f"going to {name_info['name']}'s profile...")
                        random_pause(3,10)
                        mutuals_el = driver.find_element_by_xpath(".//*[contains(@class, 'ph5 pb5')]").find_element_by_xpath(".//*[contains(@class, 'app-aware-link')]")
                        m_url = mutuals_el.get_attribute("href")
                        #go to mutual connections link
                        # driver.get(m_url)
                        mutuals_el.click()
                        print (f"going to {name_info['name']}'s mutual connections...")
                        random_pause(5,12)      
                        #get people
                        all_mutuals_el = driver.find_elements_by_class_name('entity-result__item')           
                        all_mutuals = []
                        for m in all_mutuals_el:
                            name_string = clean_emoticons(m.find_element_by_xpath(".//span[@dir='ltr']").text)
                            name = name_string[:name_string.find('\n')]
                            name = name.strip()
                            link_el = m.find_element_by_xpath(".//*[contains(@class, 'app-aware-link')]")
                            profile_link = link_el.get_attribute("href")
                            subtitle_el = m.find_element_by_xpath(".//*[contains(@class, 'entity-result__primary-subtitle')]")
                            subtitle = clean_emoticons(subtitle_el.text)
                            connect_obj = {
                                'name': name,
                                'profile_url': profile_link[:profile_link.find('?')],
                                'title': subtitle
                            }
                            all_mutuals.append(connect_obj)
                            print(connect_obj)

                        connectable_people.append( {
                            'primary target': {
                                'name': name_info,
                                'role': decision_maker['role'],
                                'profile url': p['profile link']
                            },
                            'degree': 2,
                            'connections': {
                                'number of connections': len(all_mutuals),
                                '1st connections': all_mutuals
                                }
                        })
                    except:
                        pass
                
                elif ('1st' in p['info'].lower()):
                    connectable_people.append({
                        'primary target': name_info,
                        'degree': 1,
                        'connections': None,
                        'profile url': p['profile link']
                    })
                else:
                    print ('*'*7, name_info['name'], 'is a 3rd connection, skipping...')

        if len(connectable_people) > 0:
            return connectable_people
        else:
            return None
        
    except Exception as e:
        print ('error parsing linkedin page:', e)

        return 'error'


# log into linkedin first
# li_login()

# Iterate through each JSON item
def connect_with_vcs(data, li_logged_in, target_connections_count = 0):

    parsed_counter = len(connections_list)

    list_total = len(data)
    
    print ('\n' *2)
    print('*'*60)
    print('*'*60)
    print('\n') 

    print (f'{parsed_counter} VCs currently parsed in output list. Input list has {list_total} VCs in total.')

    print('\n') 
    print('*'*60)
    print('*'*60)
    print('\n') 

    if target_connections_count == 0 :
        target_connections_count = list_total
    
    driver = None
    vcs = data[:]
    random.shuffle(vcs)
    c = 0
    connected_counter = 0
    for item in vcs:
        c += 1

        found = False
        for r in connections_list:
            if item['name'] == r['vc']['name']:
                # print (item['name'], 'has been parsed. Skipping...')
                found = True
                break
            
        if found == False:
            print (item['name'], 'has not been parsed. Initializing connections analyses...')
            li_url = item['linkedin']

            #clear off final backslash if exists
            if li_url[-1] == '/':
                li_url = li_url[:len(li_url)-1]

            if '/company/' in li_url.lower():

                #initialize driver if it has not been initialized yet
                if driver is None:

                    #get user creds
                    li_email = input("Enter Your LinkedIn Email:")
                    li_pw = getpass.getpass("Enter your LinkedIn password: ")
                    
                    driver = webdriver.Chrome(executable_path=webdriver_path)
                    random_pause(2,4)

                if li_logged_in == False:
                    

                    li_login(driver, li_email, li_pw)

                    #set log in to true
                    li_logged_in = True

                li_about_url = li_url + '/about/'
                li_people_url = li_url + '/people/'
                
                #currently defaults to True, becuase of too many falses.
                company_details = check_company_info(li_about_url, driver)
                connections = []
                if company_details['qualified'] == True:
                    connections = check_people(li_people_url, driver)
                    if (connections != None) or (connections != 'error'):
                        compiled_obj = {
                            'vc': item,
                            'vc tagline': company_details['tagline'],
                            'vc overview': company_details['overview'],
                            'linkedin info': company_details,
                            'people and connections': connections
                        }

                        connections_list.append(compiled_obj)

                        print (len(connections), 'connections saved for', item['name'])

                        connected_counter += 1

                        #stops when it has reached the goal
                        if connected_counter == target_connections_count:
                            break

                    elif connections == None:
                        print ("no suitable 2nd degree decision makers were found for", item['name'], 'storing results and continuing...')
                        compiled_obj = {
                            'vc': item,
                            'vc tagline': company_details['tagline'],
                            'vc overview': company_details['overview'],
                            'linkedin info': company_details,
                            'people and connections': None
                        }

                        connections_list.append(compiled_obj)

                    elif connections == 'error':
                        pass

                    # Write the object to JSON file
                    with open(connection_maps_path, 'w') as f:
                        json.dump(connections_list, f, indent=4)

                    parsed_counter += 1
                    
                    print (f'{parsed_counter} VCs parsed of {list_total}.')
                    
                    random_pause(35,90)

            else:
                print (item['name'], 'has a broken linkedin URL. Skipping...')


    print (c, f'VCs in a list of {len(vcs)} VCs scanned successfully!')

    return connection_maps_path, driver


    
if __name__ == "__main__":
    random_pause(1, 4)

    
