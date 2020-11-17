def Filter_degree(df):
    degree_level = []
    for val in df.degree:
        try:
            if val.find("bachelor") > -1:
                degree_level.append('bachelor')
            elif val.find('master') > -1:
                degree_level.append('master')
            elif val.find('doctor') > -1:
                degree_level.append('phd')
            elif val.find('associate') > -1:
                degree_level.append('bachelor')
            else:
                degree_level.append(val)
        except:
            degree_level.append("None")
    remove_words = ['bachelors', 'of', 'masters', 'master', 'bachelor', 'doctor', 'associates', 'associate', 'ates']
    filtered = []
    for val in df.degree:
        try:
            for x in remove_words:
                val = val.replace(x, "")
            val = val.strip()
            if val == "":
                filtered.append("None")
            else:
                filtered.append(val)
        except:
            filtered.append("None")

    return degree_level, filtered


def Filter_streams(filtered):
    mapping_stream_degree = {
        "engineering": ["engineering", "mechanical", "software", "aerospace", "technology"],
        "management": ["management", "administration", "international studies", "business"],
        "law": ["law", "jurisprudence"],
        "medicine and surgery": ["optometry", "surgery", "veterinary", "medicine", "dentistry"],
        "miscellaneous": ["interdisciplinary", "divinity"],
        "paramedical": ["therapy", "chiropractic", "nursing", "communication disorders", "anesthesia", "pharmacy"],
        "public administration": ["public administration", "urban and regional planning"],
        "science": ["science", "library & information studies", "public health", "natural resources",
                    "veterinary science", "information systems", "computer science", "applied math", "math",
                    "psychology", ],
        "social work": ["social work"],
        "arts": ["arts", "teaching", "fine arts", "music", "philosophy"],
        "commerce": ["commerce", "accounting"],
        "design": ["design", "architecture"],
        "education": ["education"],
    }
    stream_filtered = []
    unsettled_streams = []
    for val in filtered:
        stream_ = "None"
        for stream_cluster in mapping_stream_degree.keys():
            for stream_granular in mapping_stream_degree[stream_cluster]:
                if (val.find(stream_granular) > -1):
                    stream_ = stream_cluster
                    break
        stream_filtered.append(stream_)
        if (stream_ == "None"):
            unsettled_streams.append(val)
    return stream_filtered, unsettled_streams


def find_closest(input_vector, vectors):
    index_max = vectors[0][0]
    value_max = 0
    for pair in vectors:
        calc_value = np.dot(pair[0], input_vector)
        if (calc_value > value_max):
            index_max = pair[1]
            value_max = calc_value
    return index_max

def baseline_model():
    model = Sequential()
    model.add(Dense(100, input_dim=300, activation='relu'))
    # model.add(Dense(100, activation='relu'))
    model.add(Dense(len(unique_sectors), activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

def clean_string(string):
    string = string.replace("&", "")
    string = string.replace("/", " ")
    return string

def joinStrings(stringList):
    answer = ''.join(string + " " for string in stringList)
    return answer.strip()
