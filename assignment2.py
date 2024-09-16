import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    """Downloads the data from the given URL."""
    with urllib.request.urlopen(url) as response:
        web_data = response.read().decode('utf-8')
    return web_data

def processData(file_content):
    """Processes the CSV data."""
    person_dict = {}
    logging.basicConfig(filename="error.log", level=logging.ERROR)
    logger = logging.getLogger("assignment2")

    for data_line in file_content.split("\n"):
        if len(data_line) == 0:
            continue

        try:
            identifier, name, birthday = data_line.split(",")
            if identifier == "id":
                continue

            id_int = int(identifier)
            person_birthday = datetime.datetime.strptime(birthday.strip(), '%d/%m/%Y')
            person_dict[id_int] = (name, person_birthday)

        except ValueError as e:
            error_msg = f"Error processing line: {data_line} for ID #{identifier}. Error: {e}"
            logger.error(error_msg)

    return person_dict

def displayPerson(id, personData):
    """Displays the person's name and birthday."""
    if id in personData:
        name = personData[id][0]
        birthdate = datetime.datetime.strftime(personData[id][1], "%Y-%m-%d")
        print(f"Person # {id} is {name} with a birthday of {birthdate}")
    else:
        print ("No user found with that ID")

def main(url):
    print(f"Running main with URL = {url}...")
    data = downloadData(url)
    results_dict = processData(data)

    while True:
        try:
            id = int(input("Please enter ID to lookup: "))
            if id <= 0:
                break
            else:
                displayPerson(id, results_dict)
        except ValueError:
            print("Invalid input, Please enter a numeric ID.")

if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)

