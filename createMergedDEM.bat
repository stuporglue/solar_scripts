::
:: Produce a single merged DEM from the 16 4342-01-24____.laz 1/16 laz tiles
:: Save the .bat file in the folder containing you laz or add path in blast2dem call
:: Ran in 179 seconds

set PATH=%PATH%;C:\lastools\bin;

:: create point density grid for entire project
:: this step creates lax files to speed up future processing, only necessary if touching data more than once
:: only 2 cores allowed in unlicensed version
::lasindex -i *.laz -cores 2

mkdir mplsdem

blast2dem -v -i 4342-01-24*.laz -merged -first_only -elevation -kill 50 -odir mplsdem -oimg

::blast2dem -v -i 4342*.laz -merged -first_only -elevation -kill 100 -o hennepin_4342.img

pause
