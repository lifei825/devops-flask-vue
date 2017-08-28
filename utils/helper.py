import uuid
import random


def identifying():
    part1 = list(str(uuid.uuid1(node=random.randint(100000, 110000), clock_seq=random.randint(20, 100))))
    part2 = [chr(random.randint(65, 122)) for i in range(24)]
    part3 = part1 + part2

    return "".join(random.sample(part3, len(part3)))

if __name__ == "__main__":
    for i in range(20):
        uid = identifying()
        print(str(uid))
