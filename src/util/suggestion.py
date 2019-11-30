import operator

buff_to_steam_suggestions = {
    '单位价钱收益最大——': 'gap_percent',
    '差价最大——': 'gap'
}

steam_to_buff_suggestions = {
    '单位价钱收益最大——': 'gap_percent',
    '差价最大——': 'gap'
}


def suggest(csgo_items):
    print()
    print('buff买steam卖：')
    for info, column in buff_to_steam_suggestions.items():
        print()
        output_high_to_low(csgo_items, info, column)

    print()
    print('steam买buff卖：')
    for info, column in steam_to_buff_suggestions.items():
        print()
        output_low_to_high(csgo_items, info, column)


def output_high_to_low(csgo_items, suggestion, column):
    print(suggestion)
    csgo_items.sort(key=operator.attrgetter(column), reverse=True)
    for gap_percent_most_item in csgo_items[:30]:
        print(gap_percent_most_item.detail())


def output_low_to_high(csgo_items, suggestion, column):
    print(suggestion)
    csgo_items.sort(key=operator.attrgetter(column), reverse=False)
    for gap_percent_most_item in csgo_items[:30]:
        print(gap_percent_most_item.detail())
