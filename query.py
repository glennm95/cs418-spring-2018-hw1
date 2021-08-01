# Reading all courses from cleaned.txt into a set (to get unique courses)

import sys

raw_file = sys.argv[1]
prof_name = sys.argv[-1]

# function to get similarity metric between two words

def word_similarity(w1, w2):
    l1 = list(w1)
    l2 = list(w2)    
    
    comparison_count = len(l1) if len(l1) < len(l2) else len(l2)
    common = 0
    
    # compare both words letter by letter in same order until the smaller word gets exhausted (comparison_count)
    # increment counter for common letters everytime the same letter is encountered in a word
    
    for i in range(comparison_count):
        if l1[i] == l2[i]:
            common += 1
            
    # Calculate similarity from ratio of common letters to no. of checks (comparison_count) made
    # Eg. 'Biomaterials' and 'Biomaterialz' will have high similarity since only last letters 's' and 'z' are different
    similarity = common/comparison_count
    
    return similarity


# function for getting Jaccard distance/ index of two words based on definition of Jaccard index

def jaccard_distance(w1,w2):
    s1 = set(w1.lower())
    s2 = set(w2.lower())
    
    jaccard_index = len(s1.intersection(s2))/len(s1.union(s2))

    return jaccard_index


# function for getting Jaccard value (average of Jaccard indices of words) of two strings

def jaccard_of_strings(s1,s2):
    l1 = s1.split()
    l2 = s2.split()
    
    loop_size = len(l1) if len(l1)<len(l2) else len(l2)
    total_jaccard = 0
    
    for i in range(loop_size):
        total_jaccard += jaccard_distance(l1[i], l2[i])

    avg_jacc = total_jaccard/loop_size
    
    return avg_jacc



def Q1(input_file):
    all_courses_set = set()

    file = open(raw_file,'r')

    for line in file:
        x = line.split(' - ', 1)
        for course in x[1].split('|'):
            
            # remove '/n' characters if present
            course = course.strip()
            
            # do some cleaning; replace '&' with 'and' and 'ii' with '2' for uniformity
            if '&' in course:
                course = course.replace('&', 'and')
            if ' ii' in course:
                course = course.replace(' ii', ' 2')
            all_courses_set.add(course)

    file.close()

    # convert to list and sort to get alphabetically ordered courses

    all_courses_list = list(all_courses_set)
    all_courses_list.sort()
    
   
    # Determining courses that are same but differentiated by minor spelling error and that need to be considered only once in 
    # final distinct courses set

    # keep a track of courses (course index positions) in all_courses_list that already have a match (high similarity) with one
    # of the preceding courses in the same list
    skip_course_pos = []   

    # add final distinct set of courses to this set
    all_courses_distinct = set()

# compare each ith course in all_courses_list to (i+1)th course (till nth course) in the same list
    for i in range(len(all_courses_list)):
        
        # if course already has a match (high similarity) in the list then skip that course and move to next one (continue keyword)
        if i in skip_course_pos:
            continue
        
        for j in range(i+1, len(all_courses_list)):
            
            # check if first letter of courses to be compared is equal, only then compare, else don't (course list is  
            # alphabetically sorted). This saves from a lot of unnecessary comparisons. Eg. 'Algorithms and big data'  
            # will be compared with 'Analytical geometry'and not with 'Temporalities'
            if all_courses_list[i][0] == all_courses_list[j][0]:    
                l1 = all_courses_list[i].split()
                l2 = all_courses_list[j].split()
                
                # check if course strings are equal in length since same courses will have equal no. of words
                if len(l1) == len(l2):    
                    count = 0
                    for k in range(len(l1)):
                        if word_similarity(l1[k], l2[k]) >= 0.7:    # calculate jaccard distance for each corresponding word
                            count += 1
                            if count == len(l1):    # reached the end of course string and all words are >=0.7 jaccard matches
                                skip_course_pos.append(j)    # add course index to list of i's to be skipped
                            continue
                        else:
                            break

                else:
                    continue    # course string not equal length then move on to the next j
            else: 
                break    
                # implies that current i doesn't have any similar course in list since it doesn't have another first letter match
            
        # add course to distinct set if it matches no other preceding courses in list
        all_courses_distinct.add(all_courses_list[i])
    return len(all_courses_distinct)
    
    
# Reading cleaned.txt file and storing contents in a prof_catalog dictionary
def write_file_to_dict(input_file):
    prof_catalog = dict()

    file = open('cleaned.txt','r')

    for line in file:
        x = line.split(' - ', 1)
        prof_catalog[x[0]] = x[1].strip().split('|')

    file.close()
    
    return prof_catalog
    
   
def Q2(input_file):
    prof_catalog = write_file_to_dict(input_file)

    last_name = prof_name.split(' ')[-1]
    value = prof_catalog[last_name.capitalize()]
    
    course_list = []
    for course in value:
        course_list.append(course)
        
    course_list.sort()
    
    text = ', '.join(course_list)
    
    return text


def Q3(input_file):
    # get profs teaching at least 5 courses
    prof_catalog = write_file_to_dict(input_file)

    prof_catalog_min_5_courses = dict()

    for key, value in prof_catalog.items():
        if len(value) >= 5:
            prof_catalog_min_5_courses[key] = value
            
    # comparing courses taught by each professor (who teaches at least 5 courses) for getting most aligned profs 
    # who teach similar courses

    prof_name_list = [key for key in prof_catalog_min_5_courses.keys()]

    most_aligned = []

    for i in range(len(prof_name_list)-1):
        c_list_1 = prof_catalog_min_5_courses.get(prof_name_list[i])
        

        for j in range(i+1, len(prof_name_list)):
            c_list_2 = prof_catalog_min_5_courses.get(prof_name_list[j])
            i_j_max = []

            for k in range(len(c_list_1)):    # k no. of courses in i-th list
                course_1 = c_list_1[k]
                jacc_list = []
                
                for n in range(len(c_list_2)):    # n no. of courses in j-th list
                    course_2 = c_list_2[n]
                    jacc_value = round(jaccard_of_strings(course_1, course_2),2)
                    jacc_list.append(jacc_value)
    #                 print(course_1+'--------'+course_2+'---',jacc_value)
                # k*n total jaccard values    
    #             print(jacc_list)
                i_j_max.append(max(jacc_list))
    #             print(prof_name_list[i], prof_name_list[j], max(jacc_list))    
                # jacc_list of size k = length of i-th list
    #         print(prof_name_list[i], prof_name_list[j], i_j_max, np.mean(i_j_max))
            
            if sum([ele>0.7 for ele in i_j_max]) >= 2:    # at least 2 courses are same between the profs
                most_aligned.append((prof_name_list[i], prof_name_list[j]))
                
    return most_aligned

    
    #         print('------------------')
    

def main():
    print(f'The dataset contains {Q1(raw_file)} distinct courses')
    print(f'\nCourses taught by Prof. {prof_name} are: {Q2(raw_file)}')
    most_aligned = Q3(raw_file)
    print('\nThe professors that have the most aligned teaching interests based on course titles are: ')
    for item in most_aligned:
        print(f'{item[0]} and {item[1]}')
    
 
if __name__ == '__main__':
    main()
    
