#!/bin/bash

# Ścieżka do Twojego agenta (używamy pełnej ścieżki, żeby działało wszędzie)
AGENT_PATH="kanboard_setup/kb_manager.py"
# Nazwa projektu to nazwa obecnego katalogu
PROJECT_NAME=$(basename "$PWD")

echo "🚀 Inicjalizacja projektu w Kanboard dla: $PROJECT_NAME"

# Wywołanie agenta
python3 "$AGENT_PATH" init "$PROJECT_NAME"

if [ $? -eq 0 ]; then
    echo "✅ Gotowe! Projekt '$PROJECT_NAME' jest aktywny w Kanboard."
else
    echo "❌ Wystąpił błąd podczas tworzenia projektu."
fi
