from transliterate import translit
import pprint

def get_regions_map(regions_data: list) -> dict:
    print(regions_data)
    mapping_table = {}
    if regions_data[0] and regions_data[1]:
        first_bookmkr = list(regions_data[0].keys())[0]
        second_bookmkr = list(regions_data[1].keys())[0]
        first_bookmkr_regions = set()
        second_bookmkr_regions = set()
        for region_data in regions_data:
            if region_data.get(first_bookmkr):
                for region in region_data[first_bookmkr]:
                    first_bookmkr_regions.add(translit(region.lower(), 'ru'))
            elif region_data.get(second_bookmkr):
                for region in region_data[second_bookmkr]:
                    second_bookmkr_regions.add(translit(region.lower(), 'ru'))
        matching_regions = second_bookmkr_regions & first_bookmkr_regions

        for matching_region in matching_regions:
            for region_data in regions_data:
                if region_data.get(first_bookmkr):
                    for region in region_data[first_bookmkr]:
                        if translit(region.lower(), 'ru') == matching_region:
                            if not mapping_table.get(matching_region):
                                mapping_table[matching_region] = {
                                    first_bookmkr: {
                                        region: region_data[first_bookmkr][region]
                                    }
                                }
                            else:
                                mapping_table[matching_region][first_bookmkr] = {
                                        region: region_data[first_bookmkr][region]
                                    }
                elif region_data.get(second_bookmkr):
                    for region in region_data[second_bookmkr]:
                        if translit(region.lower(), 'ru') == matching_region:
                            if not mapping_table.get(matching_region):
                                mapping_table[matching_region] = {
                                    second_bookmkr: {
                                        region: region_data[second_bookmkr][region]
                                    }
                                }
                            else:
                                mapping_table[matching_region][second_bookmkr] = {
                                    region: region_data[second_bookmkr][region]
                                }

    return mapping_table

def get_leagues_map(regions_data: list) -> dict:
    """IN PROGRESS...."""
    print(regions_data)
    mapping_table = {}
    if regions_data[0] and regions_data[1]:
        first_bookmkr = list(regions_data[0].keys())[0]
        second_bookmkr = list(regions_data[1].keys())[0]
        first_bookmkr_regions = set()
        second_bookmkr_regions = set()
        for region_data in regions_data:
            if region_data.get(first_bookmkr):
                for region in region_data[first_bookmkr]:
                    first_bookmkr_regions.add(translit(region.lower(), 'ru'))
            elif region_data.get(second_bookmkr):
                for region in region_data[second_bookmkr]:
                    second_bookmkr_regions.add(translit(region.lower(), 'ru'))
        matching_regions = second_bookmkr_regions & first_bookmkr_regions

        for matching_region in matching_regions:
            for region_data in regions_data:
                if region_data.get(first_bookmkr):
                    print(region_data.get(first_bookmkr))
                    for region in region_data[first_bookmkr]:
                        if translit(region.lower(), 'ru') == matching_region:
                            if not mapping_table.get(matching_region):
                                mapping_table[matching_region] = {first_bookmkr: region_data[first_bookmkr][region]}
                            else:
                                mapping_table[matching_region][first_bookmkr] = region_data[first_bookmkr][region]
                elif region_data.get(second_bookmkr):
                    for region in region_data[second_bookmkr]:
                        if translit(region.lower(), 'ru') == matching_region:
                            if not mapping_table.get(matching_region):
                                mapping_table[matching_region] = {second_bookmkr: region_data[second_bookmkr][region]}
                            else:
                                mapping_table[matching_region][second_bookmkr] = region_data[second_bookmkr][region]

    return mapping_table

if __name__ == '__main__':

    pass


### пример вывода get_regions_map###

# {'австралия': {'betboom': {'country_name': 'Австралия',
#                            'req_params': {'countryCode': None,
#                                           'countryId': 1224,
#                                           'langId': 1,
#                                           'partnerId': 147,
#                                           'timeFilter': 0}},
#                'leon': {'country_name': 'Австралия',
#                         'league_id': 1970324836987201,
#                         'league_name': 'Премьер-лига U23'}},
# }