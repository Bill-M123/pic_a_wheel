from cards import Cards

def test_get_simple_u_card_h():
    cards2=Cards()
    tmp=cards2.get_simple_u_card_h((7,'S'))
    assert tmp == (7,'&#9824')
    tmp=cards2.get_simple_u_card_h((4,'C'))
    assert tmp == (4,'&#9827')
    tmp=cards2.get_simple_u_card_h((11,'H'))
    assert tmp == (11,'&#9825')
    tmp=cards2.get_simple_u_card_h((1,'D'))
    assert tmp == (1,'&#9830')

def test_get_simple_u_card_p():
    cards2=Cards()
    tmp=cards2.get_simple_u_card_p((7,'S'))
    assert tmp == (7,'\u2660')
    tmp=cards2.get_simple_u_card_p((4,'C'))
    assert tmp == (4,'\u2663')
    tmp=cards2.get_simple_u_card_p((11,'H'))
    assert tmp == (11,'\u2665')
    tmp=cards2.get_simple_u_card_p((1,'D'))
    assert tmp == (1,'\u2666')
