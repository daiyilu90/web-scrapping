# Google Play Store app review scrapping and analysis

Scaping module is based on google-play_scraper. 
More details can be found at: https://github.com/facundoolano/google-play-scraper.git


To run the scrapping:
First step: download and install Node.js at:
https://nodejs.org/en/download/

Second step: install packges in command (take sometime):
1.Create a new folder such as "scraper"
2.Open CMD and change directory to that new folder
e.g. cd C:\Users\Yilu Dai\Desktop\Scraper
3.in CMD run command and install latest packages
npm install google-play-scraper 
npm install objects-to-csv  
(if you see "found 0 vulnerabilities", packages are successfully installed)

Third Step: Write your js parsing files and run the files
1.create a new file or make changes to scrape_reviews.js 
2.create output folder and call it "out" or what you named in your new file
3.in CMD run command: node scrape_reviews.js

Final Step: check scrapped output files in out folder

***Alternatively, in order to extract app details instead of reviews, run scrape_app_details.js

To run the analysis:
- After updating the ngram_theme_dictionary.csv, run sentiment_analysis_google_play_reviews.py
- The first half of the sentiment_analysis_google_play_reviews.py script can be repurposed to export a ngram list to create the ngram theme dictionary from. TO DO: Write a version of the sentiment analysis script that can be run for this purpose without modification.
