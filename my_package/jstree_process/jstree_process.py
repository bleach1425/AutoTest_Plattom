import yaml

class tree:
    def __init__(self):
        pass
    def Vip_history_yaml_process(casetype, CaseNumber, yamlname, account):
        jstree = []
        first_layer = 0
        second_layer = 0
        third_layer = 0
        four_layer = 0
        if casetype == 'Api':
            casetype = 'api'
            with open(f"Vip_Ram_Folder/{account}/{casetype}/{CaseNumber}/{yamlname}") as f:
                data = yaml.safe_load(f)
                for n in data:
                    if n == 'Environment':
                        first_layer += 1
                        item = {"id": f"json{first_layer}", "parent": "#", "text": n, "a_attr": {"style": "color : red"},
                                "state": {"opened": 'true'}}
                        jstree.append(item)
                        for key in data[n]:
                            if type(data[n][key]) == list:
                                for list_item in data[n][key]:
                                    second_layer += 1
                                    item = {"id": f"json{first_layer}-{second_layer}", "parent": f"json{first_layer}",
                                            "text": list_item, "state": {"opened": 'true'}}
                                    jstree.append(item)
                            elif type(data[n][key]) == dict:
                                for dict_key in data[n][key]:
                                    second_layer += 1
                                    item = {"id": f"json{first_layer}-{second_layer}", "parent": f"json{first_layer}",
                                            "text": dict_key, "state": {"opened": 'true'}}
                                    jstree.append(item)
                                    if type(data[n][key][dict_key]) == list:
                                        for list_item_second in data[n][key][dict_key]:
                                            third_layer += 1
                                            item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                                    "parent": f"json{first_layer}-{second_layer}",
                                                    "text": list_item_second, "state": {"opened": 'true'}}
                                            jstree.append(item)
                                    elif type(data[n][key][dict_key]) == dict:
                                        for dict_item_second in data[n][key][dict_key]:
                                            third_layer += 1
                                            item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                                    "parent": f"json{first_layer}-{second_layer}",
                                                    "text": data[n][key][dict_key][dict_item_second],
                                                    "state": {"opened": 'true'}}
                                            jstree.append(item)
                                    else:
                                        third_layer += 1
                                        item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                                "parent": f"json{first_layer}-{second_layer}",
                                                "text": data[n][key][dict_key],
                                                "state": {"opened": 'true'}}
                                        jstree.append(item)
                            else:
                                second_layer += 1
                                item = {"id": f"json{first_layer}-{second_layer}", "parent": f"json{first_layer}",
                                        "text": key, "state": {"opened": 'true'}}
                                jstree.append(item)
                                # (-----------------------------------------------)
                                third_layer += 1
                                item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                        "parent": f"json{first_layer}-{second_layer}",
                                        "text": data[n][key], "state": {"opened": 'true'}}
                                jstree.append(item)
                    elif n == "APIcommand" or n == "Configure":
                        first_layer += 1
                        item = {"id": f"json{first_layer}", "parent": "#", "text": n, "state": {"opened": 'true'}}
                        jstree.append(item)
                        for i, n1 in enumerate(data[n]):
                            # if n != 'except':
                            second_layer += 1
                            item = {"id": f"json{first_layer}-{second_layer}", "parent": f"json{first_layer}", "text": str(n1),
                                    "state": {"opened": 'true'}}
                            jstree.append(item)
                            if type(data[n][n1]) == dict:
                                for index, value in enumerate(data[n][n1]):
                                    if type(data[n][n1][value]) == list:
                                        for final_layer in data[n][n1][value]:
                                            four_layer += 1
                                            item = {"id": f"json{first_layer}-{second_layer}-{third_layer}-{four_layer}",
                                                    "parent": f"json{first_layer}-{second_layer}-{third_layer}",
                                                    "text": str(final_layer)}
                                            jstree.append(item)
                                    # (---------------------------------------------------------------------------)
                                    third_layer += 1
                                    item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                            "parent": f"json{first_layer}-{second_layer}", "text": str(value),
                                            "state": {"opened": 'true'}}
                                    jstree.append(item)
                            elif type(data[n][n1]) == list:
                                for url in data[n][n1]:
                                    third_layer += 1
                                    item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                            "parent": f"json{first_layer}-{second_layer}", "text": str(url),
                                            "state": {"opened": 'true'}}
                                    jstree.append(item)
                            else:
                                if data[n][n1] == dict:
                                    for value in data[n][n1]:
                                        third_layer += 1
                                        item = {"id": f"json{first_layer}-{second_layer}-{third_layer}-{four_layer}",
                                                "parent": f"json{first_layer}-{second_layer}-{third_layer}",
                                                "text": str(token_param),
                                                "state": {"opened": 'true'}}
                                        jstree.append(item)
                                elif data[n][n1] == list:
                                    for token_param in data[n][n1]:
                                        third_layer += 1
                                        item = {"id": f"json{first_layer}-{second_layer}-{third_layer}-{four_layer}",
                                                "parent": f"json{first_layer}-{second_layer}-{third_layer}",
                                                "text": str(token_param)}
                                        jstree.append(item)
                                third_layer += 1
                                item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                        "parent": f"json{first_layer}-{second_layer}", "text": str(data[n][n1]),
                                        "state": {"opened": 'true'}}
                                jstree.append(item)
                    elif n == 'except':
                        second_layer += 1
                        item = {"id": f"json{first_layer}-{second_layer}",
                                "parent": f"json{first_layer}", "text": str(n), "state": {"opened": 'true'}}
                        jstree.append(item)
                        for i, except_item in enumerate(data[n]):
                            third_layer += 1
                            item1 = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                     "parent": f"json{first_layer}-{second_layer}", "text": str(data[n][i]['Response'])}
                            third_layer += 1
                            item2 = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                     "parent": f"json{first_layer}-{second_layer}", "text": str(data[n][i]['code'])}
                            jstree.append(item1)
                            jstree.append(item2)
                return jstree
        elif casetype == 'Web':
            casetype = 'web'
            with open(f"Vip_Ram_Folder/{account}/{casetype}/{CaseNumber}/{yamlname}") as f:
                data = yaml.safe_load(f)
                jstree = []
                first_layer = 0
                second_layer = 0
                third_layer = 0
                four_layer = 0

                for layer1_index, layer1 in enumerate(data):
                    first_layer += 1
                    item = {"id": f"json{first_layer}", "parent": "#", "text": layer1,
                            "a_attr": {"style": "color : red"}, "state": {"opened": "true"}}
                    jstree.append(item)
                    for i, layer2 in enumerate(list(data[layer1].keys())):
                        second_layer += 1
                        item = {"id": f"json{first_layer}-{second_layer}", "parent": f"json{first_layer}",
                                "text": layer2,
                                "state": {"opened": 'true'}}
                        jstree.append(item)
                        if type(data[layer1][layer2]) == dict:
                            for index, layer3 in enumerate(list(data[layer1][layer2].keys())):
                                third_layer += 1
                                item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                        "parent": f"json{first_layer}-{second_layer}",
                                        "text": list(data[layer1][layer2].values())[index], "state": {"opened": 'true'}}
                                jstree.append(item)
                        else:
                            third_layer += 1
                            item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                    "parent": f"json{first_layer}-{second_layer}", "text": data[layer1][layer2],
                                    "state": {"opened": 'true'}}
                            jstree.append(item)
            return jstree

    def Process_yaml_api(casetype, system, yamlname, *args):
        jstree = []
        first_layer = 0
        second_layer = 0
        third_layer = 0
        four_layer = 0
        if not args:
            with open(f"./TestCase_ver1.0/{casetype}/{system}/{yamlname}") as f:
                data = yaml.safe_load(f)
                for n in data:
                    if n == 'Environment':
                        first_layer += 1
                        item = {"id": f"json{first_layer}", "parent": "#", "text": n,
                                "a_attr": {"style": "color : red"}, "state": {"opened": 'true'}}
                        jstree.append(item)
                        for key in data[n]:
                            if type(data[n][key]) == list:
                                for list_item in data[n][key]:
                                    second_layer += 1
                                    item = {"id": f"json{first_layer}-{second_layer}", "parent": f"json{first_layer}",
                                            "text": list_item, "state": {"opened": 'true'}}
                                    jstree.append(item)
                            elif type(data[n][key]) == dict:
                                for dict_key in data[n][key]:
                                    second_layer += 1
                                    item = {"id": f"json{first_layer}-{second_layer}", "parent": f"json{first_layer}",
                                            "text": dict_key, "state": {"opened": 'true'}}
                                    jstree.append(item)
                                    if type(data[n][key][dict_key]) == list:
                                        for list_item_second in data[n][key][dict_key]:
                                            third_layer += 1
                                            item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                                    "parent": f"json{first_layer}-{second_layer}",
                                                    "text": list_item_second, "state": {"opened": 'true'}}
                                            jstree.append(item)
                                    elif type(data[n][key][dict_key]) == dict:
                                        for dict_item_second in data[n][key][dict_key]:
                                            third_layer += 1
                                            item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                                    "parent": f"json{first_layer}-{second_layer}",
                                                    "text": data[n][key][dict_key][dict_item_second],
                                                    "state": {"opened": 'true'}}
                                            jstree.append(item)
                                    else:
                                        third_layer += 1
                                        item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                                "parent": f"json{first_layer}-{second_layer}",
                                                "text": data[n][key][dict_key],
                                                "state": {"opened": 'true'}}
                                        jstree.append(item)
                            else:
                                second_layer += 1
                                item = {"id": f"json{first_layer}-{second_layer}", "parent": f"json{first_layer}",
                                        "text": key, "state": {"opened": 'true'}}
                                jstree.append(item)
                                # (-----------------------------------------------)
                                third_layer += 1
                                item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                        "parent": f"json{first_layer}-{second_layer}",
                                        "text": data[n][key], "state": {"opened": 'true'}}
                                jstree.append(item)
                    elif n == "APIcommand" or n == "Configure":
                        first_layer += 1
                        item = {"id": f"json{first_layer}", "parent": "#", "text": n, "state": {"opened": 'true'}}
                        jstree.append(item)
                        for i, n1 in enumerate(data[n]):
                            # if n != 'except':
                            second_layer += 1
                            item = {"id": f"json{first_layer}-{second_layer}", "parent": f"json{first_layer}",
                                    "text": str(n1), "state": {"opened": 'true'}}
                            jstree.append(item)
                            if type(data[n][n1]) == dict:
                                for index, value in enumerate(data[n][n1]):
                                    if type(data[n][n1][value]) == list:
                                        for final_layer in data[n][n1][value]:
                                            four_layer += 1
                                            item = {
                                                "id": f"json{first_layer}-{second_layer}-{third_layer}-{four_layer}",
                                                "parent": f"json{first_layer}-{second_layer}-{third_layer}",
                                                "text": str(final_layer)}
                                            jstree.append(item)
                                    # (---------------------------------------------------------------------------)
                                    third_layer += 1
                                    item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                            "parent": f"json{first_layer}-{second_layer}", "text": str(value),
                                            "state": {"opened": 'true'}}
                                    jstree.append(item)
                            elif type(data[n][n1]) == list:
                                for url in data[n][n1]:
                                    third_layer += 1
                                    item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                            "parent": f"json{first_layer}-{second_layer}", "text": str(url),
                                            "state": {"opened": 'true'}}
                                    jstree.append(item)
                            else:
                                if data[n][n1] == dict:
                                    for value in data[n][n1]:
                                        third_layer += 1
                                        item = {"id": f"json{first_layer}-{second_layer}-{third_layer}-{four_layer}",
                                                "parent": f"json{first_layer}-{second_layer}-{third_layer}",
                                                "text": str(token_param),
                                                "state": {"opened": 'true'}}
                                        jstree.append(item)
                                elif data[n][n1] == list:
                                    for token_param in data[n][n1]:
                                        third_layer += 1
                                        item = {"id": f"json{first_layer}-{second_layer}-{third_layer}-{four_layer}",
                                                "parent": f"json{first_layer}-{second_layer}-{third_layer}",
                                                "text": str(token_param)}
                                        jstree.append(item)
                                third_layer += 1
                                item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                        "parent": f"json{first_layer}-{second_layer}", "text": str(data[n][n1]),
                                        "state": {"opened": 'true'}}
                                jstree.append(item)
                    elif n == 'except':
                        second_layer += 1
                        item = {"id": f"json{first_layer}-{second_layer}",
                                "parent": f"json{first_layer}", "text": str(n), "state": {"opened": 'true'}}
                        jstree.append(item)
                        for i, except_item in enumerate(data[n]):
                            third_layer += 1
                            item1 = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                     "parent": f"json{first_layer}-{second_layer}", "text": str(data[n][i]['Response'])}
                            third_layer += 1
                            item2 = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                     "parent": f"json{first_layer}-{second_layer}", "text": str(data[n][i]['code'])}
                            jstree.append(item1)
                            jstree.append(item2)
                return jstree
        else:
            with open(f"Server_history_files/{yamlname}") as f:
                data = yaml.safe_load(f)
                for n in data:
                    if n == 'Environment':
                        first_layer += 1
                        item = {"id": f"json{first_layer}", "parent": "#", "text": n, "state": {"opened": 'true'}}
                        jstree.append(item)
                        for key in data[n]:
                            if type(data[n][key]) == list:
                                for list_item in data[n][key]:
                                    second_layer += 1
                                    item = {"id": f"json{first_layer}-{second_layer}", "parent": f"json{first_layer}",
                                            "text": list_item, "state": {"opened": 'true'}}
                                    jstree.append(item)
                            elif type(data[n][key]) == dict:
                                for dict_key in data[n][key]:
                                    second_layer += 1
                                    item = {"id": f"json{first_layer}-{second_layer}", "parent": f"json{first_layer}",
                                            "text": dict_key, "state": {"opened": 'true'}}
                                    jstree.append(item)
                                    if type(data[n][key][dict_key]) == list:
                                        for list_item_second in data[n][key][dict_key]:
                                            third_layer += 1
                                            item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                                    "parent": f"json{first_layer}-{second_layer}",
                                                    "text": list_item_second, "state": {"opened": 'true'}}
                                            jstree.append(item)
                                    elif type(data[n][key][dict_key]) == dict:
                                        for dict_item_second in data[n][key][dict_key]:
                                            third_layer += 1
                                            item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                                    "parent": f"json{first_layer}-{second_layer}",
                                                    "text": data[n][key][dict_key][dict_item_second],
                                                    "state": {"opened": 'true'}}
                                            jstree.append(item)
                                    else:
                                        third_layer += 1
                                        item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                                "parent": f"json{first_layer}-{second_layer}",
                                                "text": data[n][key][dict_key],
                                                "state": {"opened": 'true'}}
                                        jstree.append(item)
                            else:
                                second_layer += 1
                                item = {"id": f"json{first_layer}-{second_layer}", "parent": f"json{first_layer}",
                                        "text": key, "state": {"opened": 'true'}}
                                jstree.append(item)
                                # (-----------------------------------------------)
                                third_layer += 1
                                item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                        "parent": f"json{first_layer}-{second_layer}",
                                        "text": data[n][key], "state": {"opened": 'true'}}
                                jstree.append(item)
                    elif n == "APIcommand" or n == "Configure":
                        first_layer += 1
                        item = {"id": f"json{first_layer}", "parent": "#", "text": n, "state": {"opened": 'true'}}
                        jstree.append(item)
                        for i, n1 in enumerate(data[n]):
                            # if n != 'except':
                            second_layer += 1
                            item = {"id": f"json{first_layer}-{second_layer}", "parent": f"json{first_layer}",
                                    "text": str(n1), "state": {"opened": 'true'}}
                            jstree.append(item)
                            if type(data[n][n1]) == dict:
                                for index, value in enumerate(data[n][n1]):
                                    if type(data[n][n1][value]) == list:
                                        for final_layer in data[n][n1][value]:
                                            four_layer += 1
                                            item = {
                                                "id": f"json{first_layer}-{second_layer}-{third_layer}-{four_layer}",
                                                "parent": f"json{first_layer}-{second_layer}-{third_layer}",
                                                "text": str(final_layer)}
                                            jstree.append(item)
                                    # (---------------------------------------------------------------------------)
                                    third_layer += 1
                                    item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                            "parent": f"json{first_layer}-{second_layer}", "text": str(value),
                                            "state": {"opened": 'true'}}
                                    jstree.append(item)
                            elif type(data[n][n1]) == list:
                                for url in data[n][n1]:
                                    third_layer += 1
                                    item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                            "parent": f"json{first_layer}-{second_layer}", "text": str(url),
                                            "state": {"opened": 'true'}}
                                    jstree.append(item)
                            else:
                                if data[n][n1] == dict:
                                    for value in data[n][n1]:
                                        third_layer += 1
                                        item = {"id": f"json{first_layer}-{second_layer}-{third_layer}-{four_layer}",
                                                "parent": f"json{first_layer}-{second_layer}-{third_layer}",
                                                "text": str(token_param),
                                                "state": {"opened": 'true'}}
                                        jstree.append(item)
                                elif data[n][n1] == list:
                                    for token_param in data[n][n1]:
                                        third_layer += 1
                                        item = {"id": f"json{first_layer}-{second_layer}-{third_layer}-{four_layer}",
                                                "parent": f"json{first_layer}-{second_layer}-{third_layer}",
                                                "text": str(token_param)}
                                        jstree.append(item)
                                third_layer += 1
                                item = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                        "parent": f"json{first_layer}-{second_layer}", "text": str(data[n][n1]),
                                        "state": {"opened": 'true'}}
                                jstree.append(item)
                    elif n == 'except':
                        second_layer += 1
                        item = {"id": f"json{first_layer}-{second_layer}",
                                "parent": f"json{first_layer}", "text": str(n), "state": {"opened": 'true'}}
                        jstree.append(item)
                        for i, except_item in enumerate(data[n]):
                            third_layer += 1
                            item1 = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                     "parent": f"json{first_layer}-{second_layer}", "text": str(data[n][i]['Response'])}
                            third_layer += 1
                            item2 = {"id": f"json{first_layer}-{second_layer}-{third_layer}",
                                     "parent": f"json{first_layer}-{second_layer}", "text": str(data[n][i]['code'])}
                            jstree.append(item1)
                            jstree.append(item2)
                return jstree