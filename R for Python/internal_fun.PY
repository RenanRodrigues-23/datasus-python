# Convert dummy columns [0, 1] to factor ["Sim", "Não"]
def convert_dummy_to_sim_nao(data, column_names):
    for col in column_names:
        if col in data.columns:
            data[col] = data[col].replace({1: "Sim", 0: "Não"})
            # Alternatively, for handling missing values:
            # data[col] = data[col].map({1: "Sim", 0: "Não", None: None})
    return data


# Convert columns to integer
def convert_to_integer(data, column_names):
    for col in column_names:
        if col in data.columns:
            data[col] = data[col].astype(int)
    return data


# Convert columns to numeric
def convert_to_numeric(data, column_names):
    for col in column_names:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce')
    return data


# Convert columns to character
def convert_to_character(data, column_names):
    for col in column_names:
        if col in data.columns:
            data[col] = data[col].astype(str)
    return data
