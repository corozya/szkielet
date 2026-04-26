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
const KANBOARD_PROJECT = env.KANBOARD_PROJECT;

// Make JSON-RPC call
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

async function findProjectByName(name) {
  for (let id = 1; id <= 10; id++) {
    try {
      const project = await rpc('getProjectById', { project_id: id });
      if (project && project.name === name) {
        return project;
      }
    } catch (e) {
      // Try next
    }
  }
  return null;
}

async function checkTasks() {
  const taskIds = [2, 5, 9, 10, 11];

  try {
    // Get project
    const project = await findProjectByName(KANBOARD_PROJECT);
    if (!project) {
      console.error(`Projekt "${KANBOARD_PROJECT}" nie znaleziony`);
      process.exit(1);
    }

    // Get board with all tasks
    const board = await rpc('getBoard', { project_id: project.id });

    console.log('🔍 Sprawdzanie statusów zadań w Kanboard:\n');
    console.log('ID | Tytuł | Status | Kolumna');
    console.log('---|-------|--------|--------');

    const taskMap = {};
    board.forEach(swimlane => {
      if (swimlane.columns) {
        swimlane.columns.forEach(col => {
          if (col.tasks) {
            col.tasks.forEach(task => {
              taskMap[task.id] = {
                title: task.title,
                column: col.title,
                is_active: task.is_active,
              };
            });
          }
        });
      }
    });

    for (const taskId of taskIds) {
      if (taskMap[taskId]) {
        const t = taskMap[taskId];
        const status = t.is_active === 1 ? '✅ OTWARTY' : '❌ ZAMKNIĘTY';
        console.log(`${taskId} | ${t.title.substring(0, 40).padEnd(40)} | ${status} | ${t.column}`);
      } else {
        console.log(`${taskId} | ⚠️  Nie znaleziono w tablicy`);
      }
    }
  } catch (err) {
    console.error('Błąd:', err.message);
    process.exit(1);
  }
}

checkTasks();
