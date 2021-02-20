from SAQWineList import SAQWineList
from VivinoAPI import VivinoAPI

def main():
    SAQ = SAQWineList()
    SAQ.writeToExcel()
    Vivino = VivinoAPI(SAQ.wineList)

if __name__ == '__main__':
    main()