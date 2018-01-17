A Python project with a single script to check if your letter grades have been assigned on your latest semester,
for Bogazici University students.

## Installation of the required packages

Prior to installation of required packages, you may want to create an isolated space for them via a virtual environment, as follows:

```powershell
# on Windows with PowerShell

# This creates a virtual environment folder called 'env'
python -m venv env

# This one activates the virtual environment
./env/Scripts/activate
```

The `requirements.txt` file is for the required packages which you may install through:

```powershell
pip install -r requirements.txt
```

## Running the script

You may run the script, simply by passing the script to the Python interpreter:

```powershell
# Make sure that your virtual environment is active first
./env/Scripts/activate

# Run the script
python SemesterGrades.py
```

It will prompt you to enter your credentials. To keep your password away from the eyes nearby,
choose not to see your password as you type when asked.

**Hint:** You may hard-code your credentials within the code, to skip re-entering them at each run.
Search for `credentials` within the script, and uncomment the lines where `credentials[uname]` and `credentials[upass]` are set.
Enter your student number and password there.

**Beware:** Anybody that has access to the script will be able to see your credentials!

## Shortcomings and TODOs

At some point, this script was capable of repeatedly querying the system for an update on the grades.
This was even the main purpose of the whole script,
to have a script-servant checking if any of my grades have been assigned by the end of a semester.

I will be updating this to give it that functionality back, later some time.
