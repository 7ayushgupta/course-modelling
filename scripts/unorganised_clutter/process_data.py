from functions_for_processData import Filter_degree, find_closest, Filter_streams, baseline_model, joinStrings, clean_string
import pandas as pd
!pip install unidecode
import numpy as np
import matplotlib.pyplot as plt

%cd "/content/drive/My Drive/Revamp/Data/"

import spacy
!python -m spacy download en_core_web_lg
nlp = spacy.load('en_core_web_lg')

def processData(df):
    unique_degrees = df.degree.unique()

    degree_level, filtered = Filter_degree(df)
    stream_filtered, unsettled_streams = Filter_streams(filtered)

    df['stream_processed'] = stream_filtered
    df['degree_processed'] = degree_level
#######################################################################################################################
    majors_classification_df = pd.read_csv("College_Majors_Classification.csv")
    print(majors_classification_df.shape)
    majors_classification_df = majors_classification_df.dropna()
    majors_classification_df = majors_classification_df.applymap(lambda s: s.lower().strip())
    majors_mapping = {}
    idx_majors_mapping = {}
    for major in majors_classification_df.Major_Category.unique():
        majors_mapping.update({major: []})
    for index, row in majors_classification_df.iterrows():
        majors_mapping[row['Major_Category']].append(row['Major'])
        idx_majors_mapping.update({row['Major']: row['Major_Category']})
    df['major'] = df['major'].fillna('None')

#######################################################################################################################
    unsettled_titles = []
    settled_titles = []

    known_majors_vectors = []
    for key, item in idx_majors_mapping.items():
        nlp_token = nlp(key)
        if (nlp_token.vector_norm):
            known_majors_vectors.append((nlp_token.vector, item))

    created_mapping = {}

    for val in df.major.unique():
        nlp_token = nlp(val)
        if not nlp_token.vector_norm:
            unsettled_titles.append(val)
            continue
        closest_major = find_closest(nlp_token.vector, known_majors_vectors)
        created_mapping.update({val: closest_major})

    prettify_create_mapping = {}
    for major in majors_classification_df.Major_Category.unique():
        prettify_create_mapping.update({major: []})

    for key, val in created_mapping.items():
        prettify_create_mapping[val].append(key)

    # pd.DataFrame.from_dict(prettify_create_mapping, orient='index').to_csv('majors_mapping.csv')
#######################################################################################################################
    r = pd.read_csv('majors_mapping.csv')
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
    majors_mapping = prettify_create_mapping
#######################################################################################################################
    majors_processed = []

    for major_raw in df.major:
        major_ = "None"
        if major_raw == "None":
            majors_processed.append("None")
            continue
        for major_group, val in majors_mapping.items():
            if major_raw in val:
                major_ = major_group
                break
        majors_processed.append(major_)

    df['majors_processed'] = majors_processed
#######################################################################################################################

    a = pd.read_csv("industries_classification.csv")
    a = a.drop(["Sector", "Industry Group", "Industry", "Sub-Industry"], axis=1)
    a = a.rename({"Unnamed: 1": "Sector", "Unnamed: 3": "Industry Group", "Unnamed: 5": "Industry",
                  "Unnamed: 7": "Sub-Industry"}, axis=1)
    a = a.dropna(how='all')
    a = a.fillna("None")

    SP_classification = []
    column_used = "Industry Group"
    sector = a.iloc[0][column_used]
    for index, row in a.iterrows():
        subindustry = row['Sub-Industry']
        if (row[column_used] != "None"):
            sector = row[column_used]
        SP_classification.append([sector, subindustry])

    for tuple_ in SP_classification:
        if tuple_[0] == "(cont’d)":
            tuple_[0] = "Consumer Discretionary"
        if tuple_[0] == "Discretionary":
            tuple_[0] = "Consumer Discretionary"
        if tuple_[0] == "Consumer":
            tuple_[0] = "Consumer Discretionary"

        tuple_[0] = tuple_[0].replace(" (cont’d)", "")
        tuple_[0] = tuple_[0].replace("\n", " ")
        tuple_[0] = tuple_[0].split(" (")[0]
        tuple_[1] = tuple_[1].replace("\n", " ")
        tuple_[1] = tuple_[1].replace(" & ", " and ")
        tuple_[1] = tuple_[1].split(" -- ")[0]
        tuple_[1] = tuple_[1].split("(")[0]
        tuple_[1] = tuple_[1].replace("REITs", "Real Estate Investment Trusts")
        tuple_[1] = tuple_[1].replace("-", " ")
