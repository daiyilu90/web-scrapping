var store = require('app-store-scraper');
var ObjectsToCsv = require('objects-to-csv');

const object = {
				'./out/etrade.csv': 313259740,
				'./out/power_etrade.csv': 1111881020,
				'./out/ms.csv': 811512122,
				
			
				'./out/mymerrill.csv': 420490216,
				'./out/merrilledge.csv': 420496625,
				'./out/boa.csv': 284847138,
				'./out/UBS.csv': 952739938,
				
				'./out/robinhood.csv': 938003185,
				'./out/td.csv': 534659421,
				
				
				'./out/schwab.csv': 407358186,
                './out/marcus.csv': 1489511701,
				'./out/fidelity.csv': 348177453,
				'./out/personalcapital.csv': 504672168,	
            };
		
for (const [key, value] of Object.entries(object)) {
	for (var i =1; i<101; i++){
		const data = store.reviews({
										id: value,
										sort: store.sort.RECENT,
										page: i
									})
			// If you use "await", code must be inside an asynchronous function:
		// console.log(i);
		// console.log(key);
		data.then(function(value) {
		new ObjectsToCsv(value).toDisk(key,{append:true})})
}}
