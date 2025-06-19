# def load_data(filepath):
#     import pandas as pd
#     try:
#         data = pd.read_json(filepath)
#         return data
#     except ValueError as e:
#         print(f"Error loading data: {e}")
#         return None

# def get_sample_data():
#     return load_data('data/sample_maude.json')