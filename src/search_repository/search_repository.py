#!/usr/bin/env python3

from src.helpers import git_requests, file_handler, user_input

repos = user_input.comma_str_to_list()
search_string = user_input.extract_user_string("Search String: ")
file_names = user_input.extract_user_string("In which files? ")

for repo in repos:
    location = git_requests.download_repository(repo, "/tmp/")

    for file in file_handler.get_files_in_dir_rec(file_names, location):
        lines = file_handler.find_lines(search_string, file, True)
        if lines:

            print(
                file_handler.ChangeColors.new + "\n" + str(len(lines)) + " Occurrences In: " + file.replace("/tmp/", "")
                + "\n" + file_handler.ChangeColors.end)
            for line in lines:
                print(line[0].strip() + "\nLine Number: " + str(line[1]) + "\n")