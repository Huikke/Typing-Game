import os

# Take list and save it as csv to file
# Doesn't overwrite files
def save_score(stats_list):
    base_name = "score"
    extension = "csv"
    i = 1
    while os.path.exists(f"{base_name}_{i}.{extension}"):
        i += 1

    with open(f"{base_name}_{i}.{extension}", "w") as file:
        file.write(",".join(map(str, stats_list)))