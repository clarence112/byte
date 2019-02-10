import os, pygame, sys
pygame.init()

import platform
if platform.system() == "Windows":
    print("Using windows taskbar icon workaround")
    import ctypes
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("clarence112.byte")

def byteSetup():

    global needsSave
    needsSave = False

    if os.path.isfile("cfg.cfg"):

        global blockNames
        blockNames = ["Motion", "Looks", "Display", "Tiles", "Sound", "Events", "Control", "Sensing", "Operators", "Variables", "Lists", "System", "Files", "Functions", "Libraries", "Numbers", "Strings", "Iterables", "Error", "error2"]

        global byteFont
        byteFont = pygame.font.Font("byteAssets/rubik.ttf", 12)

        global byteCfg
        byteCfg = []

        global scroll
        scroll = 0

        with open("cfg.cfg") as f:
            byteCfgFile = f.read().splitlines()
        #print(byteCfgFile)

        byteCfg.append(int(float(byteCfgFile[1]))) #defalut screensize
        byteCfg.append(int(float(byteCfgFile[2])))

        #print(byteCfg)

        for i in range(21): #Block colors, every other line starting on line 8, ending on line 48
            byteCfg.append(int(byteCfgFile[(i * 2) + 7], 0)) # :'( note to self: this isn't lua, arrays start at 0

        byteCfg.append(int(byteCfgFile[50], 0)) #Text color

        byteCfg.append(int(byteCfgFile[53], 0)) #debug mode(s)

        print(byteCfg)

        byteLogos = []
        byteLogos.append(pygame.image.load("byteAssets/byteIcon32.png"))
        byteLogos.append(pygame.image.load("byteAssets/byteIcon256.png"))
        byteLogos.append(pygame.image.load("byteAssets/byteText.png"))
        byteLogos.append(pygame.image.load("byteAssets/byteLogo.png"))
        pygame.display.set_caption("Byte IDE")
        pygame.display.set_icon(byteLogos[0])

        global size
        size = width, height = byteCfg[0], byteCfg[1] #NOT LUA. ARRAYS START AT 0.
        global screen
        screen = pygame.display.set_mode(size, pygame.RESIZABLE)
        global clock
        clock = pygame.time.Clock()

        if byteCfg[24] == 1:
            global testindex
            testindex = 0

        global byteMenu
        byteMenu = 0

    else:
        print("Generating new config file")
        # ***************************************************************
        # When making new config options: append, don't insert. This will
        # prevent lots of code from needing to be updated for the new
        # config layout.
        # ***************************************************************
        byteCfgFile = open("cfg.cfg", "w+")

        byteCfgFile.write("Default Window Size:\n")
        windowInfo = pygame.display.Info()
        byteCfgFile.write(str(windowInfo.current_w / 1.5) + "\n")
        byteCfgFile.write(str(windowInfo.current_h / 1.5) + "\n\n")

        byteCfgFile.write("Block colors:\n\n")

        byteCfgFile.write("blockMotion\n")
        byteCfgFile.write("0x003cde\n")
        byteCfgFile.write("blockLooks\n")
        byteCfgFile.write("0x8b66d5\n")
        byteCfgFile.write("blockDisplay\n")
        byteCfgFile.write("0xf568eb\n")
        byteCfgFile.write("blockTiles\n")
        byteCfgFile.write("0xc47cea\n")
        byteCfgFile.write("blockSound\n")
        byteCfgFile.write("0xd500bf\n")
        byteCfgFile.write("blockEvents\n")
        byteCfgFile.write("0xbc9232\n")
        byteCfgFile.write("blockControl\n")
        byteCfgFile.write("0xe6d000\n")
        byteCfgFile.write("blockSensing\n")
        byteCfgFile.write("0x2be9ea\n")
        byteCfgFile.write("blockOperators\n")
        byteCfgFile.write("0x19b100\n")
        byteCfgFile.write("blockVariables\n")
        byteCfgFile.write("0xf29700\n")
        byteCfgFile.write("blockLists\n")
        byteCfgFile.write("0xb07108\n")
        byteCfgFile.write("blockSystem\n")
        byteCfgFile.write("0x6f965f\n")
        byteCfgFile.write("blockFiles\n")
        byteCfgFile.write("0x80b1b1\n")
        byteCfgFile.write("blockFunctions\n")
        byteCfgFile.write("0x3e0ca4\n")
        byteCfgFile.write("blockLibraries\n")
        byteCfgFile.write("0xaa4865\n")
        byteCfgFile.write("blockNumbers\n")
        byteCfgFile.write("0xd3ef00\n")
        byteCfgFile.write("blockStrings\n")
        byteCfgFile.write("0xbad201\n")
        byteCfgFile.write("blockIterables\n")
        byteCfgFile.write("0x9dae17\n")
        byteCfgFile.write("jmpIndicator\n")
        byteCfgFile.write("0xff0000\n")
        byteCfgFile.write("Invalid\n")
        byteCfgFile.write("0x5c0000\n")
        byteCfgFile.write("darkenBy\n")
        byteCfgFile.write("15\n\n")

        byteCfgFile.write("TextColor\n")
        byteCfgFile.write("0xffffff\n\n")

        byteCfgFile.write("Debug Mode\n")
        byteCfgFile.write("0\n\n")

        byteCfgFile.close()

        byteSetup()

byteSetup()

def byteBttn(action, textinput, x = 0, y = 0, bgcolor = [0, 0, 0], key = 1, textcolor = [255, 255, 255]):
    textsize = pygame.font.Font.size(byteFont, textinput)  # lint:ok
    pygame.draw.rect(screen, bgcolor, pygame.Rect((x, y), (textsize[0] + 10, textsize[1])))
    textrend(textinput, x + 5, y)
    global byteButtons
    byteButtons.append([action, x, y, x + textsize[0] + 10, y + textsize[1], key])

