import json

with open('./technology_fields.json', 'r') as f:
    fields = json.load(f)
with open('./key_technologies.json', 'r') as f:
    techs = json.load(f)

results = []

for field in fields:
    results.append({
        "label": field["label"],
        "short": field["short"],
        "style": field["style"],
        "technologies": []
    })

for tech in techs:
    field = next(field for field in fields if field["_id"]["$oid"] == tech["field"])
    obj = next(result for result in results if field["label"] == result["label"])

    obj["technologies"].append({
        "label": tech["label"],
        "short": tech["short"],
    })

with open('./tech.json', 'w') as f:
    json.dump(results, f)