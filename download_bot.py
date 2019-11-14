from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome import service
from selenium import webdriver
from pprint import pprint
import shutil
import json
import time
import os


class Download_Bot:
    """"""

    # Class Initialization:
    def __init__(self):
        # Importing Libraries:

        # Structural Variables:
        self.database_filename = "download_bot_database"

        self.database_structure = {"Anime_Data_Partition": {},
                                   "Analysis_Partition": {}}

        self.anime_data_structure = {"page_url": "",
                                     "episodes": {}}

        self.episode_structure = {"link": "",
                                  "status": "not downloaded"}

        self.analysis_data_structure = {"anime_pages_extracted": 0,
                                        "anime_pages_acessed": 0,
                                        "links_extracted": 0,
                                        "links_acessed": 0,
                                        "completed_downloads": 0,
                                        "restarted_downloads": 0,
                                        "errors_detected": 0}
        # Path Variables:
        self.current_path = os.getcwd()
        self.user_path = self.find_user_path(self.current_path)
        self.download_path = self.user_path + 'Downloads'
        self.video_path = self.user_path + 'Videos'

        # Database Variables:
        self.database = self.check_database()

    #
    def link_start(self):
        """"""
        pass

    # JSON Manipulation Methods (Interactions with the JSON file used as database):
    def create_database(self):
        """Creates the two database partitions on a single file outside the current directory
        (prevents to accidentaly publish your data)"""
        with open("../{}.json".format(self.database_filename), 'w+') as main_file:
            data_copy = self.database_structure.copy()
            data_copy['Analysis_Partition'] = self.analysis_data_structure.copy()
            return json.dump(data_copy, main_file)

    def load_database(self):
        """Reads the database and returns it as a dictionary"""
        with open("../{}.json".format(self.database_filename), 'r+') as main_file:
            return json.loads(main_file.read())

    def update_database(self):
        """Reads the database and overwirtes it"""
        with open("../{}.json".format(self.database_filename), 'w+') as main_file:
            return json.dump(self.database.copy(), main_file)

    def check_database(self):
        """Acess the database file (in case of empty or inexistent file creates a new one and then acess it)"""
        try:
            return self.load_database()
        except:
            self.create_database()
            return self.load_database()

    # Dict Manipulation Methods (Updates and additions to the database as a dictionary):
    def create_section(self, anime_name):
        """Creates a new section on the database data"""
        self.database['Anime_Data_Partition'][anime_name] = self.anime_data_structure.copy()

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
        """Add the whole structure of an episode updated with the current episode number and download link"""
        episode_dict = self.episode_structure.copy()
        episode_dict['link'] = url
        data_copy = self.database['Anime_Data_Partition'][anime_name]['episodes'].copy()
        data_copy[ep_number] = episode_dict
        self.database['Anime_Data_Partition'][anime_name]['episodes'] = data_copy

    def update_episode_attribute(self, key, value, ep_number, anime_name):
        """Update (or create in case it doesn't exist) an attribute for a given episode"""
        data_copy = self.database['Anime_Data_Partition'][anime_name]['episodes'][ep_number].copy()
        data_copy[key] = value
        self.database['Anime_Data_Partition'][anime_name]['episodes'][ep_number] = data_copy

    # Browser Manipulation (navigate and extract data using Selenium WebDriver):
    def extract_episodes(self, url):
        """Recieve the 'page_url' value of a given anime extracts and saves all links of each episode"""
        anime_name = self.convert_page_link(url)
        driver = webdriver.Firefox()
        driver.get(url)
        try:
            for button in driver.find_element_by_class_name('bnt-area').find_elements_by_tag_name('a'):
                self.add_episode(button.get_attribute('href'), self.convert_ep_number(button.text), anime_name)
        except:
            print("Extraction Process Interrupted")
        finally:
            driver.quit()

    def extract_episode_info(self, url, ep_number, anime_name):
        """Acess an episode link, extracts and saves the direct download link and the file size"""
        driver = webdriver.Firefox()
        driver.get(url)
        try:
            infos = driver.find_elements_by_class_name('fileinfo')
            download_link = driver.find_element_by_class_name('bnt-down').get_attribute('href')
            self.update_episode_attribute('file_size', infos[1].text, ep_number, anime_name)
            self.update_episode_attribute('direct_link', download_link, ep_number, anime_name)
            print('direct link exported')
        # except:
        #    print("Extraction Process Interrupted")
        finally:
            driver.quit()

    def open_new_tab(self):
        # driver.execute_script('''window.open("{}","_blank");'''.format(url))
        # driver.execute_script('''window.open("{}");'''.format(url))
        driver.execute_script('''window.open("","_blank");''')

    def download_manager(self):
        """"""
        pass

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
        return os.path.getsize(path + "/" + filename)

    # Directory Manipulation Methods (Modifications on a given directory's files and folders):
    def new_directory(self, dir_name, path):
        """Creates a new folder in a given path"""
        os.mkdir(path + "/" + dir_name)

    def move_file(self, filename, from_path, to_path):
        """Move a file from a path to another"""
        shutil.move(from_path + "/" + filename, to_path)

    def find_download_file(self, file_name, file_type, path, endswith_state=False):
        """Finds the download file on a given directory
           Temporary file: exists while the download process is running (endswith_state = False)
           Final file: exists after the download process finishes (endswith_state = True)"""
        partial_filename = self.partial_file_name(file_name)
        for filename in os.listdir(path):
            if (partial_filename in filename) and (file_type in filename) and (
                    filename.endswith(file_type) == endswith_state):
                return filename
                break

    def check_download_file(self, path, file_name, ep_number, anime_name):
        """Check if the downloaded file has the expected file size.
           If the size IS correct the program moves the file to the correspondent anime folder and returns TRUE (or creates an anime folder in case it doesn't exists) :
           If the size IS NOT correct the program deletes the file and returns FALSE"""
        current_file_size = self.convert_file_size(self.find_filesize(path, file_name))
        expected_file_size = self.convert_file_size(self.database['Anime_Data_Partition'][anime_name]['episodes'][ep_number]['file_size'])
        if current_file_size == expected_file_size:
            try:
                self.move_file(file_name, self.download_path, self.video_path)
            except:
                self.new_directory(anime_name, self.video_path)
                self.move_file(file_name, self.download_path, self.video_path)
            finally:
                return True
        else:
            os.remove(file_name)
            return False

    # String Manipulation Methods (String manipulations ):
    def convert_ep_number(self, ep_number_string):
        return str(int(ep_number_string))

    def convert_file_size(self, file_size):
        if type(file_size) == str:
            return int(float(file_size[:-3]))
        elif type(file_size) == int:
            return int((file_size / 2 ** 20))

    def convert_page_link(self, page_url):
        return ' '.join([word.capitalize() for word in page_url.split('/')[-2].split('-')])

    def partial_file_name(self, file_name_string):
        if file_name_string.endswith('...') == True:
            return file_name_string[:-3]
        else:
            return file_name_string

    # Manual Override (Manually execute entire commands):
    def manual_input(self, url):
        anime_name = self.convert_page_link(url)
        self.check_section(anime_name)
        self.add_page_url(url, anime_name)
        self.update_database()

    def find_downloaded_file(self, file_name, param, downloaded_path, endswith_state):
        pass


