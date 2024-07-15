"""
This module provides functions for creating csv files for some of the scripts used here.

Author: David Durham

License: MIT
"""

from csv import writer


_HEADERS = {
	"new_hire" : [["user_id","f_name","l_name","email","position"]],
	"course_copy": [["course_name","course_id","master_id","term","instructor_1","instructor_2","instructor_3"]],
	"enroll_user" : [["course_id", "user_id", "role"]],
	"adjunct_training": [["f_name","l_name","user_id","supervisor","mentor","program","p1_due","p2_due","p3_due","p4_due"]]
}

_OUT_FILES = {
	"new_hire" : "data/new_hires.csv",
	"course_copy": "data/course_copy.csv",
	"enroll_user" : "data/enroll_users.csv",
	"adjunct_training": "data/adjunct_training.csv"
}

def _create_template_csv(output_file: str, headers: list) -> None:
	"""Creates an empty csv for various functions. Includes needed headers"""

	_headers = headers
	csv_file_path = output_file

	with open(csv_file_path, mode='w', newline='') as file:
		_writer = writer(file)
		_writer.writerows(_headers)

	print(f"CSV file '{csv_file_path}' created successfully.")



def create_course_copy_csv() -> None:
	_create_template_csv(output_file=_OUT_FILES["course_copy"], headers=_HEADERS["course_copy"])

def create_new_hire_list_csv() -> None:
	_create_template_csv(output_file=_OUT_FILES["new_hire"], headers=_HEADERS["new_hire"])

def create_adjunct_training_csv() -> None:
	_create_template_csv(output_file=_OUT_FILES["adjunct_training"], headers=_HEADERS["adjunct_training"])

def create_enroll_user_csv() -> None:
	_create_template_csv(output_file=_OUT_FILES["enroll_user"], headers=_HEADERS["enroll_user"])


if __name__ == "__main__":
	pass