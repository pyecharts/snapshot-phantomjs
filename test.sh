pip freeze
nosetests --with-coverage --cover-package snapshot_phantomjs --cover-package tests tests snapshot_phantomjs && flake8 . --exclude=.moban.d --builtins=unicode,xrange,long
