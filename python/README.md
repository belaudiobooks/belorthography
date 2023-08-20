# Łacinka

Python 3 library for converting Belarusian cyrillic case to latin

### Create Python virtual enviroment

Ensure venv is installed:
```
apt-get install python3-venv
```

In the project folder run:
```
python -m venv ./venv
source ./venv/bin/activate
```

### Setup package and run tests:
```
python setup.py develop
pip install -r requirements.txt
pytest
```

### Diff mode

Diff mode helps to see if changes to translation algorithms have any effect. it is useful during development, especially while we are working on an existing algorithm that we don't fully understand yet. Steps to use it:

1. Guard changes using `diff_mode.is_new()` condition. For example in order to test whether removal of some conversion affects results:

```python
if not diff_mode.is_new():
    res = res.replace('сллі', 'ślli')
```

2. Run diff tool:

```
python diff.py
```

It will go through a set of Belarusian texts, converting each into Lacinka twice: once with `is_new()` being set to False (golden) and once with it set to True (test). If there are changes - they will be printed an a html file with nice handy UI.

3. Run tests:

```
DIFF_NEW=true pytest
```

This will run unit tests with `is_new()` being set to true. This helps to quickly see if the change affects existing tests. If you change affects a set of sample texts from step 2 but doesn't affect any unit tests - consider adding a new unit test.