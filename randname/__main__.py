# __main__.py
from randname import randname

def main():
    return f"{randname.first_name()} {randname.last_name()}"

if __name__ == "__main__":
    print(main())