var gplay = require('google-play-scraper');
var ObjectsToCsv = require('objects-to-csv');

const object = {
				// './out/etrade.csv': 'com.etrade.mobilepro.activity',
				// './out/power_etrade.csv': 'com.aperturegroup.mobile',
				// './out/ms.csv': 'com.morganstanley.clientmobile.prod',
				
				// './out/mymerrill.csv': 'com.ml.mobile.mymerrill',
				// './out/merrilledge.csv': 'com.ml.mobile.edge',
				// './out/boa.csv': 'com.infonow.bofa',
				// './out/UBS.csv': 'com.ubs.clientmobile',
				// './out/NT.csv': 'com.ubs.clientmobile',
				
				'./out/robinhood.csv': 'com.robinhood.android',
				'./out/td.csv': 'com.tdameritrade.mobile3',
				// './out/schwab.csv': 'com.schwab.mobile',
                // './out/marcus.csv': 'com.marcus.android',
				// './out/fidelity.csv': 'com.fidelity.android',
				// './out/personalcapital.csv': 'com.personalcapital.pcapandroid',	

				
            };

for (const [key, value] of Object.entries(object)) {
    const data = gplay.reviews({
                                    appId: value,
                                    sort: gplay.sort.NEWEST,
                                    num : '10000'
                                })
    data.then(function(value) {
        // If you use "await", code must be inside an asynchronous function:
        (async () => {
            const csv = new ObjectsToCsv(value);
        
            // Save to file:
            await csv.toDisk(key);
        })();
    });
}






// var gplay = require('google-play-scraper');

// let reviews = gplay.reviews({
//                 appId: 'com.chase.sig.android',
//                 sort: gplay.sort.NEWEST,
//                 num : '10000'
//               }).then(console.log, console.log);

// // writefile.js

// const fs = require('fs');

// // write to a new file named 2pac.txt
// fs.writeFile('reviews.txt', reviews, (err) => {
//     // throws an error, you could also catch it here
//     if (err) throw err;

//     // success case, the file was saved
//     console.log('reviews saved!');
// });