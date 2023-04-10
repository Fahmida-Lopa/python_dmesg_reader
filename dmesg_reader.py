import re
import argparse
import json
from datetime import datetime

"""
@brief:     This function read a given file
@input:     filename, name of the file
@output:    Contents of the file

"""


def parseFile(filename):
    # Read the contents of the dmesg.log file
    try:
        with open(filename, "r") as f:
            content = f.read()
            f.close()
    except FileNotFoundError:
        print("Error: dmesg log file is not found")
        return
    
    return content


"""
@brief:     This function finds error messages from the given log
            to until given date. If the given date is empty, it finds
            error messages from the whole log.
@input:     log, complete message
            date, a date for find the error until that date,
            it's either empty or a valid date in yyyy-mm-dd format
@output:    Error messages

"""


def findErrors(log, date):
    # Use regular expressions to find the relevant kernel messages
    pattern = r"\[(?P<timestamp>[^\]]+)\] (?P<message>.+)"
    error_messages = []
    error_names = ["error", "failed", "stopped"]

    try:
        for match in re.finditer(pattern, log):
            # Get the timestamp and message of a single line
            timestamp = match.group("timestamp")
            message = match.group("message")

            # Check whether the line contains any error
            for e in error_names:
                if e in message.lower():
                    # If there's no until timestamp,
                    # put the message into the output
                    if not date:
                        error_messages.append(
                            {"timestamp": timestamp, "message": message}
                        )

                    # Otherwise, check if the error is within the
                    # given timestamp
                    
                    elif(datetime.strptime(
                        timestamp, "%a %b %d %H:%M:%S %Y"
                        )
                        >= date
                    ):
                        error_messages.append(
                            {"timestamp": timestamp, "message": message}
                        )

        return error_messages
    except Exception:
        print("Error: while parsing the log file")
        return


"""
@brief:     This function writes the given text to a output file
            in JSON format
@input:     filename, name of the output file
            text, text to be written in the output file

"""


def writeOutputJSONFile(filename, text):
    # Write the messages to the output file
    try:
        with open(filename, "w") as f:
            json.dump(text, f, indent=4)
            f.close()
    except IOError:
        print("Error: Unable to write to output file")


"""
@brief:     This function prints the given message in the console
@input:     message, text to be printed

"""


def printMessage(message):
    # Print the messages in text format
    if not message:
        return
    for m in message:
        print("["f"{m['timestamp']}""] "f"{m['message']}")


"""
@brief:     Driver function for finding errors in a kernel log

"""


def main():
    parser = argparse.ArgumentParser(
        description="Reads the kernel buffer and outputs the results"
        "in a specified format."
    )
    parser.add_argument(
        "-i",
        "--input-file",
        type=str,
        required=True,
        help="The input file location (and name)",
    )
    parser.add_argument(
        "-o",
        "--output-file",
        type=str,
        required=True,
        help="The output file location (and name)",
    )
    parser.add_argument(
        "-u",
        "--until",
        type=str,
        default="0",
        help="The end date for how long back in time the buffer"
        "reading is done (in format yyyy-mm-dd)",
    )

    args = parser.parse_args()

    # Read the kernel log file
    dmesg_output = parseFile(args.input_file)

    # Get the date from input
    until_date = ""
    if args.until != "0":
        try:
            until_date = datetime.strptime(args.until, "%Y-%m-%d")
        except ValueError:
            print(
                "Error: Invalid date format for --until argument."
                "Please use yyyy-mm-dd format."
            )
            return

    # Find the error messages
    error_messages = findErrors(dmesg_output, until_date)

    # Write the error messages in JSON output
    writeOutputJSONFile(args.output_file, error_messages)

    # Print the errors in text format
    printMessage(error_messages)


if __name__ == "__main__":
    main()