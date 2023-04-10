import os
import dmesg_reader

"""
@brief:     This function opens the given file and count the 
            occurence of error
@input:     filename, name of the file
@ouput:     number of error

"""

def getErrorCountFromDmesg(filename):
    # Read the log and count the number of errors
    dmesg_file = open(filename, "r")
    lines = dmesg_file.readlines()
    error_names = ["error", "failed", "stopped"]
    error_count = 0

    for l in lines:
        for e in error_names:
            if e in l.lower():
                error_count += 1
    dmesg_file.close()
    
    return error_count

"""
@brief:     This function calls the dmesg_reader.py with the given file and count the 
            occurence of error in the JSON output file
@input:     filename, name of the file
@ouput:     number of error in the JSON output file

"""

def getErrorCountFromTheReader(filename, until):
    cmd = 'python3 dmesg_reader.py -i {0} -o output_test.json -u {1}'.format(filename, until)
    os.system(cmd)
    json_error_file = open("output_test.json", "r")
    error_lines = json_error_file.readlines()
    error_names = ["error", "failed", "stopped"]
    json_error_count = 0

    for je in error_lines:
        for e in error_names:
            if e in je.lower():
                json_error_count += 1
    
    json_error_file.close()
    os.system('rm output_test.json')

    return json_error_count


def main():

    # Test for dmesg.log file

    # Read the log and count the number of errors
    error_dmesg = getErrorCountFromDmesg("dmesg.log")
    
    # Run the reader script with the same file and get the errors
    # The error count should be same for both file 
    error_json = getErrorCountFromTheReader("dmesg.log", 0)
    
    if error_dmesg == error_json:
        print("Found the errors successfully")
    else:
        print("Couldn't find the errors. Please check the reader")

    # Test for empty.log
    empty_log_json = getErrorCountFromTheReader("empty.log", 0)

    if empty_log_json == 0:
        print("Found the errors successfully")
    else:
        print("Couldn't find the errors. Please check the reader")

    # Test with dmesg_error_test.log
    # This file has 5 errors in 2023-03-08, 3 errors in 2023-03-07,
    # 1 error in 2023-03-06, 3 errors in 2023-03-02
    test_log_error = getErrorCountFromTheReader("dmesg_error_test.log", "2023-03-08")

    if test_log_error == 5:
        print("Found the errors successfully")
    else:
        print("Couldn't find the errors. Please check the reader")

    test_log_error = getErrorCountFromTheReader("dmesg_error_test.log", "2023-03-07")

    if test_log_error == 8:
        print("Found the errors successfully")
    else:
        print("Couldn't find the errors. Please check the reader")

    test_log_error = getErrorCountFromTheReader("dmesg_error_test.log", "2023-03-06")

    if test_log_error == 9:
        print("Found the errors successfully")
    else:
        print("Couldn't find the errors. Please check the reader")

    test_log_error = getErrorCountFromTheReader("dmesg_error_test.log", "2023-03-05")

    if test_log_error == 9:
        print("Found the errors successfully")
    else:
        print("Couldn't find the errors. Please check the reader")

    test_log_error = getErrorCountFromTheReader("dmesg_error_test.log", "2023-03-02")

    if test_log_error == 12:
        print("Found the errors successfully")
    else:
        print("Couldn't find the errors. Please check the reader")

if __name__ == "__main__":
    main()