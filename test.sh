pip freeze
nosetests --with-coverage --cover-package snapshot_phantomjs --cover-package tests tests  docs/source snapshot_phantomjs && flake8 . --exclude=.moban.d,docs --builtins=unicode,xrange,long
