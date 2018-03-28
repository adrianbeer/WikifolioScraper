import configparser
import os

Quarry = namedtuple('Quarry', ['title', 'amount', 'class_name', 'link'])

class ConfigParser():

    def __init__():
        self.default_quarry = os.path.join(os.path.dirname(__file__), '..', 'config', 'quarries.ini') 
        self.default_sysconfig = os.path.join(os.path.dirname(__file__), '..', 'config', 'sysconfig.ini')  

    def read_quarries(config=self.default_quarry):
        quarries = []
        parser = configparser.ConfigParser()
        parser.read(config)
        for key in parser['Quarries']:
            args = [key]
            args.extend(parser['Quarries'][key].split(' '))
            quarry = Quarry(
                    title=args[0], 
                    amount=int(args[1]), 
                    class_name=args[2],
                    link = args[3],
            )
            quarries.append(quarry)
        return quarries

    def read_sysconfig(config=self.default_sysconfig):
        parser = configparser.ConfigParser()
        parser.read(config)
        return parser['butterknife']
    
            


    
