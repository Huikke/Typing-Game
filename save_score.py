# Take list and save it as csv to file
# Doesn't overwrite files
def save_score(stats_list):
    with open(f"score_history.csv", "a") as file:
        file.write(",".join(map(str, stats_list)) + "\n")