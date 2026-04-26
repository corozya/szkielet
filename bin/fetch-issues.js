#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const https = require('https');

// Load environment variables
const envPath = path.join(__dirname, '../kanboard_setup/.env');
if (!fs.existsSync(envPath)) {
  console.error('❌ Błąd: brak kanboard_setup/.env. Uruchom: npm run init-kb');
  process.exit(1);
}

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

if (!KANBOARD_URL || !KANBOARD_USER || !KANBOARD_TOKEN || !KANBOARD_PROJECT) {
  console.error('❌ Błąd: brakuje konfiguracji Kanboard w .env');
  process.exit(1);
}

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
  // Try common IDs 1-10
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

function formatTask(task) {
  let output = `   [${task.id}] ${task.title}`;
  if (task.assignee_name) {
    output += ` 👤 ${task.assignee_name}`;
  } else {
    output += ` ⚪`;
  }
  return output;
}

function createHandoffFile(task, column, project) {
  const handoffDir = path.join(__dirname, '../handoff');

  // Ensure handoff directory exists
  if (!fs.existsSync(handoffDir)) {
    fs.mkdirSync(handoffDir, { recursive: true });
  }

  // Create filename based on task ID and title (sanitize)
  const safeName = task.title.substring(0, 30).replace(/[^a-zA-Z0-9-]/g, '_').toLowerCase();
  const filename = `TASK_${task.id}_${safeName}.md`;
  const filepath = path.join(handoffDir, filename);

  // Skip if file already exists
  if (fs.existsSync(filepath)) {
    return null;
  }

  // Format date safely
  let dateStr = 'Unknown';
  if (task.date_creation) {
    try {
      dateStr = new Date(task.date_creation * 1000).toLocaleString('pl-PL');
    } catch (e) {
      dateStr = task.date_creation;
    }
  }

  const content = `# Zadanie: [${task.id}] ${task.title}

## Projekt
${project.name}

## Kolumna
${column}

## Opis
${task.description || '(brak opisu)'}

## Szczegóły
- **ID:** ${task.id}
- **Typ:** ${task.type || 'Task'}
- **Priorytet:** ${task.priority || 'Normal'}
- **Przypisane:** ${task.assignee_name || 'Nieprzypisane'}
- **Tworzy:** ${task.creator_name || 'Unknown'}
- **Data:** ${dateStr}

---

## Akcja wymagana

Przeanalizuj to zadanie i zdecyduj o działaniach. Po zakończeniu usuń ten plik z \`handoff/\`.
`;

  try {
    fs.writeFileSync(filepath, content, 'utf-8');
    return filename;
  } catch (e) {
    console.error(`❌ Błąd tworzenia pliku ${filepath}: ${e.message}`);
    return null;
  }
}

async function main() {
  try {
    console.log(`📋 Pobieranie zgłoszeń z projektu: ${KANBOARD_PROJECT}\n`);

    // Find project by name
    const project = await findProjectByName(KANBOARD_PROJECT);
    if (!project) {
      console.error(`❌ Projekt "${KANBOARD_PROJECT}" nie znaleziony`);
      process.exit(1);
    }
    const projectId = project.id;

    // Get board with all tasks
    const board = await rpc('getBoard', { project_id: projectId });
    if (!board || board.length === 0) {
      console.error('❌ Nie udało się pobrać tablicy (board)');
      process.exit(1);
    }

    // Count tasks only from Backlog column - tylko otwarte (is_active === 1)
    let totalTasks = 0;
    const allTasks = [];
    board.forEach(swimlane => {
      if (swimlane.columns) {
        swimlane.columns.forEach(col => {
          // Only process "Backlog" column
          if (col.title === 'Backlog' && col.tasks) {
            col.tasks.forEach(task => {
              // Pobierz tylko otwarte zadania
              if (task.is_active === 1) {
                totalTasks++;
                allTasks.push({ task, column: col.title, swimlane: swimlane.name });
              }
            });
          }
        });
      }
    });

    console.log(`✓ Projekt: ${project.name} (ID: ${projectId})`);
    console.log(`✓ Pobieranie: tylko kolumna "Backlog"`);
    console.log(`✓ Zgłoszeń w Backlog: ${totalTasks}\n`);

    if (totalTasks === 0) {
      console.log('Brak zgłoszeń w projekcie.');
      return;
    }

    // Create handoff files and close tasks in Kanboard
    let created = 0;
    let closed = 0;

    for (const { task, column, swimlane } of allTasks) {
      const filename = createHandoffFile(task, column, project);
      if (filename) {
        created++;

        // Close task in Kanboard (mark as Done)
        try {
          const result = await rpc('closeTask', { task_id: task.id });
          if (result) {
            closed++;
            console.log(`   ✓ Zamknięto (Done) [${task.id}]`);
          }
        } catch (e) {
          console.error(`   ⚠ Błąd zamykania [${task.id}]: ${e.message}`);
        }
      }
    }

    // Display tasks from Backlog column only - tylko otwarte
    board.forEach((swimlane, swimlaneIdx) => {
      if (swimlane.columns) {
        swimlane.columns.forEach(column => {
          if (column.title === 'Backlog' && column.tasks && column.tasks.length > 0) {
            const openTasks = column.tasks.filter(t => t.is_active === 1);
            if (openTasks.length > 0) {
              console.log(`📌 ${column.title} (${openTasks.length})`);
              openTasks.forEach(task => {
                console.log(formatTask(task));
              });
            }
          }
        });
      }
    });

    // Summary
    console.log();
    if (created > 0) {
      console.log(`✅ Utworzono ${created} zadań w \`handoff/\` do przeanalizowania`);
      console.log(`🔒 Zamknięto ${closed} zgłoszeń w Kanboard (zaznaczono jako Done)`);
    } else {
      console.log(`📝 Wszystkie zadania już istnieją w \`handoff/\``);
    }

  } catch (error) {
    console.error(`❌ Błąd: ${error.message}`);
    process.exit(1);
  }
}

main();
