module.exports = function(RED){
	var PythonShell = require('python-shell');
	function readerRun(config){
		RED.nodes.createNode(this, config);
		var node = this;
		this.on('input', function(){
			PythonShell.run('main.py',function(err){
				if(err) throw err;
				console.log('finished');
			})
		});
	}
	RED.nodes.registerType("mqttproxreader", readerRun);}
