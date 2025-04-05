mox inspect <file> storage-layout

$ mox test --coverage
---------- coverage: platform win32, python 3.11.2-final-0 -----------
Name Stmts Miss Branch BrPart Cover

---

C:\Users\nugge\AppData\Roaming\uv\tools\moccasin\Lib\site-packages\boa\environment.py 198 126 48 12 38%
script\_\_init\_\_.py 0 0 0 0 100%
script\deploy.py 17 6 2 1 63%
script\deploy_mockpricefeed.py 8 1 0 0 88%
tests\conftest.py 22 0 0 0 100%
tests\unit\test_unit_coffee.py 39 0 2 0 100%

---

TOTAL 284 133 52 13 52%

$ mox test --coverage --cov-report term-missing

# Test types

There are many types of tests:

    Unit: Test a single function/part of your code.
    Integration: Test how different parts of your code work together.
    Staging: Test your code in a production-like environment.
    Forked (Staging): Test your code in a production-like environment, but with a forked version of the blockchain.
    Fuzz: Test your code with random inputs.
    Formal Verification: Prove that your code is correct.

# Git commands

git init
git add .
git status
git commit -m "Commiting"
git remote add origin <>
git push -u origin master
git reflog # this sees what went the logs
git reset --hard HEAD@{1} # this helps to reset(rollback)
git rebase --continue # to stop the rebase
