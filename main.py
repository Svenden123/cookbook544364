class Meal:
    def __init__(self, name='', items=None):
        self.name = name
        self.items = items

    def transform(self):
        return {self.name: [item.transform() for item in self.items]}


class Item:
    def __init__(self, name='', count=0, unit=''):
        self.name = name
        self.count = count
        self.unit = unit

    def transform(self):
        return {'ingridient_name': self.name, 'quantity': self.count,
                'measure': self.unit}


def get_shop_list_by_dishes(dishes, person_c):
    items = {}
    cook_book = get_cook_book()
    for mealName in dishes:
        meal_items = cook_book[mealName]
        for mealItem in meal_items:
            if not items.get(mealItem['ingridient_name']):
                items[mealItem['ingridient_name']] = {
                    'measure': mealItem['measure'],
                    'quantity': mealItem['quantity'] * person_c
                }
            else:
                ing_name = mealItem['ingridient_name']
                quantity = mealItem['quantity']
                items[ing_name]['quantity'] += quantity * person_c
    return items


def get_cooks_from_file(file_name='cookbook.dat'):
    buff_meal = None
    buff_items = []
    meals = []
    total = 1
    with open(file_name) as file:
        array = [row.strip() for row in file]
        for line in array:
            if not line:
                continue
            parts = [part.strip() for part in line.split('|')]
            if len(parts) == 3:
                buff_items.append(Item(parts[0], int(parts[1]), parts[2]))
            elif len(parts) == 1:
                if parts[0].isdigit():
                    total = int(parts[0])
                else:
                    if buff_meal is not None:
                        buff_meal.items = buff_items[:total]
                        buff_items = []
                        meals.append(buff_meal)
                    buff_meal = Meal(parts[0])
            else:
                print(file_name + ' file was ruined, check it')
                exit(1)

    return [meal.transform() for meal in meals]


def get_cook_book():
    cook_book = {}
    for meal in get_cooks_from_file():
        cook_book.update(meal)
    return cook_book
