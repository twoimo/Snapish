from korean_lunar_calendar import KoreanLunarCalendar

eight_mulddae_cycle = {
    1: '8물', 2: '9물', 3: '10물', 4: '11물', 5: '12물', 6: '13물', 7: '14물',
    8: '조금', 9: '1물', 10: '2물', 11: '3물', 12: '4물', 13: '5물', 14: '6물', 15: '7물',
    16: '8물', 17: '9물', 18: '10물', 19: '11물', 20: '12물', 21: '13물', 22: '14물',
    23: '조금', 24: '1물', 25: '2물', 26: '3물', 27: '4물', 28: '5물', 29: '6물', 30: '7물'
}

seven_mulddae_cycle = {
    1: '7물', 2: '8물', 3: '9물', 4: '10물', 5: '11물', 6: '12물', 7: '13물',
    8: '조금', 9: '무시', 10: '1물', 11: '2물', 12: '3물', 13: '4물', 14: '5물', 15: '6물',
    16: '7물', 17: '8물', 18: '9물', 19: '10물', 20: '11물', 21: '12물',
    22: '13물', 23: '조금', 24: '무시', 25: '1물', 26: '2물', 27: '3물', 28: '4물', 29: '5물', 30: '6물'
}

def get_mulddae_cycle(nowdate):
    # Calendar 불러오기
    calendar = KoreanLunarCalendar()

    # 오늘 날짜 기준으로 Set
    calendar.setSolarDate(nowdate.year,
                        nowdate.month,
                        nowdate.day)

    lunar_nowdate = calendar.LunarIsoFormat()
    lunar_nowdate_day = int(lunar_nowdate.split("-")[-1])
    
    seohae_mulddae = seven_mulddae_cycle[lunar_nowdate_day]
    other_mulddae = eight_mulddae_cycle[lunar_nowdate_day]
    
    return seohae_mulddae, other_mulddae
    