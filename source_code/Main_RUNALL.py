# -*- coding: utf-8 -*-

import Main_Indicator_VolumeSpike
import Main_Download_MalaysiaStockLists
import Main_Append_Existing_Files
import Main_SendEmail

def main():

    Main_Download_MalaysiaStockLists.main()
    Main_Append_Existing_Files.main()
    Main_Indicator_VolumeSpike.main()
    Main_SendEmail.main()  

if __name__ == "__main__":
    main()