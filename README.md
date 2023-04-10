This folder contains a python script, dmesg_reader.py that reads and parses a input log file (linx kernel ring buffer log, dmesg) and finds the errors within the file. The errors are given in an output file with JSON format. The errors are printed out by the script too. There's a test file dmesg_reader_test.py, which tests the dmesg_reader.py against a few input file. There're three log files for testing purpose. The files are executed and tested in Windows environment

To run the the script,
python3 dmesg_reader.py -i {input} -o {output} -u {until}
where,
    -i expects the input file name
    -o expects the output file name
    -u until the time the errors are read. If until is 0, the script reads the errors form the whole file, otherwise it reads the error from the given date to till now
    The date should be in yyyy-mm-dd format

Example:
python3 dmesg_reader.py -i dmesg.log -o output.json -u 0
python3 dmesg_reader.py -i dmesg.log -o output.json -u 2023-02-24

To run the test script,
python3 dmesg_reader_test.py