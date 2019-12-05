# -*- coding: utf-8 -*-

from download_bot import Download_Bot
import os

print('Download_Bot library successfully imported')
bot = Download_Bot()


controller = True
while controller:
	control_mode = str(input("\nNext Input: "))

	if (control_mode == 'organize') or (control_mode == 'o'):
		# Files on Downloads directory:
		files = bot.find_file_by_type('.mp4', bot.download_path) + bot.find_file_by_type('.m4v', bot.download_path)
		for episode_file in files:
		    anime_name = bot.convert_filename_to_anime_name(episode_file)
		    anime_name = " ".join([word.capitalize() for word in anime_name.split(' ')])
		    bot.check_anime_directory(episode_file, anime_name, bot.download_path, bot.video_path+'/'+bot.root_folder)
		print("Last command: ORGANIZE")
	elif (control_mode == 'disorganize') or (control_mode == 'd'):
		# Files in Videos/Animes directory:
		root_folder = bot.video_path+"/"+bot.root_folder
		for folder in os.listdir(root_folder):
		    folder_path = root_folder+"/"+folder
		    files = bot.find_file_by_type('.mp4', folder_path) + bot.find_file_by_type('.m4v', folder_path)
		    for episode_file in files:
		        bot.move_file(episode_file, folder_path, bot.download_path)
		    os.rmdir(folder_path)
		print("Last command: DISORGANIZE")
	elif (control_mode == 'exit') or (control_mode == 'e'):
		controller = False
		print("Program finished")
	else:
		print("Invalid command, please try again")