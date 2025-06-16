const http = require('http');
const { spawn } = require('child_process');

const PORT = 5000;

function sendJSON(res, statusCode, data) {
  res.writeHead(statusCode, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
  });
  res.end(JSON.stringify(data));
}

const server = http.createServer((req, res) => {
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': 86400,
    });
    return res.end();
  }

  if (req.url === '/choose-llm' && req.method === 'POST') {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      let parsed;
      try {
        parsed = JSON.parse(body);
      } catch (err) {
        return sendJSON(res, 400, { error: 'Invalid JSON' });
      }
      if (!parsed.query) {
        return sendJSON(res, 400, { error: 'Query not provided' });
      }

      const py = spawn('python', ['backend/run_find_best_models.py', parsed.query]);

      let output = '';
      py.stdout.on('data', data => { output += data.toString(); });

      let errData = '';
      py.stderr.on('data', data => { errData += data.toString(); });

      py.on('close', code => {
        if (code !== 0) {
          console.error(errData);
          return sendJSON(res, 500, { error: 'Python process failed' });
        }
        try {
          const result = JSON.parse(output);
          const llms = (result.models || []).map(m => m.model_name);
          return sendJSON(res, 200, { llms });
        } catch (e) {
          console.error('Parsing error:', e);
          return sendJSON(res, 500, { error: 'Failed to parse Python output' });
        }
      });
    });
  } else {
    sendJSON(res, 404, { error: 'Not found' });
  }
});

server.listen(PORT, () => {
  console.log(`Server listening on port ${PORT}`);
});
