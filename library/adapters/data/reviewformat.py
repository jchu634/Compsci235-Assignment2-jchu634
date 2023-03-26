# flag = True
# input_file = open("users.csv","r")
# user_reference = {}
# for line in input_file:
#     if flag:
#         flag = False
#     else:
#         temp = line.strip().split(',')
#         user_reference[temp[1]] = temp[0]
# input_file.close()
# flag = True
# # print(user_reference)
# input_file = open("reviews.csv","r")
# write_file = open("new_reviews.csv","w")

# for line in input_file:
#     if flag:
#         flag = False
#         write_file.write(','.join(line.strip().split(','))+'\n')
#     else:
#         temp_line = line.strip().split(',')
#         temp_line[2] = temp_line[2].replace(".","").replace("_","").replace("-","")
#         write_file.write(','.join(temp_line)+'\n')
#     # print(line.strip().split(','))
#     # print(','.join(line.strip().split(',')))
#     # input()
        
# input_file.close()
# write_file.close()
flag = True
input_file = open("reviews.csv","r")
write_file = open("new_reviews.csv","w")

for line in input_file:
    if flag:
        flag = False
        write_file.write(','.join(line.strip().split(','))+'\n')
    else:
        temp_line = line.strip().split(',')
        temp_line[0] = str(int(temp_line[0])-1)
        write_file.write(','.join(temp_line)+'\n')
input_file.close()
write_file.close()
# flag = True
# input_file = open("reviews.csv","r")
# write_file = open("new_reviews.csv","w")

# for line in input_file:
#     if flag:
#         flag = False
#         write_file.write(','.join(line.strip().split(','))+'\n')
#     else:
#         temp_line = line.strip().split(',')
#         temp_line[2] = temp_line[2].replace(".","")
#         write_file.write(','.join(temp_line)+'\n')
#     # print(line.strip().split(','))
#     # print(','.join(line.strip().split(',')))
#     # input()
        
# input_file.close()
# write_file.close()