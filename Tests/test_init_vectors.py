import json

def update_vectors():
    status_vector = dict()
    status_vector['GPS'] = 1  # 1
    status_vector['COMPASS'] = 1  # 1
    #status_vector = {"one":10, "two":20}
    json.dump(status_vector, open("init_vectors_file.txt",'w'))

def init_vectors():
    status_vector = dict()
    status_vector = json.load(open("file_init_status_vector.txt"))
    print(status_vector)
    status_vector['GPS'] += 1
    json.dump(status_vector, open("file_init_status_vector.txt",'w'))

def test():
    status_vector = json.load(open("file_init_status_vector.txt"))
    command_vector = json.load(open("file_init_command_vector.txt"))
    print(status_vector['TEMP'])
    print(command_vector['REBOOT_SLAVE'])
    command_vector['DEP'] = 1
    json.dump(status_vector, open("file_init_status_vector.txt",'w'))
    json.dump(command_vector, open("file_init_command_vector.txt",'w'))

def test_pose():
    position = json.load(open("file_init_position.txt"))
    counter_for_overlap = json.load(open("file_init_counter.txt"))
    print(position)
    print(counter_for_overlap)
    position = 10
    counter_for_overlap = 370
    json.dump(position, open("file_init_position.txt", 'w'))
    json.dump(counter_for_overlap, open("file_init_counter.txt", 'w'))

if __name__ == '__main__':
    #update_vectors()
    #init_vectors()
    test_pose()
