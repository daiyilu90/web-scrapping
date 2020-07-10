var gplay = require('google-play-scraper');
var ObjectsToCsv = require('objects-to-csv');

const bank_dict = {'./out/chase_appdetails.csv': 'com.chase.sig.android',
                './out/tdbank_appdetails.csv': 'com.tdbank',
                './out/capitalone_appdetails.csv': 'com.konylabs.capitalone',
                './out/discover_appdetails.csv':'com.discoverfinancial.mobile',
                './out/amex_appdetails.csv':'com.americanexpress.android.acctsvcs.us',
                './out/pnc_appdetails.csv':'com.pnc.ecommerce.mobile',
            };

var arr = []
var counter = Object.keys(bank_dict).length
console.log(counter)

for (const [key, value] of Object.entries(bank_dict)) {
    const data = gplay.app({
                                appId: value
                            })
    data.then((app) => {
        console.log(app.histogram);
        arr.push(app.histogram)
    })
    counter-=1
    console.log(counter)
    if(counter==0) {
       write_file() 
    }
}

function write_file() {
    // write file to csv
    console.log(arr)
    const csv = new ObjectsToCsv(arr);
    csv.toDisk('test.csv');
    }


// // console.log(arr)

// arr.then(function(value) {
//     // If you use "await", code must be inside an asynchronous function:
//     (async () => {
//         const csv = new ObjectsToCsv(value);
    
//         // Save to file:
//         await csv.toDisk(key);
//     })();
// });