data_dict = [{'x': '10', 'y': '20', 'z': '30'}, {'p': '40', 'q': '50', 'r': '60'}]

result = [{k:int(v)} for i in data_dict for k,v in i.items()]

print(result)

