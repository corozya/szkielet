#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const https = require('https');

// Load environment variables
const envPath = path.join(__dirname, '../kanboard_setup/.env');
const env = {};
fs.readFileSync(envPath, 'utf-8')
  .split('\n')
  .filter(line => line.trim() && !line.startsWith('#'))
  .forEach(line => {
    const [key, value] = line.split('=');
    if (key && value) env[key.trim()] = value.trim();
  });

const KANBOARD_URL = env.KANBOARD_URL;
const KANBOARD_USER = env.KANBOARD_USER;
const KANBOARD_TOKEN = env.KANBOARD_TOKEN;

function rpc(method, params = {}) {
  return new Promise((resolve, reject) => {
    const auth = Buffer.from(`${KANBOARD_USER}:${KANBOARD_TOKEN}`).toString('base64');
    const url = new URL(KANBOARD_URL);

    const options = {
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Basic ${auth}`,
      },
    };

    const req = (url.protocol === 'https:' ? https : require('http')).request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          if (json.error) reject(new Error(json.error.message));
          else resolve(json.result);
        } catch (e) {
          reject(e);
        }
      });
    });

    req.on('error', reject);
    req.write(JSON.stringify({
      jsonrpc: '2.0',
      method,
      params,
      id: 1,
    }));
    req.end();
  });
}

async function main() {
  console.log('Szukam projektów...\n');
  for (let id = 1; id <= 20; id++) {
    try {
      const project = await rpc('getProjectById', { project_id: id });
      if (project) {
        console.log(`[${id}] ${project.name} (active: ${project.is_active})`);
      }
    } catch (e) {
      // Ignore
    }
  }
}

main().catch(err => console.error('Error:', err.message));