bot = Download_Bot()

def download_manager(download_button, file_name, ep_number, anime_name, controller=True):
    print('Download Manager Initialized')
    while controller == True:
        # Check if the episode was already downloaded:
        if bot.database['Anime_Data_Partition'][anime_name]['episodes'][ep_number]['status'] == 'not downloaded':
            # Only updates the controller status if all the other commands were properly executed, otherwise the loop continues:
            try:
                # Starts download process:
                download_button.click()
                print('Download Started')
                # Waits in order to the browser starts downloading:
                time.sleep(20)
                # Filters the partial file name:
                filename = bot.partial_file_name(file_name)
                # Starts a controller:
                temporary_file = " "
                # Checks if the temporary file still exists and updates the controller variable(while the temporary file exists the download didn't finish yet):
                while temporary_file is not None:
                    # Waits some time for new verification:
                    time.sleep(15)
                    # Gets the temporary file name (if it still exists):
                    temporary_file = bot.find_download_file(file_name, '.mp4', bot.download_path)
                    print('Temporary file found')
                # Gets the downloded file name:
                downloaded_file = bot.find_download_file(file_name, '.mp4', bot.download_path, endswith_state=True)
                # Checks if the downloaded file has the expected size:
                if bot.check_download_file(filename, ep_number, anime_name) == True:
                    # Update controller variable and end the loop:
                    controller = False
            #In case of any error:
            except:
                #print('Download Process Interrupted\nRestarting Process...')
                # Try to delete the temporary file:
                try:
                    os.remove(bot.download_path+"/"+temporary_file)
                except:
                    pass
        else:
            controller = False

#from selenium.webdriver.common.keys import Keys
anime_name = 'Dr Stone'
anime_main_page = bot.database['Anime_Data_Partition'][anime_name]['page_url']
try:
    # Opens FireFox browser under Selenium control:
    driver = webdriver.Firefox()
    # Accesses the main page:
    driver.get(anime_main_page)
    # Repeats the process for every episode link:
    for button in driver.find_element_by_class_name('bnt-area').find_elements_by_tag_name('a'):
        # Accesses episode number:
        ep_number = bot.convert_ep_number(button.text)
        ep_direct_link = button.get_attribute('href')
        # Opens a new window:
        bot.open_new_tab()
        # Makes drive analyse on the new window:
        driver.switch_to.window(driver.window_handles[1])
        # Accesses the episode download page:
        driver.get(ep_direct_link)
        # Finds file info (partial file name and file size):
        infos = driver.find_elements_by_class_name('fileinfo')
        # Finds donwload button:
        download_button = driver.find_element_by_class_name('bnt-down')
        # Exports file size:
        bot.update_episode_attribute('file_size', infos[1].text, ep_number, anime_name)
        # Exports direct download link:
        bot.update_episode_attribute('direct_link', download_button.get_attribute('href'), ep_number, anime_name)
        # Starts download:
        print("Acess episode download page sucessfull")
        download_manager(download_button, infos[0].text, ep_number, anime_name)
        # Closes the episode download page:
        driver.close()
        pprint(bot.database)
        break
finally:
    driver.quit()