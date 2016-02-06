
def title(message):
    front = message.split('$')[0].strip()
    if len(front) > 50:
        return front[:50]
    else:
        return front

def price(message):
    try:
        back = message.split('$')[1].strip()
        back = back.split(' ')[0].strip()
    except:
        return 'None'
    return '$' + back

def test_title():
    message = '5 shelf - BookShelf $21 - Pittsburgh, Pennsylvania  Good condition  Cash only  Book not included'
    assert(title(message) == '5 shelf - BookShelf')

def test_price():
    message = '5 shelf - BookShelf $21 - Pittsburgh, Pennsylvania  Good condition  Cash only  Book not included'
    assert(price(message) == '$21')

