# Reading the class.txt file
dict_1 = dict()

file = open('class.txt', 'r')

for line in file:
    # Splitting only on first instance of '-' to separate prof names from courses taught since a line can contain multiple '-'
    name_course_split = line.split('-',1)   
    
    prof_name = name_course_split[0].strip()    # remove leading and trailing white spaces
    course_list = name_course_split[1].lstrip().split('|')    # remove leading white spaces

    course_list[-1] = course_list[-1].strip()    # remove new-line character from last element in course_list
    
    dict_1[prof_name] = course_list    # add line to dictionary
    
    
"""
 Handling duplicate prof names in dict_1 and getting only prof's last name

The professor's last name is a unique identifier for the name of the professor.

Normally, the professor's last name comes after their first name. But when the name is in comma separated form, the first name comes after the last name.

Eg: Kshemkalyani, Ajay -> Last name: Kshemkalyani

"""  
dict_2 = dict()

for key in dict_1.keys():
    # Handle names of format 'last_name, first_name'
    if ',' in key:
        prof_last_name = key.split(',')[0].lower()


    # Handle names of format 'first_name middle_initial. last_name' and 'first_name.last_name'
    elif '.' in key:
        if (' ') in key:
            prof_last_name = key.split(' ')[-1].strip().lower()
        else:
            prof_last_name = key.split('.')[-1].strip().lower()

    # Handle names of format 'first_name last_name' or 'first_name middle_name last_name'
    else:
        prof_last_name = key.split(' ')[-1].strip().lower()

    # Check if prof already exists/ added to dictionary   
    # if not then add prof_last_name as key in dict_2 with value as value of corresponding key in dict_1
    # else, if already present in dict_2, then extend value list (course list) of key in dict_2 with additional 
    # value (couse list) from corresponding key in dict_1
    if dict_2.get(prof_last_name) == None:
        dict_2[prof_last_name] = dict_1[key]
    else:
        dict_2[prof_last_name].extend(dict_1[key])   


# Write to cleaned.txt file after processing

# sort prof names
prof_names_list = []

for key in dict_2.keys():
    prof_names_list.append(key)

prof_names_list.sort()

file = open('cleaned.txt','w')

# write to file; name will be fetched in sorted order since prof_name_list is sorted alphabetically
for name in prof_names_list:
    line = ''
    courses = ''
    prof_course_list = dict_2[name]

    # Capitalize only first letter of each course and sort courses alphabetically 
    for i in range(len(prof_course_list)):
        prof_course_list[i] = prof_course_list[i].capitalize()
    
    prof_course_list.sort()
    
    courses = '|'.join(prof_course_list)
        
    line += name.capitalize() + ' - ' + courses + '\n'
    
    file.write(line)
    
file.close()