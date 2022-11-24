from tg_client import *
#import pytest

def test_process_period():
    assert process_period("02.03.2022 - 04.03.2022") == [date(2022, 3, 2), date(2022, 3, 4)]
    assert process_period("02.03.2022") == [date(2022, 3, 2), date(2022, 3, 2)]
    assert process_period("21e13 sdawd") == "Wrong format"
    assert process_period("02.03.2023") == "The future has not come yet!"
    assert process_period("02.03.2022 - 01.02.2021") == "Wrong order for this date"


if __name__=='__main__':
    session = TG_client(session_name='Test',api_id='14944054',api_hash='606105bdb95252c3ed205feaba3536ff')
    print(session.auth('89158969245'))


    #session.send_message('me', 'Hello to myself!')