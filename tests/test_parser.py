import tokenizer as toke


def test_id_paren():
    assert toke.id_paren('(3+4)') == '(___)'

def