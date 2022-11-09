import json


def main():
  with open("items.json") as read_file:
    data = json.load(read_file)
  list = data.values()
  list = ("\n".join(list)).split()
  print(list[0])

if __name__ == "__main__":
  main()