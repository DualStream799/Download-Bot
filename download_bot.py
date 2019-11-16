# -*- coding: utf-8 -*-

from twilio.rest import Client
from selenium import webdriver
from pprint import pprint
import shutil
import json
import time
import os

class Download_Bot:
    """"""
    # Class Initialization:
    def __init__(self, client_status=False):
        # Importing Libraries:

        # Structural Variables:
        self.database_filename = "download_bot_database"
        self.client_filename = "client_database"
        self.database_structure = {"Anime_Data_Partition":{},
                                   "Analysis_Partition":{}}
        self.anime_data_structure = {"page_url":"",
                                     "episodes":{}}
        self.episode_structure = {"link":"",
                                  "status":"not downloaded"}
        self.analysis_data_structure = {"anime_pages_acessed":0,
                                        "completed_downloads":0,
                                        "restarted_downloads":0,
                                        "total_enlapsed_time":0,
                                        "errors_detected":0,
                                        "enlapsed_time_records":[]}
        # Path Variables:
        self.current_path = os.getcwd()
        self.user_path = self.find_user_path(self.current_path)
        self.download_path = self.user_path + 'Downloads'
        self.video_path = self.user_path + 'Videos'
        # Class Global Variables:
        self.database = self.check_database(self.database_filename)
        self.home_page_url = 'https://saikoanimes.net/'
        self.acess_amount = 0
        self.acess_limit = 1000
        self.client_status = client_status
        # Client Variables:
        if self.client_status == True:
            client_database = self.load_database(self.client_filename)
            self.to_number = client_database['to_number']
            self.from_number = client_database['from_number']
            self.client = Client()
            #self.client = Client(client_database['twilio_account_sid'], client_database['twilio_auth_token'])
        
    # WhatsApp Messaging using Twilio Sandbox:
    def whatsapp_send_message(self, message, to_number, from_number, mode=None):
        message = self.client.messages.create(body=message, to="whatsapp:+"+to_number, from_="whatsapp:+"+from_number)
        if mode == 'display': print(message.sid)
    
    # JSON Manipulation Methods (Interactions with the JSON file used as database):
    def create_database(self):
        """Creates the two database partitions on a single file outside the current directory (prevents to accidentaly publish your data)"""
        with open("../{}.json".format(self.database_filename), 'w+') as main_file:
            data_copy = self.database_structure.copy()
            data_copy['Analysis_Partition'] = self.analysis_data_structure.copy()
            return json.dump(data_copy, main_file)
        
    def load_database(self, filename):
        """Reads the database and returns it as a dictionary"""
        with open("../{}.json".format(filename), 'r+') as main_file:
            return json.loads(main_file.read())
            
    def update_database(self, filename):
        """Reads the database and overwirtes it"""
        with open("../{}.json".format(filename), 'w+') as main_file:
            return json.dump(self.database.copy(), main_file)
        
    def check_database(self, filename):
        """Acess the database file (in case of empty or inexistent file creates a new one and then acess it)"""
        try:
            return self.load_database(filename)
        except:
            self.create_database(filename)
            return self.load_database(filename)
            
    # Dict Manipulation Methods (Updates and additions to the database as a dictionary):
    def update_analysis_partition(self):
        """Updates the 'Analysis Partition' structure"""
        data_copy = self.database.copy()
        data_copy['Analysis_Partition'] = self.analysis_data_structure.copy()
        self.database = data_copy
    
    def create_section(self, anime_name, url):
        """Creates a new section on the database data"""
        data_copy = self.anime_data_structure.copy()
        data_copy['page_url'] = url
        self.database['Anime_Data_Partition'][anime_name] = data_copy
        
    def remove_section(self, anime_name):
        """Removes an existing section or do nothing otherwise"""
        self.database['Anime_Data_Partition'].pop(anime_name, None)
        
    def check_section(self, anime_name):
        """Checks if the database contains section of a given anime"""
        if anime_name not in self.database['Anime_Data_Partition'].keys():
            self.create_section(anime_name)
        
    def add_page_url(self, url, anime_name):
        """Adds the url of a given anime into the 'page_url' key"""
        data_copy = self.database['Anime_Data_Partition'][anime_name].copy()
        data_copy['page_url'] = url
        self.database['Anime_Data_Partition'][anime_name] = data_copy
        
    def add_episode(self, url, ep_number, anime_name):
        """Adds the whole structure of an episode updated with the current episode number and download link"""
        episode_dict = self.episode_structure.copy()
        episode_dict['link'] = url
        data_copy = self.database['Anime_Data_Partition'][anime_name]['episodes'].copy()
        data_copy[ep_number] = episode_dict
        self.database['Anime_Data_Partition'][anime_name]['episodes'] = data_copy
        
    def update_episode_attribute(self, key, value, ep_number, anime_name):
        """Updates (or create in case it doesn't exist) an attribute for a given episode"""
        data_copy = self.database['Anime_Data_Partition'][anime_name]['episodes'][ep_number].copy()
        data_copy[key] = value
        self.database['Anime_Data_Partition'][anime_name]['episodes'][ep_number] = data_copy
    
    def update_analysis_attribute(self, key, value, iterator=False):
        """Updates an attribute for a given analysis attribute (if no iterator is given, attribute is overwritten)"""
        data_copy = self.database['Analysis_Partition'].copy()
        if key != 'enlapsed_time_records':
            if iterator == True:
                data_copy[key] = data_copy[key] + value
            else:
                data_copy[key] = value
        else:
            data_copy[key].append(value)
        self.database['Analysis_Partition'] = data_copy
        
    # Path Manipulation Methods (Use paths to find files and folders):
    def find_file_by_type(self, file_type, path):
        """Find all files with a certain file type"""
        return [filename for filename in os.listdir(path) if filename.endswith(file_type) == True]
        
    def find_user_path(self, path):
        usual_dirs = ['Documents', 'Pictures', 'Videos', 'Downloads', 'Music', 'Desktop']
        for usual_dir in usual_dirs:
            splited_path = path.split(usual_dir)
            if len(splited_path) > 1:
                return splited_path[0]
                break
        print("Invalid Path: Nothing to return")
        
    def find_filesize(self, path, filename):
        """Returns the size of a given file in bytes (1Mb = 2^20 bytes)"""
        return os.path.getsize(path+"/"+filename)
        
    # Directory Manipulation Methods (Modifications on a given directory's files and folders):
    def new_directory(self, dir_name, path):
        """Creates a new folder in a given path"""
        os.mkdir(path + "/" + dir_name)
        
    def move_file(self, filename, from_path, to_path):
        """Moves a file from a path to another"""
        shutil.move(from_path + "/" + filename, to_path)
    
    def find_download_file(self, file_name, file_type, path, endswith_state = False):
        """Finds the download file on a given directory
           Temporary file: exists while the download process is running (endswith_state = False)
           Final file: exists after the download process finishes (endswith_state = True)"""
        partial_filename = self.partial_file_name(file_name)
        for filename in os.listdir(path):
            if (partial_filename in filename) and (file_type in filename) and (filename.endswith(file_type) == endswith_state):
                return filename
                break
                
    def check_anime_directory(self, file_name, anime_name, from_path, to_path):
        """Checks if exist a anime name's folder (if it doesn't exists, creates a new one) and moves a file to this folder"""
        if anime_name not in os.listdir(to_path):
            self.new_directory(anime_name, to_path)
        self.move_file(file_name, from_path, to_path+"/"+anime_name)
                
    def check_download_file(self, file_name, path, ep_number, anime_name):
        """Checks if the downloaded file has the expected file size.
           If the size IS correct the program moves the file to the correspondent anime folder and returns TRUE (or creates an anime folder in case it doesn't exists) :
           If the size IS NOT correct the program deletes the file and returns FALSE"""
        current_file_size = self.convert_file_size(self.find_filesize(path, file_name))
        expected_file_size = self.convert_file_size(self.database['Anime_Data_Partition'][anime_name]['episodes'][ep_number]['file_size'])
        if current_file_size >= expected_file_size:
            self.check_anime_directory(file_name, anime_name, self.download_path, self.video_path)
            return True
        else:
            os.remove(file_name)
            return False
        
    # String Manipulation Methods (String manipulations):
    def convert_file_size(self, file_size):
        if type(file_size) == str:
            return int(float(file_size[:-3]))
        elif type(file_size) == int:
            return int((file_size/2**20))
        
    def convert_page_to_name(self, page_url):
        return ' '.join([word.capitalize() for word in page_url.split('/')[-2].split('-')])
    
    def convert_title_to_filename(self, page_title):
        return page_title.split(' - ')[0].split('.')[0:2]
        
    def partial_file_name(self, file_name_string):
        if file_name_string.endswith('...') == True:
            return file_name_string[:-3]
        else:
            return file_name_string
        
    # Manual Override (Manually execute entire commands):
    def manual_insert(self, url):
        """Manually creates a new anime section"""
        anime_name = self.convert_page_to_name(url)
        self.check_section(anime_name)
        self.add_page_url(url, anime_name)
        self.update_database(self.database_filename)
        
    def manual_delete(self, url):
        """Manually removes an existent anime section"""
        anime_name = self.convert_page_to_name(url)
        self.remove_section(anime_name)
        self.update_database(self.database_filename)
        
    def manual_set_download(self, anime_name):
        """"""
        pass
                
    # Browser Manipulation (Navigate and extract data using Selenium WebDriver):
    def open_new_tab(self, driver):
        """Open a new tab using Selenium WebDriver"""
        driver.execute_script('''window.open("","_blank");''')
        
    def driver_start_firefox(self):
        """Open Firefox browser under Selenium webdriver's control"""
        return webdriver.Firefox()
    
    def driver_end(self, driver):
        """Closes Firefox browser under Selenium webdriver's control"""
        driver.quit()   
    
    def main(self, mode='download'):
        # initializes time counter:
        timer = time.time()
        # Opens Firefox browser under Selenium webdriver's control:
        driver = self.driver_start_firefox()
        # Acesses Saiko Animes' home page and extracts all new anime links:
        new_animes = self.acess_home_page(driver)
        #del new_animes[new_animes.index('https://saikoanimes.net/diamond-no-ace-act-ii-33/')]
        link = 'https://saikoanimes.net/diamond-no-ace-act-ii-33/'
        del new_animes[new_animes.index(link)]
        # Open a new tab:
        self.open_new_tab(driver)
        self.open_new_tab(driver)
        # For each one of the extracted links:
        for anime_page in new_animes:
            if mode == 'display': print('Acessing {} of {} anime pages. Episodes scanned: {}'.format(new_animes.index(anime_page)+1, len(new_animes), self.acess_amount))
            # Makes driver analyse on the new tab:
            driver.switch_to.window(driver.window_handles[1])
            # Acesses the anime page and finds all necessary variables
            self.acess_anime_page(driver, anime_page, mode)
            # Checks if acess amount exceeded limit:
            if self.acess_amount > self.acess_limit:
                if mode == 'display': print("Chunk Limit Exceeded")
                break
        # Closes the window's browser:
        driver.quit()
        # Finishes the timer:
        enlapsed_time = time.time() - timer
        # Updates analysis counters:
        self.update_analysis_attribute('total_enlapsed_time', enlapsed_time, iterator=True)
        self.update_analysis_attribute('enlapsed_time_records', enlapsed_time)
        # Update database file:
        self.update_database(self.database_filename)
        if mode == 'display': print('Database exported')
        
    def acess_home_page(self, driver):
        try:
            # List to store all pages' urls:
            new_anime_urls = []
            # Dictionary to store all page's controllers in order:
            page_controllers = {}
            # Acesses main page:
            driver.get(self.home_page_url)
            # Finds the fist and last id value from the section's controllers:
            last_controller_id = driver.find_element_by_id('pag_sa').find_element_by_class_name('facetwp-pager').find_element_by_class_name('last-page').get_attribute('data-page')            
            current_controller_id = driver.find_element_by_id('pag_sa').find_element_by_class_name('facetwp-pager').find_element_by_class_name('active').get_attribute('data-page')
            # Runs until reaches the last section:
            while current_controller_id != last_controller_id:
                # Finds new anime's area:
                anime_area = driver.find_element_by_id('pag_sa')
                # Gets and stores all anime pages' urls:
                anime_links = [box.find_element_by_tag_name('a').get_attribute('href') for box in anime_area.find_element_by_class_name('facetwp-template').find_elements_by_id('content')]
                _ = [new_anime_urls.append(url) for url in anime_links if url not in new_anime_urls] 
                # Gets and stores all section's controllers:
                boxes_controllers = anime_area.find_element_by_class_name('facetwp-pager').find_elements_by_class_name('facetwp-page')
                for key, value in zip([controller.get_attribute('data-page') for controller in boxes_controllers], boxes_controllers):
                    page_controllers[key] = value
                # Updates the 'while loop' controller:
                current_controller_id = str(int(current_controller_id)+1)
                # Clicks on the next section controller:
                page_controllers[current_controller_id].click()
                # Waits until section's update:
                time.sleep(10)    
        finally:
            return new_anime_urls
        
    def acess_anime_page(self, driver, page_url, mode='download'):
        """Accesses the anime main page, finds episode's links and execute download_manager for each one of them"""
        try:
            extraction_counter = 0
            # Accesses the anime's page:
            driver.get(page_url)
            # Gets the redirected url (correct url for anime name extraction):
            page_url = driver.current_url
            
            if mode == 'display': print(page_url)
            # Extracts the anime name from the page's url:
            anime_name = self.convert_page_to_name(page_url)
            # Checks if there is an anime section (if not, creates a new section):
            if anime_name not in self.database['Anime_Data_Partition'].keys():
                self.create_section(anime_name, page_url)
                if mode == 'display': print('New anime section created')
            # Checks if the 'Saikô Cloud' tab is active (if is not, click in the 'Saikô Cloud' tab button):
            tab = driver.find_element_by_class_name('tab_content-pag-anime').find_element_by_class_name('tabs-bnt')
            if (tab.find_element_by_class_name('active').find_element_by_tag_name('a').text).encode('utf-8') != 'SAIKÔ CLOUD':
                tab_button = tab.find_element_by_partial_link_text('Ô CLOUD')
                tab_button.click()
                time.sleep(5)
                tab_id = tab_button.get_attribute('href').split('#')[-1]
                buttons = driver.find_element_by_class_name('tab_bnt_container').find_element_by_id(tab_id).find_element_by_class_name('bnt-area').find_elements_by_tag_name('a')
                
            else:
                # Extracts all episode buttons:
                buttons = driver.find_element_by_class_name('bnt-area').find_elements_by_tag_name('a')
            # Accesses episodes' number and episodes' download page link:
            ep_numbers = [button.text for button in buttons]
            ep_download_pages = [button.get_attribute('href') for button in buttons]
            # Makes driver analyse on the new tab:
            driver.switch_to.window(driver.window_handles[2])
            # Repeats the process for every episode link:            
            for ep_number, ep_download_page in zip(ep_numbers, ep_download_pages):
                if mode == 'display': print('Acessing {} of {} episode pages'.format(ep_numbers.index(ep_number)+1, len(ep_numbers)))
                # Checks if there is a episode section (if not, creates a new section):
                if ep_number not in self.database['Anime_Data_Partition'][anime_name]['episodes'].keys():
                    if mode == 'display': print('New section created for episode {}'.format(ep_number))
                    # Creates a new episode section:
                    self.add_episode(ep_download_page, ep_number, anime_name)
                    # Updates chunksize variable to limit RAM usage:
                    self.acess_amount += 1
                    extraction_counter += 1
                # Checks if the episode was already downloaded:
                elif self.database['Anime_Data_Partition'][anime_name]['episodes'][ep_number]['status'] == 'not downloaded' and mode == 'download':
                    # Accesses the episode download page:
                    driver.get(ep_download_page)
                    # Activates download manager to control and verify the download process:
                    self.download_manager(driver, anime_name, ep_number, ep_download_page)
                    # Updates chunksize variable to limit RAM usage:
                    self.acess_amount += 1
                    if mode == 'download': self.download_manager(driver, anime_name, ep_number, ep_download_page, partial_name, file_size)
                else:
                    if mode == 'display': print('Episode {} of {} already downloaded'.format(ep_numbers.index(ep_number)+1, len(ep_numbers)))
        except:
            self.update_analysis_attribute('errors_detected', 1, iterator=True)
            if mode == 'display': print('Error detected')
        finally:
            # Updates analysis counters:
            self.update_analysis_attribute('anime_pages_acessed', 1, iterator=True)
            if self.client_status == True:
                mes = "*Download Bot:* {}  new episodes of _{}_ found".format(extraction_counter, anime_name)
                self.whatsapp_send_message(mes, self.to_number, self.from_number)
            
    def download_manager(self, driver, anime_name, ep_number, ep_download_page):
        # Filters the partial file name and extension:
        partial_name, file_extension = self.convert_title_to_filename(driver.title)
        # Gets file size:
        file_size = driver.find_elements_by_class_name('fileinfo')[1].text
        # Exports file size:
        self.update_episode_attribute('file_size', file_size, ep_number, anime_name)
        # While loop and control variable:
        controller = True
        while controller:
            # Only updates the controller status if all the other commands were properly executed, otherwise the loop continues:
            try:
                # Gets episode direct link:
                download_button = driver.find_element_by_class_name('bnt-down')
                download_link = download_button.get_attribute('href')
                # Starts download file process:
                download_button.send_keys(Keys.ENTER)
                # Waits in order to the browser starts downloading:
                time.sleep(15)
                # Checks if the temporary file still exists and updates the controller variable(while the temporary file exists the download didn't finish yet):
                temporary_file = ' '
                while temporary_file is not None:
                    # Waits some time for new verification:
                    time.sleep(5)
                    # Gets the temporary file name (if it still exists):
                    temporary_file = self.find_download_file(partial_name, file_extension, self.download_path)

                    print("Temporary file found")
                print("Temporary file not found")
                # Gets the downloded file name:
                downloaded_file = self.find_download_file(partial_name, file_extension, self.download_path, endswith_state=True)
                # Waits some time until the download file be ready:
                time.sleep(15)
                # Checks if the downloaded file has the expected size:
                if self.check_download_file(downloaded_file, self.download_path, ep_number, anime_name) == True:
                    # Updates episode status:
                    self.database['Anime_Data_Partition'][anime_name]['episodes'][ep_number]['status'] = 'downloaded'
                    # Updates analysis counters:
                    self.update_analysis_attribute('completed_downloads', 1, iterator=True)
                    pprint(self.database)
                    # Updates controller variable and end the loop:
                    controller = False
                    print("Clean Process")
            #In case of any error (suposes a internet connection error, not a programming error):
#                        except:
#                            self.update_analysis_attribute('restarted_downloads', 1, iterator=True)
#                            print("Error detected, reinitializing process...")
            finally:
                pass