# global-ice-sheet-data-analysis-2016
This project aggregates the NSIDC G02135 Sea Ice Index dataset files and produces graphs showing the historical trends of global ice extents.

## Purpose and Reasoning
The G02135 dataset is broken into two parts: the northern hemisphere (the Arctic ice data) and the southern hemisphere (the Antarctic ice data). However, there is no combined global dataset, and so getting a historical comparison view of the global ice extent data isn't possible using just files provided by NSIDC. Additionally, the dataset for each hemisphere is broken into a historical "finalized" file containing all the data up to the end of the previous year, and a daily-updated file for the current year, which adds additional (if minor) complexity to the process of compiling the data.

Outputting the aggregated data to a CSV for plotting using traditional spreadsheet software proved more difficult than initially thought, due to needing each year as a separate trendline. Thus, matplotlib was chosen so that complete control over the produced graphs would be possible.

## Requirements
Requires matplotlib and Python 2.7.

## Usage
Copy the entire repository to a directory. Navigate to that directory, and run the **calc.py** script through your Python interpreter of choice. It will produce new copies of the three image files. Uncomment the block of file-writing code in the middle of the script to also produce a CSV containing the aggregated data, sorted by ascending date.

## Data Source
Homepage: https://nsidc.org/data/g02135

The most recent version of the dataset files can be found on the University of Colorado SIDADS FTP server:

ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/north/daily/data/
ftp://sidads.colorado.edu/DATASETS/NOAA/G02135/south/daily/data/

You should be able to copy the CSV dataset files with the matching names from the server and overwrite the ones provided here to generate graphs with updated data. The files provided here are **NOT** regularly updated, and users are highly encouraged to update to the dataset files from the SIDADS server before generating new graphs.

## Citation
Fetterer, F., K. Knowles, W. Meier, and M. Savoie. 2016, updated daily. *Sea Ice Index, Version 2*. Boulder, Colorado USA. NSIDC: National Snow and Ice Data Center. doi: http://dx.doi.org/10.7265/N5736NV7. Accessed: 2016-11-28.
