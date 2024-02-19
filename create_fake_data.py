from faker import Faker

fake = Faker([ 'es_ES'])
names = [fake.name()[:15] for _ in range(100)] # 100 names, max 15 chars

with open("names-fake.txt", "w") as f:
    f.write("\n".join(names))