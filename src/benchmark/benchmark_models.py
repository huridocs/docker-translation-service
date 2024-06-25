import pandas as pd
from shutil import rmtree
from os.path import join
from huggingface_hub import hf_hub_download


def download_data():
    repo_id = "Helsinki-NLP/opus-100"
    train_file_name = "train-00000-of-00001.parquet"
    language_pairs = ["ar-en", "en-es", "en-fr", "en-ru"]
    for pair in language_pairs:
        file_name = join(pair, train_file_name)
        hf_hub_download(repo_id=repo_id, filename=file_name, local_dir="./data", repo_type="dataset")
    rmtree("./data/.huggingface")


def read_parquet(parquet_file_path: str):
    df = pd.read_parquet(parquet_file_path, engine='pyarrow')
    lang1, lang2 = df.iloc[0]['translation'].keys()
    for i in range(5):
        print(f"Source:\n{df.iloc[i]['translation'][lang1]}\nTranslation:\n{df.iloc[i]['translation'][lang2]}\n")


if __name__ == '__main__':
    download_data()
    read_parquet("data/en-es")
