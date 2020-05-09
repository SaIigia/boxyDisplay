''' docstring here '''

import subprocess

class Screen(object):
    ''' '''
    # Definitions of drawing blocks
    blocks={
        # Lines: horizontal, vertical
        'linSml': [u'\u2500', u'\u2502'],
        'linBig': [u'\u2501', u'\u2503'],
        'linDbl': [u'\u2550', u'\u2551'],
        'linStrSml': [u'\u2504', u'\u2506'],
        'linStrBig': [u'\u2505', u'\u2507'],
        'linAux': ['-', '|'],

        # Angles: upL, upR, lowL, lowR
        'angSml': [u'\u250C', u'\u2510', u'\u2514', u'\u2518'],
        'angBig': [u'\u250F', u'\u2513', u'\u2517', u'\u251B'],
        'angDbl': [u'\u2554', u'\u2557', u'\u255A', u'\u255D'],
        'angAux': ['/', '\\', '\\', '/'],

        # Junctions: left, right, top, bottom, quad
        'junSml': [u'\u2524', u'\u251C', u'\u2534', u'\u252C', u'\u253C'],
        'junBig': [u'\u252B', u'\u2523', u'\u253B', u'\u2533', u'\u254B'],
        'junDbl': [u'\u2563', u'\u2560', u'\u2569', u'\u2566', u'\u256C'],
        'junAux': ['#', '#', '#', '#', '#']
    }

    def __init__(self, width, height, bType=None):
        '''Constructor'''
        if bType not in ['1', '2', '3']: bType='4'
        if bType=='1':
           self.__blocks=[Screen.blocks['linSml'], Screen.blocks['angSml'], Screen.blocks['junSml']]
        elif bType=='2':
            self.__blocks=[Screen.blocks['linBig'], Screen.blocks['angBig'], Screen.blocks['junBig']]
        elif bType=='3':
            self.__blocks=[Screen.blocks['linDbl'], Screen.blocks['angDbl'], Screen.blocks['junDbl']]
        elif bType=='4':
            self.__blocks=[Screen.blocks['linAux'], Screen.blocks['angAux'], Screen.blocks['junAux']]

        self.__blockset=bType
        self.__width=width
        self.__height=height
        self.__elements=[]
        self.__data=None
        self.__CreateScreen()


    @property
    def Size(self):
        return self.__width, self.__height
    @Size.setter
    def Size(self, newSize):
        try: width, height=newSize
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            assert all((width>=0, height>=0))
            self.__width, self.__height=width, height

    @property
    def Data(self):
        return self.__data
    @Data.setter
    def Data(self, newData):
        self.__data=newData

    @property
    def Blocks(self):
        return self.__blocks
    @Blocks.setter
    def Blocks(self, bType):
        if bType not in ['1', '2', '3']: bType='4'
        if bType=='1':
           newBlocks=[Screen.blocks['linSml'], Screen.blocks['angSml'], Screen.blocks['junSml']]
        elif bType=='2':
            newBlocks=[Screen.blocks['linBig'], Screen.blocks['angBig'], Screen.blocks['junBig']]
        elif bType=='3':
            newBlocks=[Screen.blocks['linDbl'], Screen.blocks['angDbl'], Screen.blocks['junDbl']]
        elif bType=='4':
            newBlocks=[Screen.blocks['linAux'], Screen.blocks['angAux'], Screen.blocks['junAux']]

        self.__blocks=newBlocks

    @property
    def Elements(self):
        return self.__elements

    @property
    def MaxWidth(self):
        return self.__width-1
    @property
    def MaxHeight(self):
        return self.__height-1


    def __CreateScreen(self):
        '''Create empty screen'''
        # Add screen frame top
        data=''+self.Blocks[1][0]+(self.Size[0]-2)*self.Blocks[0][0]+self.Blocks[1][1]+'\n'
        # Add screen frame sides and empty space
        for _ in range(self.__height-2):
            data+=self.Blocks[0][1]+(self.Size[0]-2)*' '+self.Blocks[0][1]+'\n'
        # Add screen frame bottom
        data+=self.Blocks[1][2]+(self.Size[0]-2)*self.Blocks[0][0]+self.Blocks[1][3]+'\n'

        self.__PushScreenData(data)

    def __FlushScreenData(self):
        '''Refresh screen data'''
        for item in self.Elements:
            try: item.__CreateScreen()
            except AttributeError: pass
        self.__CreateScreen()

    def __PushScreenData(self, data):
        '''Push data to be displayed on the screen'''
        assert(len(data)<=(self.Size[0]+1)*self.Size[1])
        if type(data)==str:self.__data=data
        else: self.__data=''.join(data)

    def UpdateScreenData(self, noFlush=False):
        '''Update data from elements tied to the screen'''
        if not noFlush: self.__FlushScreenData()
        for item in self.Elements:
            data=item.InsertScreenData(self.MaxWidth, self.MaxHeight, self.Data)
            if data: self.__PushScreenData(data)

    def DrawScreen(self):
        '''Draw screen data'''
        subprocess.run(['clear'])
        print(self.Data)


    def AddBox(self, width, height, xPos, yPos):
        '''Add a box to the screen '''
        # Make sure that box is in boudaries of printable screen space
        if (height+yPos)>= self.__height or (width+xPos)>=self.__width:
            raise ValueError('Not enough screen space')
        # Make sure that it's not on screen frame
        if xPos==0: xPos=1
        elif yPos==0: yPos=1
        self.Elements.append(ScreenBox(width, height, self.__blockset, xPos, yPos))
        return self.Elements[-1]

    def AddDividor(self, orient, xPos=None, yPos=None):
        '''Add dividing line on the screen '''
        self.Elements.append(Screen.Dividor(orient, self.Blocks, self.Size, xPos, yPos))
        return self.Elements[-1]

    def AddBanner(self, height, yPos):
        pass


    class Dividor(object):
        ''' '''
        def __init__(self, orient, sBlocks, sSize, xPos=None, yPos=None):
            '''Constructor'''
            try: sWidth, sHeight=sSize
            except ValueError:
                raise ValueError("Pass an iterable with two items")
            else: assert all((sWidth>0, sHeight>0))
            if orient=='hor' and yPos==None:
                raise ValueError('Horizontal dividor needs Y coordinate')
            elif orient=='ver' and xPos==None:
                raise ValueError('Vertical dividor needs X coordinate')
            if orient=='hor' and yPos:
                if yPos>sHeight-2 or yPos<=0:
                    raise ValueError('Vertical dividor outside of screen')

            self.__orient=orient
            self.__xPos=xPos
            self.__yPos=yPos
            self.__data=None
            self.__blocks=sBlocks
            self.__CreateDividor(sWidth, sHeight)

        def __CreateDividor(self, sWidth, sHeight):
            '''Create dividor string '''
            if self.__orient=='hor':
                self.Data=self.Blocks[2][1]+(sWidth-2)*self.Blocks[0][0]+self.Blocks[2][0]
            elif self.__orient=='ver':
                self.Data=self.Blocks[2][3]+(sHeight-2)*self.Blocks[0][1]+self.Blocks[2][2]
            else: raise ValueError('Only "hor" and "ver" are valid')


        @property
        def Data(self):
            return self.__data
        @Data.setter
        def Data(self, newData):
            if isinstance(newData, list): newData=''.join(newData)
            self.__data=newData

        @property
        def Position(self):
            return self.__xPos, self.__yPos
        @Position.setter
        def Position(self, newPos):
            try: newX, newY=newPos
            except ValueError:
                raise ValueError("Pass an iterable with two items")
            else:
                if self.__orient=='hor' and newY==None:
                    raise ValueError('Horizontal dividor needs Y coordinate')
                elif self.__orient=='ver' and newX==None:
                    raise ValueError('Vertical dividor needs X coordinate')
                self.__xPos, self.__yPos=newX, newY

        @property
        def Blocks(self):
            return self.__blocks
        @Blocks.setter
        def Blocks(self, bType):
            if bType not in ['1', '2', '3']: bType='4'
            if bType=='1':
                newBlocks=[Screen.blocks['linSml'], Screen.blocks['angSml'], Screen.blocks['junSml']]
            elif bType=='2':
                newBlocks=[Screen.blocks['linBig'], Screen.blocks['angBig'], Screen.blocks['junBig']]
            elif bType=='3':
                newBlocks=[Screen.blocks['linDbl'], Screen.blocks['angDbl'], Screen.blocks['junDbl']]
            elif bType=='4':
                newBlocks=[Screen.blocks['linAux'], Screen.blocks['angAux'], Screen.blocks['junAux']]

            self.__blocks=newBlocks


        def InsertScreenData(self, width, height, sData):
            divid, sData, i=list(self.Data), list(sData), 0
            if self.__orient=='hor': # Code for horizontal dividor
                for y in range(height):
                    for x in range(width+1):
                        if y==self.Position[1]:
                            if x in range(1, width) and sData[(width+2)*y+x]==self.Blocks[0][1]:
                                sData[(width+2)*y+x]=self.Blocks[2][4]
                            else:sData[(width+2)*y+x]=divid[i]
                            i+=1
            else: # Code for vertical dividor
                for y in range(height+1):
                    for x in range(width):
                        if x==self.Position[0]:
                            if y in range(1, height) and sData[(width+2)*y+x]==self.Blocks[0][0]:
                                sData[(width+2)*y+x]=self.Blocks[2][4]
                            else:sData[(width+2)*y+x]=divid[i]
                            i+=1
            return sData


    class Banner(object):
        pass


