dictionary={'hate': [['hate','love'], ['hate']], 'live': [[]], 'anger': [['hate']], 'love': [['love']]}
for k,v in dictionary.items():
    new_val=[]
    for value in v:
        new_val=new_val+value
        dictionary[k]=new_val

print(dictionary)

unique_items = set(x for y in dictionary.values() for x in y)
print(unique_items)
dict_count_track={}
for item in unique_items:
    dict_count_track[item] = {k: v.count(item) for k, v in dictionary.items()}

print(dict_count_track)

count_track={}
for key,value in dict_count_track.items():  
    print(key," ", sum(value.values()))
    count_track.update({key:sum(value.values())})

print(count_track)

max_value = max(count_track.values()) 
print(max_value)