def byteRegion(action, x = 0, y = 0, w = 10, h = 10, key = 1):
    global byteButtons
    byteButtons.append([action, x, y, x + w, y + h, key])

def byteBttnChk(x, y, key):
    for button in byteButtons:
        if (button[1] <= x <= button[3]) and (button[2] <= y <= button[4]) and (key == button[5]):
            exec(button[0])

def byteDialogue():
    pass

def textrend(textinput, x = 0, y = 0, textcolor = [255, 255, 255], aa = True):
    byteTextSuface = byteFont.render(textinput, aa, textcolor)  # lint:ok
    screen.blit(byteTextSuface,(x, y))

def displayTest():
    global testindex
    testindex = testindex + 1   # lint:ok
    if testindex > 19:
        testindex = 0
    screen.fill(byteCfg[testindex])  # lint:ok

def drawLayers():
    screen.fill(0xbbbbbb)
    drawLayer0()
    drawLayer1()

def drawLayer0():
    if byteMenu == 0:  # lint:ok
        pygame.draw.rect(screen, 0x646464, pygame.Rect((193, scroll + 18), (5, 16)))  # lint:ok
        byteRegion("global scroll; scroll = scroll + 16", 0, 16, 200, size[1], 5)
        byteRegion("global scroll; scroll = scroll - 16", 0, 16, 200, size[1], 4)
        for i in list(range(18)):
            if (size[1] + (i * 16)) <= scroll:  # lint:ok
                pygame.draw.rect(screen, byteCfg[i + 2], pygame.Rect((0, 16 * (i + 1)), (191, 16)))  # lint:ok
            else:
                pygame.draw.rect(screen, byteCfg[i + 2], pygame.Rect((0, size[1] - (scroll - (16 * (i + 1)))), (191, 16)))  # lint:ok
                byteBttn("pass", blockNames[i], 0, size[1] - (scroll - (16 * (i + 1))), byteCfg[i + 2])  # lint:ok


def drawLayer1():
    global size
    pygame.draw.rect(screen, 0x999999, pygame.Rect((0, 0), (size[0], 16)))  # lint:ok
    if byteMenu == 0:  # lint:ok
        pygame.draw.rect(screen, 0x999999, pygame.Rect((200, 16), (3, size[1] - 16)))  # lint:ok block shelf divider
        byteBttn("global byteMenu; byteMenu = 0", "Code", size[0] - 281, 0, [120, 120, 160]); byteBttn("global byteMenu; byteMenu = 1", "Tiles and Costumes", size[0] - 240, 0, [100, 100, 100]); byteBttn("global byteMenu; byteMenu = 2", "Stage", size[0] - 118, 0, [100, 100, 100]); byteBttn("global byteMenu; byteMenu = 3", "Map Editor", size[0] - 72, 0, [100, 100, 100])
    elif byteMenu == 1:  # lint:ok
        byteBttn("global byteMenu; byteMenu = 0", "Code", size[0] - 281, 0, [100, 100, 100]); byteBttn("global byteMenu; byteMenu = 1", "Tiles and Costumes", size[0] - 240, 0, [120, 120, 160]); byteBttn("global byteMenu; byteMenu = 2", "Stage", size[0] - 118, 0, [100, 100, 100]); byteBttn("global byteMenu; byteMenu = 3", "Map Editor", size[0] - 72, 0, [100, 100, 100])
    elif byteMenu == 2:  # lint:ok
        byteBttn("global byteMenu; byteMenu = 0", "Code", size[0] - 281, 0, [100, 100, 100]); byteBttn("global byteMenu; byteMenu = 1", "Tiles and Costumes", size[0] - 240, 0, [100, 100, 100]); byteBttn("global byteMenu; byteMenu = 2", "Stage", size[0] - 118, 0, [120, 120, 160]); byteBttn("global byteMenu; byteMenu = 3", "Map Editor", size[0] - 72, 0, [100, 100, 100])
    elif byteMenu == 3:  # lint:ok
        byteBttn("global byteMenu; byteMenu = 0", "Code", size[0] - 281, 0, [100, 100, 100]); byteBttn("global byteMenu; byteMenu = 1", "Tiles and Costumes", size[0] - 240, 0, [100, 100, 100]); byteBttn("global byteMenu; byteMenu = 2", "Stage", size[0] - 118, 0, [100, 100, 100]); byteBttn("global byteMenu; byteMenu = 3", "Map Editor", size[0] - 72, 0, [120, 120, 160])

    byteBttn("pass", "File", 2, 0, [100, 100, 100]); byteBttn("pass", "Edit", 34, 0, [100, 100, 100]) # file and edit buttons

testvar = 0

while True:

    byteButtons = []

    if byteCfg[24] == 1: # lint:ok
        displayTest()
        clock.tick(2) # lint:ok
    elif byteCfg[24] == 2: # lint:ok
        textrend("text test")
    else:
        drawLayers()
        if testvar == 0:
            print(byteButtons)
            testvar = 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if needsSave:  # lint:ok
                pass
            else:
                sys.exit()

        if event.type == pygame.VIDEORESIZE:
            global size
            oldScreen = screen  # lint:ok
            size = [event.w, event.h]
            if size[0] < 485:
                size[0] = 485
            if size[1] < 400:
                size[1] = 400
            screen = pygame.display.set_mode(size , pygame.RESIZABLE)
            screen.blit(oldScreen, (0, 0))
            del oldScreen
            #print(size)

        if event.type == pygame.MOUSEBUTTONUP:
            byteBttnChk(event.pos[0], event.pos[1], event.button)

    pygame.display.flip()
