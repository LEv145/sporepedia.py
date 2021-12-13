
.PHONY: build
build:
	pip install --editable .


.PHONY: binary
binary:
	pyinstaller pyinstaller.spec --distpath pyinstaller_builds/linux_dist --workpath pyinstaller_builds/linux_build


.PHONY: mkinit
mkinit:
	mkinit sporepedia -w --black --nomods --relative --recursive


.PHONY: run_tests
run_tests:
	tox


.PHONY: coverage_status
coverage_status:
	coverage run -m unittest discover tests "test_*"
	coverage report -m


.PHONY: clear
clear:
	rm -R build/ dist/ .eggs/ pyinstaller_builds/