#######################################################################################################################
    sectors = []
    for tuple_ in SP_classification:
        sectors.append(tuple_[0])
    unique_sectors = np.unique(sectors)

    sector_mapping = {}
    for i, sector in enumerate(unique_sectors):
        sector_mapping.update({sector: i + 1})
#######################################################################################################################
    SP_vectors = []
    for tuple_ in SP_classification:
        idx = sector_mapping[tuple_[0]]
        SP_vectors.append(np.append(nlp(tuple_[1]).vector, idx))
#######################################################################################################################
    data = pd.DataFrame(SP_vectors)
    X = data.loc[:, :299]
    y = data.loc[:, 300]
    from sklearn.preprocessing import LabelEncoder
    from keras.utils import np_utils
    encoder = LabelEncoder()
    encoder.fit(y)
    encoded_Y = encoder.transform(y)
    dummy_y = np_utils.to_categorical(encoded_Y, num_classes=len(unique_sectors))
    data.head()

    from keras.wrappers.scikit_learn import KerasClassifier
    estimator = KerasClassifier(build_fn=baseline_model, epochs=200, batch_size=5, verbose=0)
    from keras.models import Sequential
    from sklearn.model_selection import train_test_split
    from keras.layers import Dense
    data = np.concatenate([X, dummy_y], axis=1)
    X_train, X_test, y_train, y_test = train_test_split(data[:, :300], data[:, 300:], test_size=0.33, random_state=42)
    estimator.fit(X_train, y_train)
    y_pred = estimator.predict(X_test)
    y_pred = np_utils.to_categorical(y_pred, num_classes=len(unique_sectors))
    print(X_train.shape, X_test.shape, y_train.shape, y_test.shape, y_pred.shape)
########################################################################################################################

    from sklearn.metrics import classification_report
    df['industry'] = df['industry'].fillna('None')
    vectors_unique = []
    words_unique = []
    industries_unique = df.industry.unique()
    industries_filtered = []
    for val in industries_unique:
        val = val.replace("&", "")
        val = val.replace("/", " ")
        if val != "None" and val.find(':') == -1 and val.find("]"):
            industries_filtered.append(val)

    for val in industries_filtered:
        nlp_token = nlp(val)
        if (nlp_token.has_vector):
            vectors_unique.append(nlp_token.vector)
            words_unique.append(val)
    vectors_unique = np.array(vectors_unique)
    y_pred = estimator.predict(vectors_unique)

    predicted_sectors = {}

    for key, value in sector_mapping.items():
        predicted_sectors[key] = []

    for a, b in zip(words_unique, y_pred):
        predicted_sectors[unique_sectors[b]].append(a)
    # pd.DataFrame.from_dict(predicted_sectors, orient='index').to_csv("/content/predicted_industries_classification.csv")
########################################################################################################################
    industry_processed = []

    for industry_raw in df.industry:
        industry_ = "None"
        industry_raw = clean_string(industry_raw)
        for key, value in predicted_sectors.items():
            if industry_raw in value:
                industry_ = key
                break
        if (industry_ == "None" and industry_raw != "None"):
            print(industry_raw)
        industry_processed.append(industry_)

    df['industry_processed'] = industry_processed
########################################################################################################################
    workers_classification = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/e/2PACX-1vSXxWGKiCFw6QRXV09znbdHmd5HqCGgzl8o8qGndrft2U9I9fyNz94rblr69YLQkqhDiTkGrwGH6M4R/pub?gid=2085110439&single=true&output=csv')
    workers_classification.columns = ['none', 'level', 'title']
    workers_classification = workers_classification.drop(['none'], axis=1)
    workers_classification = workers_classification.fillna(method='ffill')
    workers_classification = workers_classification.applymap(lambda s: s.lower().strip())
    workers_mapping = {}
    for x in workers_classification.level.unique():
        workers_mapping[x] = []
    for index, row in workers_classification.iterrows():
        workers_mapping[row['level']].append((row['title']).lower())
    levels = list(workers_mapping.keys())
    data = []
    counter = 0
    for level, titles in workers_mapping.items():
        for title in titles:
            if nlp(title).has_vector:
                data.append(np.append(nlp(title).vector, counter))
        counter += 1
    data = pd.DataFrame(data)

    workers_mapping = {}
    for x in workers_classification.level.unique():
        workers_mapping[x] = []
    for index, row in workers_classification.iterrows():
        workers_mapping[row['level']].append((row['title']).lower())
    idx_workers_mapping = {}
    idx_vectors_mapping = {}

    for key, value in workers_mapping.items():
        for item in value:
            idx_workers_mapping[item] = key
            idx_vectors_mapping[item] = (nlp(item))
