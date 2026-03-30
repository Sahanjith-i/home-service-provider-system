const { PythonShell } = require('python-shell');

let options = {
  mode: 'text',
};

PythonShell.run('script.py', options, function (err, results) {
  if (err) throw err;
  console.log('Python output:', results);
});