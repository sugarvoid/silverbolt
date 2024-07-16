

from datetime import datetime
from time import sleep
from bb_lib.course import copy_course, create_empty_course, delete_course, enroll_user, copy_courses_from_csv, get_users_in_course, remove_by_role, unenroll_user, update_courses_from_csv, get_user_courses
from bb_lib.user import create_user, get_username_from_id, does_user_exist



courses = ["ADJPART12020","AdjTrainingPART2D23","AdjTrainingPART3","AdjTrainingPART4D24"]

#create_empty_course(course_id="test123", course_name="Delete Me")
#enroll_user(user_ID="001100", course_ID="AdjTrainingPART2-2024", role="Student")

# create_user("", "test1", "test2", "email")

numbers_list = [

]

if __name__ == "__main__":

    #for s in numbers_list: 
      #  enroll_user(user_ID=s, course_id="aviation_workshop")

    #create_empty_course(course_id="10070103-2-2024fall", course_name="Service Maintenance & Principles(Section 2)")
    #create_empty_course(course_id="31410356-2-2024fall", course_name="Interior Closure Project (Section 2)")
    pass
    #Logger.info("hey there")
    #copy_courses()
    ### copy_courses_from_csv("data/course_copy.csv")
    ### sleep(60)
    ### update_courses_from_csv("data/course_copy.csv")
    #update_titles()
    #add_teachers()
    ### copy_course(master_id="10-809-195reidoer", copy_id="discussion_test")
    #pass
    #for c in courses:
        #enroll_user(user_ID="120250693", course_id=c, role="Instructor")
    #get_user_courses(user_id="120170412")
   # create_empty_course("")
    #delete_course("dad_test")

    # create_user(username="10000009", f_name="david", l_name="davidson", email="")
    ##get_user_courses(user_id="500162037")
    # create_empty_course(course_name="Gen. Anatomy & Physiology (Section 2) (Online)", course_id="10806177DE-2-2024fall")
    # create_empty_course(course_name="Adv. Anatomy & Physiology (Section 3)",course_id="10806179-3-2024fall")
    # create_empty_course(course_name="Plant Identification (Section 4)",course_id="10057140-4-2024fall")


    #remove_by_role(course_id="testing_course_000", role="Student")

    ##my_guys = get_users_in_course(course_id="testing_course_000", role="Student")

   



    ##for u in my_guys:
       ### unenroll_user(get_username_from_id(user_id=u.get("userId")), course_id="testing_course_000")
