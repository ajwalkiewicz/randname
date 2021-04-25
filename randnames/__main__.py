# __main__.py
from randnames import randnames

def main():
    return f"{randnames.first_name()} {randnames.last_name()}"

if __name__ == "__main__":
    print(main())