########################################################################################################################
    import re
    from tqdm import tqdm_notebook

    switches = {
        "sr": "senior",
        "asst": "assistant",
        " & ": " ",
        "-": "",
        "engg": "engineer",
        "ceo": "chief executive officer",
        "cto": "chief technical officer",
        "@": " ",
        "dy": "deputy",
        "/": " ",
        '"': "",
    }

    levels_split = []
    unsettled_titles = []
    specialisation = []
    already_done_ = {}
    df = df.sort_values(by=['job_title'])
    df['job_title'] = df['job_title'].fillna('None')
    df['level_raw'] = df['level_raw'].fillna('None')

    for title_raw, level_raw in tqdm_notebook(zip(df.job_title, df.level_raw), total=len(df.job_title)):
        selected_word = ""
        if title_raw == "None" and level_raw == "None":
            level_ = "None"
        else:
            if title_raw == "None":
                level_ = level_raw
            else:
                try:
                    level_, selected_word = already_done_[(title_raw, level_raw)]
                except:
                    title = title_raw
                    for original, new in switches.items():
                        title = title.replace(original, new)
                        title = title.strip()

                    level_ = "None"
                    for level in ['tm', 'mm', 'lm', 'fm', 'worker', 'others']:
                        for level_granular in workers_mapping[level]:
                            if title.find(level_granular) > -1:
                                level_ = level
                                selected_word = level_granular
                                break
                        if selected_word != "":
                            break

                    title_token = nlp(title)
                    if level_ == "None" and title_token.vector_norm:
                        for level_granular, level in idx_workers_mapping.items():
                            token = idx_vectors_mapping[level_granular]
                            if token.vector_norm and title_token.similarity(token) > 0.9:
                                level_ = level
                                selected_word = level_granular
                                break

                    if level_ == "None" and title != "None":
                        unsettled_titles.append(title)
                        level_ = "undefined"

                    already_done_.update({(title_raw, level_raw): (level_, selected_word)})

        left_part = title_raw.replace(selected_word, "")
        if left_part == "":
            left_part = "None"

        levels_split.append(level_)
        specialisation.append(left_part)
        # print(title_raw,"|", level_raw,"|", level_, "|", left_part)
    # pd.DataFrame(unsettled_titles).to_csv('unsettled_titles.csv')

    print(len(levels_split))
    print(len(unsettled_titles))
    print(len(specialisation))
    df['levels_processed'] = levels_split
    df['specialisation'] = specialisation
