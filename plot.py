
class Plot:


    def __init__(self, path, foldername):
        if foldername[:5] == 'plot_':
            self.foldername = foldername
            self.path = path+'/'+foldername
        else:
            raise Error('foldername has to begin with \'plot\'')
        
    def load():
        pazss

    def plot():
        pass