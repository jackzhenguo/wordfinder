import json
import os


def combine_json_to_txt(filepath, save_file_name):
    texts = ""
    # file is a generated file
    for file in os.listdir(filepath):
        with open(filepath + '/' + file, encoding='utf-8') as f:
            # each line in the file is a wiki page
            for line in f:
                # read the line as valid json and select text field
                text = json.loads(line)['text']
                texts += text + '\n'

    with open(save_file_name, mode='w') as wf:
        wf.write(texts)
        print('writing done')


if __name__ == "__main__":
    combine_json_to_txt('/home/zglg/SLU/psd/corpus/english/enwiki', '/home/zglg/SLU/psd/corpus/english/wiki_en.txt')