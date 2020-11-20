import pandas as pd
import numpy as np

r = pd.read_csv('../static_data/predicted_specialisation.csv')
r = r.set_index('Unnamed: 0')
prettify_create_mapping = {}
for i in r.index:
    prettify_create_mapping[i] = []
    for enum, j in enumerate(r.columns):
        if enum == 1:
            continue
        val = r.loc[str(i), j]
        if not pd.isnull(val):
            prettify_create_mapping[i].append(val)
already_done_ = prettify_create_mapping

level_classification = pd.read_csv('../static_data/level_mapping.csv')
    level_classification['Categories'] = level_classification['Categories'].fillna(method='ffill')
    level_classification = level_classification.applymap(lambda s: s.lower() if type(s) == str else s)
    level_classification = level_classification.drop('Levels', axis=1)
    level_classification.columns = ['level', 'granular_specialisation']
    level_mapping = {}
    for index, row in level_classification.iterrows():
        level_mapping.update({row['granular_specialisation']: row['level']})

def buildLevel_Specialisation(specialisation_raw):
    if specialisation_raw == "None":
        processed_specialisation = "None"
        granular_specialisation = "None"

    elif specialisation_raw in already_done_.keys():
        granular_specialisation = already_done_[specialisation_raw][0]
        processed_specialisation = already_done_[specialisation_raw][1]

    # else:
    #     processed_specialisation = "undefined"
    #     granular_specialisation = "undefined"
    #     spec_vector = nlp(specialisation).vector
    #     best_token = "None"
    #     max_sim = 0
    #     max_len = 0
    #     for spec_ in idx_specialisation_mapping.keys():
    #         if (len(spec_) > 7) and specialisation.find(spec_) > -1:
    #             if len(spec_) > max_len:
    #                 best_token = spec_
    #                 max_len = max(max_len, len(best_token))
    #         elif len(spec_) > 3 and specialisation.find(spec_) > -1:
    #             if (cos_sim(spec_vector, idx_vectors_mapping[spec_]) > 0.5):
    #                 best_token = spec_
    #                 break
    #             else:
    #                 # print("Close touch here ->", specialisation, "->", spec_, "-- failed")
    #                 pass
    #
    #     if best_token == "None":
    #         for spec_ in idx_specialisation_mapping.keys():
    #             current_sim = cos_sim(spec_vector, idx_vectors_mapping[spec_])
    #             if (current_sim > max_sim):
    #                 max_sim = current_sim
    #                 best_token = spec_
    #
    #     # print(max_sim, best_token)
    #     if (max_sim < 0.50 and best_token == "None"):
    #         processed_specialisation = "undefined"
    #         granular_specialisation = "undefined"
    #     else:
    #         processed_specialisation = idx_specialisation_mapping[best_token]
    #         granular_specialisation = best_token

    if granular_specialisation == "None":
        levels_processed = "None"

    elif granular_specialisation in level_mapping.keys():
        levels_processed = level_mapping[(granular_specialisation)]
    else:
        levels_processed = "undefined"

    return processed_specialisation, levels_processed
