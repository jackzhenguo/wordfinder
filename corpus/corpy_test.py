from corpy.udpipe import Model
from corpy.udpipe import pprint


m = Model("/home/zglg/SLU/psd/pre-model/classical_chinese-kyoto-ud-2.5-191206.udpipe")

sents = list(m.process("我爱北京天安门. 天安门上好风景"))
pprint(sents)