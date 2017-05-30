import copy
import json
import random
import sys

filename = sys.argv[1]

target_ndd_count = int(sys.argv[2])

with open(filename) as f:
    instance = json.load(f)["data"]

max_donor_id = max(int(donor_id) for donor_id in instance)
#print [int(donor_id) for donor_id in instance]
#print "Max donor ID:", max_donor_id

ndds = [(key, instance[key])
            for key in instance
            if "altruistic" in instance[key] and instance[key]["altruistic"]]

#print ndds[0]

recips = set()

for ndd in ndds:
    recips.update(match["recipient"] for match in ndd[1]["matches"])

ndds.sort(key=lambda ndd: len(ndd[1]["matches"]))

recip_count = {}
for ndd in ndds:
    for match in ndd[1]["matches"]:
        recip = match["recipient"]
        if recip in recip_count:
            recip_count[recip] += 1
        else:
            recip_count[recip] = 1

recips = sorted(list(recips), key=lambda recip: recip_count[recip])
recip_to_index = {r: i for (i, r) in enumerate(recips)}
index_to_recip = {i: r for (i, r) in enumerate(recips)}
#print recip_to_index
#print recips

#for ndd in ndds:
#    has_recip = [False] * len(recips)
#    for match in ndd[1]["matches"]:
#        has_recip[recip_to_index[match["recipient"]]] = True
#    print "".join("1" if x else "." for x in has_recip)

if len(ndds) > target_ndd_count:
    while len(ndds) > target_ndd_count:
        ndd_to_remove = random.choice(ndds)
        ndds.remove(ndd_to_remove)
        del instance[ndd_to_remove[0]]
elif len(ndds) < target_ndd_count:
    num_ndds = len(ndds)
    while num_ndds < target_ndd_count:
        cloned_ndd = copy.deepcopy(random.choice(ndds)[1])
        cloned_ndd["dage"] = cloned_ndd["dage"] + random.randint(-10, 10)
        for match in cloned_ndd["matches"]:
            match["score"] = int(match["score"] * (random.random()+0.5))
        max_donor_id += 1
        instance[max_donor_id] = cloned_ndd
        num_ndds += 1

print json.dumps({"data": instance}, sort_keys=True, indent=2)
