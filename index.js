const express = require('express');
const mysql = require('mysql');
const colors = require('colors');

const app = express();
const port = 4000;

const pool = mysql.createPool({
	connectionLimit: 	10,
	host: 		'localhost',
	user: 		'root',
	password: 	'root',
	database: 	'transactions'
});

// pool.connect((err) => {
// 	if (err) {
// 		console.error(err.code.bold.red.inverse);
// 	} else {
// 		console.log('Db connection established'.green.inverse);
// 	}
// });


app.get('/', (req, res) => res.send('Hello World'));

app.get('/transactions/all', (req, res) => {
	const statement = 'select * from transaction;';
	pool.query(statement, function (err, results, fields) {
		if (err) {
			console.log(err.code.red.inverse);
			throw err;
		} else {
			console.log(typeof(results));
			res.send(results);
		}
	})
});

app.get('/transactions/:uId', (req, res) => {

	console.log('req.uId: ' + req.params.uId);
	res.send('user id: ' + req.params.uId);
});

app.listen(port, () => console.log('Starting up server'));