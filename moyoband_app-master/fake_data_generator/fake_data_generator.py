import random
import csv
from time import sleep

"""Creates a csv file, in current working directory, with fake patients information.
Every row is a information about one patient in format:
 bed_id, first_name, last_name, heart_rate, temperature, medical_description, age, weight, medicaments"""


def r_first_name(first_names):
    return f'{first_names[random.randrange(0, len(first_names))]}'


def r_last_name(last_names):
    return f'{last_names[random.randrange(0, len(last_names))]}'


def r_name(first_names, last_names):
    return r_first_name(first_names) + ' ' + r_last_name(last_names)


def r_heart_rate(lower_hr, upper_hr):
    return random.randint(lower_hr, upper_hr)


def r_temperature(lower_temp, upper_temp):
    return round(random.uniform(lower_temp, upper_temp), 2)


def r_saturation(lower_sat, upper_sat):
    return round(random.uniform(lower_sat, upper_sat), 2)


def r_medical_description(letters):
    return f'{"".join([letters[random.randrange(0, len(letters) - i)] for i in range(len(letters))])}'


def r_age(lower_age, upper_age):
    return random.randint(lower_age, upper_age)


def r_weight(lower_weight, upper_weight):
    return random.randint(lower_weight, upper_weight)


def r_medicaments(medication):
    return ",".join({medication[random.randrange(0, len(medication))] for i in range(random.randint(0, 3))})


def main():
    rooms_num = 8
    beds_num = 8

    first_names = ['Jan', 'Karol', 'Kacper', 'Radosław', 'Bartosz', 'Mateusz', 'Wojciech', 'Jan', 'Stanisław',
                   'Andrzej',
                   'Józef', 'Tadeusz', 'Jerzy', 'Zbigniew', 'Krzysztof', 'Henryk', 'Ryszard', 'Kazimierz', 'Marek',
                   'Marian', 'Piotr', 'Janusz', 'Władysław', 'Adam', 'Wiesław', 'Zdzisław', 'Edward', 'Mieczysław',
                   'Roman', 'Mirosław', 'Grzegorz', 'Czesław', 'Maria', 'Krystyna', 'Anna', 'Barbara', 'Teresa',
                   'Elżbieta', 'Janina', 'Zofia', 'Jadwiga', 'Danuta', 'Halina', 'Irena', 'Ewa', 'Małgorzata', 'Helena',
                   'Grażyna', 'Bożena', 'Stanisława', 'Jolanta', 'Marianna', 'Urszula', 'Wanda', 'Alicja', 'Dorota',
                   'Agnieszka', 'Natalia']
    last_names = ['Nowak', 'Kowalski', 'Wiśniewski', 'Wójcik', 'Kowalczyk', 'Kamiński', 'Lewandowski', 'Zieliński',
                  'Szymański', 'Woźniak', 'Dąbrowski', 'Kozłowski', 'Jankowski', 'Mazur', 'Wojciechowski',
                  'Kwiatkowski', 'Krawczyk', 'Kaczmarek', 'Piotrowski', 'Grabowski']
    letters = [i for i in 'abcdefghijklmnoprstuwxyz  ABCDEFGHIJKLMNOPRSTUWXYZ']
    medication = [' Aspiryna', ' Nimesil', ' Acotin', ' Aflavic', ' Biofuroksym', ' Cabometyx', ' Doxagen', ' Equoral']

    lower_hr = 50
    upper_hr = 120

    lower_temp = 36
    upper_temp = 37.5

    lower_sat = 60
    upper_sat = 100

    lower_age = 18
    upper_age = 90

    lower_weight = 45
    upper_weight = 120

    # never ending while loop imitates constant flow of data from sensors
    # (names and surnames probably wouldn't change but its for testing purpose only)
    while True:
        with open('fake_data.txt', 'w', newline='', encoding="utf-8") as f:
            field_names = ['bed_id', 'first_name', 'last_name', 'heart_rate', 'temperature', 'saturation',
                           'medical_description', 'age', 'weight', 'medicaments']
            csv_writer = csv.writer(f)

            csv_writer.writerow(field_names)

            for i in range(1, rooms_num + 1):
                for j in range(1, beds_num + 1):
                    bed_id = i * 10 + j
                    if random.randint(0, 20) != 7:
                        first_name = r_first_name(first_names)
                        last_name = r_last_name(last_names)
                        heart_rate = r_heart_rate(lower_hr, upper_hr)
                        temperature = r_temperature(lower_temp, upper_temp)
                        saturation = r_saturation(lower_sat, upper_sat)
                        medical_description = r_medical_description(letters)
                        medical_description = medical_description[:20] + '\n' + medical_description[20:]
                        age = r_age(lower_age, upper_age)
                        weight = r_weight(lower_weight, upper_weight)
                        medicaments = r_medicaments(medication)
                        line = [bed_id, first_name, last_name, heart_rate, temperature, saturation, medical_description,
                                age, weight, medicaments]
                    else:
                        line = [bed_id]
                        for k in range(5):
                            line.append("-")
                        line.append("No Info\n")
                        for k in range(3):
                            line.append("-")
                    csv_writer.writerow(line)
        sleep(4)


if __name__ == '__main__':
    main()
