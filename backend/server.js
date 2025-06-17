import express, { json } from 'express';
import { spawn } from 'child_process';
import cors from 'cors';

const app = express();
const PORT = 5000;

app.use(cors());
app.use(json());

app.post('/choose-llm', (req, res) => {
  const query = req.body.query;

  const pyProcess = spawn('python', ['find_best_models.py', query]);

  let result = '';
  pyProcess.stdout.on('data', (data) => {
    result += data.toString();
  });

  pyProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });

  pyProcess.on('close', (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: 'Python script failed' });
    }

    try {
      const parsed = JSON.parse(result);
      const namesOnly = parsed.models.map(m => m.model_name);
      res.json({ llms: namesOnly });
    } catch (e) {
      res.status(500).json({ error: 'Invalid output from Python script' });
    }
  });
});

app.listen(PORT, () => {
  console.log(`Server running at http://localhost:${PORT}`);
});