########################################################################################################################
    # spec_classification = pd.read_csv("/content/drive/My Drive/Revamp/Data/specialisations_classification.csv")
    spec_classification = pd.read_csv(
        'https://docs.google.com/spreadsheets/d/e/2PACX-1vSXxWGKiCFw6QRXV09znbdHmd5HqCGgzl8o8qGndrft2U9I9fyNz94rblr69YLQkqhDiTkGrwGH6M4R/pub?gid=0&single=true&output=csv')
    spec_classification.columns = ['specialisation', 'categories']
    spec_classification['specialisation'] = spec_classification['specialisation'].fillna(method='ffill')
    spec_classification = spec_classification.applymap(lambda s: s.lower().strip())
    spec_classification.head()

    specialisation_mapping = {}

    spec_classification = spec_classification.applymap(lambda s: s.lower() if type(s) == str else s)

    for spec in spec_classification['specialisation'].unique():
        specialisation_mapping[spec] = []

    for index, row in spec_classification.iterrows():
        specialisation_mapping[row['specialisation']].append(row['categories'])
    idx_specialisation_mapping = {}
    idx_tokens_mapping = {}
    idx_vectors_mapping = {}
    for key, value in specialisation_mapping.items():
        for item in value:
            idx_specialisation_mapping[item] = key
            idx_tokens_mapping[item] = nlp(item)
            idx_vectors_mapping[item] = idx_tokens_mapping[item].vector

    processed_specialisations = []
    specialiasation_cleaned = []
    granular_specialisations = []
    already_done_ = {}
    count = 0
    df['job_title'] = df['job_title'].fillna('None')
    choices = []
    for key, value in idx_specialisation_mapping.items():
        choices.append(key)

    from numpy import dot
    from numpy.linalg import norm

    def cos_sim(a, b):
        return dot(a, b) / (norm(a) * norm(b))

    from tqdm import tqdm_notebook
    # for specialisation_raw in tqdm_notebook(df.job_title.unique(), total=len(df.job_title.unique())):
    for specialisation_raw in tqdm_notebook(df.job_title, total=len(df.job_title)):
        count += 1
        # print(specialisation_raw)
        specialisation = specialisation_raw
        specialisation = specialisation.replace('"', "")
        specialisation = specialisation.replace("'", "")
        specialisation = specialisation.replace('-', " ")
        specialisation = specialisation.replace('*', " ")

        specialisation = specialisation.replace('(', "")
        specialisation = specialisation.replace('/', "")
        specialisation = specialisation.replace('|', "")
        specialisation = specialisation.replace('\\', "")
        specialisation = specialisation.replace(')', "")
        specialisation = specialisation.strip()

        if specialisation_raw == "None":
            processed_specialisation = "None"
            specialisation = "None"
            granular_specialisation = "None"

        else:
            if specialisation_raw in already_done_.keys():
                granular_specialisation = already_done_[specialisation_raw][0]
                processed_specialisation = already_done_[specialisation_raw][1]
            else:
                processed_specialisation = "undefined"
                granular_specialisation = "undefined"
                spec_vector = nlp(specialisation).vector
                best_token = "None"
                max_sim = 0
                max_len = 0
                for spec_ in idx_specialisation_mapping.keys():
                    if (len(spec_) > 7) and specialisation.find(spec_) > -1:
                        if len(spec_) > max_len:
                            best_token = spec_
                            max_len = max(max_len, len(best_token))
                    elif len(spec_) > 3 and specialisation.find(spec_) > -1:
                        if (cos_sim(spec_vector, idx_vectors_mapping[spec_]) > 0.5):
                            best_token = spec_
                            break
                        else:
                            # print("Close touch here ->", specialisation, "->", spec_, "-- failed")
                            pass

                if best_token == "None":
                    for spec_ in idx_specialisation_mapping.keys():
                        current_sim = cos_sim(spec_vector, idx_vectors_mapping[spec_])
                        if (current_sim > max_sim):
                            max_sim = current_sim
                            best_token = spec_

                # print(max_sim, best_token)
                if (max_sim < 0.50 and best_token == "None"):
                    processed_specialisation = "undefined"
                    granular_specialisation = "undefined"
                else:
                    processed_specialisation = idx_specialisation_mapping[best_token]
                    granular_specialisation = best_token

                already_done_.update({specialisation_raw: (granular_specialisation, processed_specialisation)})
                if (count % 1 == 0):
                    # print(specialisation, "|\t|", granular_specialisation, "|\t|", processed_specialisation, "|\t|", max_sim)
                    pass

        processed_specialisations.append(processed_specialisation)
        granular_specialisations.append(granular_specialisation)
        specialiasation_cleaned.append(specialisation)

    df['specialisations_processed'] = processed_specialisations
    df['granular_specialisations'] = granular_specialisations
    df['job_title_cleaned'] = specialiasation_cleaned

    level_classification = pd.read_csv(
        "https://docs.google.com/spreadsheets/d/e/2PACX-1vSXxWGKiCFw6QRXV09znbdHmd5HqCGgzl8o8qGndrft2U9I9fyNz94rblr69YLQkqhDiTkGrwGH6M4R/pub?gid=2085110439&single=true&output=csv")
    level_classification['Categories'] = level_classification['Categories'].fillna(method='ffill')
    level_classification = level_classification.applymap(lambda s: s.lower() if type(s) == str else s)
    level_classification = level_classification.drop('Levels', axis=1)
    level_classification.columns = ['level', 'granular_specialisation']
    level_mapping = {}
    for index, row in level_classification.iterrows():
        level_mapping.update({row['granular_specialisation']: row['level']})
    print(level_mapping)
    levels_processed = []
    unsettled = []
    for spec in df.granular_specialisations:
        if spec == "None":
            levels_processed.append("None")
        elif spec in level_mapping.keys():
            levels_processed.append(level_mapping[(spec)])
        else:
            levels_processed.append("undefined")
            unsettled.append(spec)
    df['levels_processed'] = levels_processed
    # df.to_csv('features_created_.csv')
    return df