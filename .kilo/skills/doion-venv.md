# Doion Virtual Environment Skill

This skill ensures that when working with the Doion Django project, the Python virtual environment is always activated before executing any Python-related commands.

## Usage

Before running any Python command (manage.py, pytest, etc.), this skill will:
1. Check if the virtual environment is already activated
2. If not, activate it from `backend/.venv/bin/activate`
3. Ensure we're in the project directory

## Automatic Activation

When working with this project, you should always:
- Use the provided `run.sh` script for starting the development server
- For other commands, ensure the venv is activated first

## Project Structure

- Backend root: `${workspaceFolder}/backend`
- Virtual environment: `${workspaceFolder}/backend/.venv`
- Activation script: `${workspaceFolder}/backend/.venv/bin/activate`

## Example Workflow

Instead of manually running:
```bash
source backend/.venv/bin/activate  # If not already activated
cd backend
python manage.py <command>
```

You can:
1. Use the helper script: `./run.sh` (from project root)
2. Or manually activate when needed:
   ```bash
   # Check if venv is active
   echo $VIRTUAL_ENV
   
   # If empty, activate it
   source backend/.venv/bin/activate
   
   # Then run your command
   python manage.py migrate
   ```

## Verification

To verify the virtual environment is active, check:
```bash
which python  # Should point to .venv/bin/python
echo $VIRTUAL_ENV  # Should show the venv path
```

This skill prevents common issues like:
- "ModuleNotFoundError: No module named 'django'"
- Running commands against system Python instead of project Python
- Inconsistent environments between team members
