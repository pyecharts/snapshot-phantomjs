isort $(find snapshot_phantomjs -name "*.py"|xargs echo) $(find tests -name "*.py"|xargs echo)
black -l 79 snapshot_phantomjs
black -l 79 tests