class ScreenBox(Screen):
    ''' '''
    def __init__(self, width, height, bType, xPos, yPos):
        '''Constructor'''
        if width<2 or height<2: raise ValueError('Box has to be at least 2x2')
        super().__init__(width, height, bType)
        self.__xPos=xPos
        self.__yPos=yPos

    @property
    def Position(self):
        return self.__xPos, self.__yPos
    @Position.setter
    def Position(self, newPos):
        try: newX, newY=newPos
        except ValueError:
            raise ValueError("Pass an iterable with two items")
        else:
            assert all((newX>=0, newY>=0))
            self.__xPos, self.__yPos=newX, newY


    def InsertScreenData(self, width, height, sData):
        box, sData, i=list(filter(lambda a: a!='\n', self.Data)), list(sData), 0
        for y in range(height):
            for x in range(width):
                if x in range(self.__xPos, self.__xPos+self.Size[0]) and y in range(self.__yPos, self.__yPos+self.Size[1]) and sData[(width+2)*y+x]==' ':
                    sData[(width+2)*y+x]=box[i]
                    i+=1
        return sData


    def AddGauge(self, option, unit=None, data=None, title=None):
        ''' '''
        self.Elements.append(ScreenBox.Gauge(option, self.Size, unit, data, title))
        return self.Elements[-1]


    class Gauge(object):
        ''' '''
        # Generic name iterator
        idIter=1

        def __init__(self, option, boxSize, unit=None, data=None, title=None):
            '''Constructor'''
            self.__title='Gauge '+str(self.idIter) if not title else title
            self.__unit=unit
            self.__type=option
            if boxSize[0]<3 or boxSize[1]<3: raise ValueError('Box is too small')

            if option=='int' and data==None: self.__data=0
            elif option=='int' and not isinstance(data, int):
                raise TypeError('Non Int in Int gauge')
            if option=='flt' and data==None: self.__data=0.0
            elif option=='flt' and not isinstance(data, float):
                raise TypeError('Non Float in Float gauge')
            if option=='str' and data==None: self.__data='N/A'
            elif option=='str' and not isinstance(data, str):
                raise TypeError('Non String in String gauge')
            if option=='prc' and data==None: self.__data=0.0
            elif option=='prc' and not isinstance(data, float):
                raise TypeError('Non Float in Percent gauge')
            self.idIter+=1
            self.__CreateGauge()

        def __CreateGauge(self):
            '''Create gauge data '''
            self.Data=(str(self.Title), str(self.Data), str(self.Unit))

        @property
        def Title(self):
            return self.__title
        @Title.setter
        def Title(self, newTitle):
            self.__title=newTitle

        @property
        def Unit(self):
            return self.__unit
        @Unit.setter
        def Unit(self, newUnit):
            self.__unit=newUnit

        @property
        def Data(self):
            return self.__data
        @Data.setter
        def Data(self, newData):
            if self.__type=='int' and not isinstance(newData, int):
                raise TypeError('Non Int in Int gauge')
            elif self.__type=='flt' and not isinstance(newData, float):
                raise TypeError('Non Float in Float gauge')
            elif self.__type=='str' and not isinstance(newData, str):
                raise TypeError('Non String in String gauge')
            elif self.__type=='prc' and not isinstance(newData, float):
                raise ValueError('Non Float in Precent gauge')
            elif self.__type=='prc' and not newData in range(0.0, 100.0):
                raise ValueError('Outside percent range')
            else:self.__data=newData


        def InsertScreenData(self, width, height, sData):
            reqLines1=int(width/len(self.Data[0]))+1
            reqLines2=int(width/len(self.Data[1]))+1
            reqLines3=int(width/len(self.Data[2]))+1
            reqLines=reqLines1+reqLines2+reqLines3
            if reqLines>height: raise ValueError('Not enough screen space')

            # for j in range(height):
                # for x in range(width):
                    # if height>3 and j