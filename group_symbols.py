import csv

stary_symbol_input = input("Podaj ścieżkę do starego symbolu\n")
nowy_symbol_input = input("Podaj ścieżkę do nowego symbolu\n")

stary_symbol_input2 = (
    stary_symbol_input
    .replace("\\", "/")
    .replace('"', "")
)

nowy_symbol_input2 = (
    nowy_symbol_input
    .replace("\\", "/")
    .replace('"', "")
)

stary_symbol = stary_symbol_input2
nowy_symbol = nowy_symbol_input2

grupa_1 = {}
grupa_2 = {}


with open(stary_symbol, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if len(row) > 15:
            name = row[1]
            markup = row[5]
            markdown = row[6]
            leverage = row[15]

            grupa_1[name] = {
                'markup': markup,
                'markdown': markdown,
                'leverage': leverage
            }

with open(nowy_symbol, newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)
    for row in reader:
        if len(row) > 15:
            name = row[1]
            markup = row[5]
            markdown = row[6]
            leverage = row[15]

            grupa_2[name] = {
                'markup': markup,
                'markdown': markdown,
                'leverage': leverage
            }

# print(grupa_1)
# print(grupa_2)

# unikalne = {}
# for name, attrs in grupa_1.items():
#     if name not in grupa_2 and float(attrs['markup']) != 0 or float(attrs['markdown']) != 0 or str(attrs['leverage']) != "null":
#         unikalne[name] = attrs



roznice = {
    name: {
        'grupa_1': attrs,
        'grupa_2': grupa_2.get(name)
    }
    for name, attrs in grupa_1.items()
    if (
        name not in grupa_2
        or attrs['markup']   != grupa_2[name]['markup']
        or attrs['markdown'] != grupa_2[name]['markdown']
        or attrs['leverage'] != grupa_2[name]['leverage']
    )
}

# print(roznice)
for name, diff in roznice.items():
    print(f"{name}: stary symbol -> {diff['grupa_1']}, nowy symbol -> {diff['grupa_2']}")


