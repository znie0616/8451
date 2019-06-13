import requests
import pytest

host = 'http://127.0.0.1:5000/8451'


@pytest.mark.parametrize('words',
                         [
                             'qyl psltfj,kzfj',  # test diagonal
                             'jftlsp lyq,jfzk'  # test diagonal reversed
                             'vnpwo,GFT',  # test counter diagonal
                             'owpnv,tfg'  # test counter diagonal reversed
                             'quyqxorruv,SGPJW',  # test horizontal
                             'vurroxqyuq,WJPGS',  # test horizontal reversed
                             'QSOYSK,UNRYFR',  # test vertical
                             'KSYOSQ,RFYRNU'  # test vertical reversed
                         ])
def test_positive(words):
    payload = {'words': words}
    res = requests.get(host, params=payload)
    assert 200 == res.status_code


@pytest.mark.parametrize('words',
                         [
                             '',  # invalid input
                             'vamos,chicago'  # words not on the board
                         ])
def test_nagative(words):
    payload = {'words': words}
    res = requests.get(host, params=payload)
    assert 400 == res.status_code
