

import requests
from bb_lib.course import run_course_copy, create_empty_course, get_user_courses, delete_course, enroll_user
from bb_lib.user import does_user_exist
from bb_lib.fvtc import trent_enrollment


course = [
    "33768",
"33771",
"33772",
"34956",
"40016",
"40015",
]


if __name__ == "__main__":
    pass
    #print(does_user_exist("500162037"))
    #run_course_copy("data/course_copy.csv")

    #get_user_courses("120250303")

    #trent_enrollment(course_id="40551", add=False)


    # create_empty_course("10402113-2-2024fall", "Private Pilot 1A (Section 2)")
    # create_empty_course("10402113-3-2024fall", "Private Pilot 1A (Section 3)")
    # create_empty_course("10402113-4-2024fall", "Private Pilot 1A (Section 4)")
    # create_empty_course("10402113-5-2024fall", "Private Pilot 1A (Section 5)")
    # create_empty_course("10402113-6-2024fall", "Private Pilot 1A (Section 6)")
    # create_empty_course("10402113-7-2024fall", "Private Pilot 1A (Section 7)")

    # create_empty_course("10402115-2-2024fall", "Private Pilot 1B (Section 2)")
    # create_empty_course("10402115-3-2024fall", "Private Pilot 1B (Section 3)")
    # create_empty_course("10402115-4-2024fall", "Private Pilot 1B (Section 4)")
    # create_empty_course("10402115-5-2024fall", "Private Pilot 1B (Section 5)")
    # create_empty_course("10402115-6-2024fall", "Private Pilot 1B (Section 6)")
    # create_empty_course("10402115-7-2024fall", "Private Pilot 1B (Section 7)")

    # create_empty_course("10402122-2-2024fall", "Private Pilot 2 (Section 2)")
    # create_empty_course("10402122-3-2024fall", "Private Pilot 2 (Section 3)")
    # create_empty_course("10402122-4-2024fall", "Private Pilot 2 (Section 4)")
    # create_empty_course("10402122-5-2024fall", "Private Pilot 2 (Section 5)")
    # create_empty_course("10402122-6-2024fall", "Private Pilot 2 (Section 6)")
    # create_empty_course("10402122-7-2024fall", "Private Pilot 2 (Section 7)")

    # create_empty_course("10402125-2-2024fall", "Private Pilot 3 (Section 2)")
    # create_empty_course("10402125-3-2024fall", "Private Pilot 3 (Section 3)")
    # create_empty_course("10402125-4-2024fall", "Private Pilot 3 (Section 4)")
    # create_empty_course("10402125-5-2024fall", "Private Pilot 3 (Section 5)")
    # create_empty_course("10402125-6-2024fall", "Private Pilot 3 (Section 6)")
    # create_empty_course("10402125-7-2024fall", "Private Pilot 3 (Section 7)")

    # create_empty_course("10402126-2-2024fall", "Instrument Flight 1 (Section 2)")
    # create_empty_course("10402126-3-2024fall", "Instrument Flight 1 (Section 3)")
    # create_empty_course("10402126-4-2024fall", "Instrument Flight 1 (Section 4)")
    # create_empty_course("10402126-5-2024fall", "Instrument Flight 1 (Section 5)")
    # create_empty_course("10402126-6-2024fall", "Instrument Flight 1 (Section 6)")
    # create_empty_course("10402126-7-2024fall", "Instrument Flight 1 (Section 7)")

    # create_empty_course("10402116-2-2024fall", "Instrument Flight 2A (Section 2)")
    # create_empty_course("10402116-3-2024fall", "Instrument Flight 2A (Section 3)")
    # create_empty_course("10402116-4-2024fall", "Instrument Flight 2A (Section 4)")
    # create_empty_course("10402116-5-2024fall", "Instrument Flight 2A (Section 5)")
    # create_empty_course("10402116-6-2024fall", "Instrument Flight 2A (Section 6)")
    # create_empty_course("10402116-7-2024fall", "Instrument Flight 2A (Section 7)")

    # create_empty_course("10402117-2-2024fall", "Instrument Flight 2B (Section 2)")
    # create_empty_course("10402117-3-2024fall", "Instrument Flight 2B (Section 3)")
    # create_empty_course("10402117-4-2024fall", "Instrument Flight 2B (Section 4)")
    # create_empty_course("10402117-5-2024fall", "Instrument Flight 2B (Section 5)")
    # create_empty_course("10402117-6-2024fall", "Instrument Flight 2B (Section 6)")
    # create_empty_course("10402117-7-2024fall", "Instrument Flight 2B (Section 7)")
    
    # create_empty_course("10402128-2-2024fall", "Instrument Flight 3 (Section 2)")
    # create_empty_course("10402128-3-2024fall", "Instrument Flight 3 (Section 3)")
    # create_empty_course("10402128-4-2024fall", "Instrument Flight 3 (Section 4)")
    # create_empty_course("10402128-5-2024fall", "Instrument Flight 3 (Section 5)")
    # create_empty_course("10402128-6-2024fall", "Instrument Flight 3 (Section 6)")
    # create_empty_course("10402128-7-2024fall", "Instrument Flight 3 (Section 7)")

    # create_empty_course("10402118-2-2024fall", "Commercial Flight 1A (Section 2)")
    # create_empty_course("10402118-3-2024fall", "Commercial Flight 1A (Section 3)")
    # create_empty_course("10402118-4-2024fall", "Commercial Flight 1A (Section 4)")
    # create_empty_course("10402118-5-2024fall", "Commercial Flight 1A (Section 5)")
    # create_empty_course("10402118-6-2024fall", "Commercial Flight 1A (Section 6)")
    # create_empty_course("10402118-7-2024fall", "Commercial Flight 1A (Section 7)")

    # create_empty_course("10402119-2-2024fall", "Commercial Flight 1B (Section 2)")
    # create_empty_course("10402119-3-2024fall", "Commercial Flight 1B (Section 3)")
    # create_empty_course("10402119-4-2024fall", "Commercial Flight 1B (Section 4)")
    # create_empty_course("10402119-5-2024fall", "Commercial Flight 1B (Section 5)")
    # create_empty_course("10402119-6-2024fall", "Commercial Flight 1B (Section 6)")
    # create_empty_course("10402119-7-2024fall", "Commercial Flight 1B (Section 7)")

    # create_empty_course("10402121-2-2024fall", "Commercial Flight 2A (Section 2)")
    # create_empty_course("10402121-3-2024fall", "Commercial Flight 2A (Section 3)")
    # create_empty_course("10402121-4-2024fall", "Commercial Flight 2A (Section 4)")
    # create_empty_course("10402121-5-2024fall", "Commercial Flight 2A (Section 5)")
    # create_empty_course("10402121-6-2024fall", "Commercial Flight 2A (Section 6)")
    # create_empty_course("10402121-7-2024fall", "Commercial Flight 2A (Section 7)")

    # create_empty_course("10402129-2-2024fall", "Commercial Flight 2B (Section 2)")
    # create_empty_course("10402129-3-2024fall", "Commercial Flight 2B (Section 3)")
    # create_empty_course("10402129-4-2024fall", "Commercial Flight 2B (Section 4)")
    # create_empty_course("10402129-5-2024fall", "Commercial Flight 2B (Section 5)")
    # create_empty_course("10402129-6-2024fall", "Commercial Flight 2B (Section 6)")
    # create_empty_course("10402129-7-2024fall", "Commercial Flight 2B (Section 7)")