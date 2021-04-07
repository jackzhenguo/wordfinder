import json
import os


def combine_json_to_txt(filepath, save_file_name):
    def read(filepath2, file, wf):
        with open(filepath2 + '/' + file, encoding='utf-8') as f:
            # each line in the file is a wiki page
            for line in f:
                # read the line as valid json and select text field
                text = json.loads(line)['text']
                wf.write(text+"\n")

    if not os.path.exists(save_file_name):
        os.mknod(save_file_name)

    with open(save_file_name, mode='w') as wf:
        # file is a generated file
        for file in os.listdir(filepath):
            filepath2 = filepath + '/' + file
            if os.path.isdir(filepath2):
                # at most with 1 sub folder
                for jsonfile in os.listdir(filepath2):
                    read(filepath2, jsonfile, wf)
            else:
                read(filepath, file, wf)


if __name__ == "__main__":
    # convert corpus in json format of a specifid language to txt format together
    # because we have chinese and english, so only get other languages
    ls = ['fr', 'es', 'it', 'ko', 'pt', 'ru']
    for language in ls:
        combine_json_to_txt('input/corpus/%s' % (language,),
                            'input/corpus/result/wiki_%s.txt' % (language,))
