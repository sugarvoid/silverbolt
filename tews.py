
from bb_lib.course import create_empty_course

courses: list =[ 
    ["Commercial Flight 3A","10402181"],
    ["Commercial Flight 3B","10402182"],
    ["Commercial Flight 4","10402154"],
    ["CFI 1A","10402190"],
    ["CFI 1B","10402184"],
    ["CFI 2A","10402187"],
    ["CFI 2B","10402188"],
    ["CFI 3","10402173"],
    ["CFI 4","10402174"],
    ["CFI 5","10402175"],



]


def make_air_course(basename: str, catalog_num: str) -> None:
    #file_name = f"data/temp/{basename}.txt"
    for i in range(6):
        new_name = f"{basename} (Section {i+2})"
        new_id = f"{catalog_num}-{i+2}-2024fall"

        #print(f"Name: {new_name}     ID: {new_id}")
        create_empty_course(course_id=new_id, course_name=new_name)

        #with open(file_name, 'a+') as f:
        #    f.write(f"{new_id},")


for x in courses: 
    make_air_course(basename=x[0], catalog_num=x[1])
    
