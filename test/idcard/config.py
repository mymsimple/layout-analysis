from configparser import ConfigParser
CFG = ConfigParser()
CFG.read("config/config.cfg",encoding='utf-8')
print("配置文件：" ,CFG.sections())
#print(CFG.keys())