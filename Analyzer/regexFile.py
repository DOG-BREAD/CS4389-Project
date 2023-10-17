import re

def main():
    
    #open the file
    file = open('plain.txt', 'r')
    data = (file.read())
    data = re.sub('\n', ' ', data)

    # Define the regular expression pattern for splitting by '/' or '>'
    pattern = re.compile(r'\s*[/:> ]+\s*')
    # Use re.split() to split the string
    split_data = re.split(pattern, data)

    # Print the result
    print(split_data)


if __name__=="__main__":
    main()