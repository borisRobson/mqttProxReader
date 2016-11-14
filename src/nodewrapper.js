var PythonShell = require('python-shell');

PythonShell.run('main.py', function(err){
	if(err) throw err;
	console.log('finished');
});
