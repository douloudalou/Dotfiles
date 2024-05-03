How to use Mobius.py to create mobius profiles

1) Save the datas into " Profile.xlsx " under " Mobius " folder.
2) Ensure that the Date of birth, Date of enlistment, Date of ord are in mm/dd/yy format.
3) If not in correct format, can use google sheet to assist in formatting.
4) On a new column, input " =IF(ISBLANK(I1); IF(ISBLANK(J1); IF(ISBLANK(K1); L1; K1); J1); I1) ", then change the title of the column to " Node ".
5) Run the script using, scrapy runspider Mobius.py
6) Enter the sheet to automate. 
