# =============================================================================
# @file    Makefile
# @brief   Makefile for some steps in creating new releases on GitHub
# @date    2021-10-16
# @license Please see the file named LICENSE in the project directory
# @website https://github.com/caltechlibrary/commonpy
# =============================================================================

.ONESHELL: 				# Run all commands in the same shell.
.SHELLFLAGS += -e			# Exit at the first error.

# This Makefile uses syntax that needs at least GNU Make version 3.82.
# The following test is based on the approach posted by Eldar Abusalimov to
# Stack Overflow in 2012 at https://stackoverflow.com/a/12231321/743730

ifeq ($(filter undefine,$(value .FEATURES)),)
$(error Unsupported version of Make. \
    This Makefile does not work properly with GNU Make $(MAKE_VERSION); \
    it needs GNU Make version 3.82 or later)
endif

# Before we go any further, test if certain programs are available.
# The following is based on the approach posted by Jonathan Ben-Avraham to
# Stack Overflow in 2014 at https://stackoverflow.com/a/25668869

PROGRAMS_NEEDED = awk curl gh git jq sed python3
TEST := $(foreach p,$(PROGRAMS_NEEDED),\
	  $(if $(shell which $(p)),_,$(error Cannot find program "$(p)")))

# Set some basic variables.  These are quick to set; we set additional
# variables using "set-vars" but only when the others are needed.

name	 := $(strip $(shell awk -F "=" '/^name/ {print $$2}' setup.cfg))
version	 := $(strip $(shell awk -F "=" '/^version/ {print $$2}' setup.cfg))
url	 := $(strip $(shell awk -F "=" '/^url/ {print $$2}' setup.cfg))
desc	 := $(strip $(shell awk -F "=" '/^description / {print $$2}' setup.cfg))
author	 := $(strip $(shell awk -F "=" '/^author / {print $$2}' setup.cfg))
email	 := $(strip $(shell awk -F "=" '/^author_email/ {print $$2}' setup.cfg))
license	 := $(strip $(shell awk -F "=" '/^license / {print $$2}' setup.cfg))
initfile := $(name)/__init__.py
branch	 := $(shell git rev-parse --abbrev-ref HEAD)


# Print help if no command is given ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

help:
	@echo 'Available commands:'
	@echo ''
	@echo 'make'
	@echo 'make help'
	@echo '  Print this summary of available commands.'
	@echo ''
	@echo 'make report'
	@echo '  Print variables set in this Makefile from various sources.'
	@echo '  This is useful to verify the values that have been parsed.'
	@echo ''
	@echo 'make lint'
	@echo '  Run Python linters like flake8.'
	@echo ''
	@echo 'make test'
	@echo '  Run pytest.'
	@echo ''
	@echo 'make install'
	@echo '  Install the project in dev mode.'
	@echo ''
	@echo 'make release'
	@echo '  Do a release on GitHub. This will push changes to GitHub,'
	@echo '  open an editor to let you edit release notes, and run'
	@echo '  "gh release create" followed by "gh release upload".'
	@echo '  Note: this will NOT upload to PyPI, nor create binaries.'
	@echo ''
	@echo 'make update-doi'
	@echo '  Update the DOI inside the README.md file.'
	@echo '  This is only to be done after doing a "make release".'
	@echo ''
	@echo 'make packages'
	@echo '  Create the distribution files for PyPI.'
	@echo '  Do this manually to check that everything looks okay before.'
	@echo '  After doing this, do a "make test-pypi".'
	@echo ''
	@echo 'make test-pypi'
	@echo '  Upload distribution to test.pypi.org.'
	@echo '  Do this before doing "make pypi" for real.'
	@echo ''
	@echo 'make pypi'
	@echo '  Upload distribution to pypi.org.'
	@echo ''
	@echo 'make clean'
	@echo '  Clean up various files generated by this Makefile.'


# Gather values that we need ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.SILENT: vars
vars:
	$(info Gathering data -- this takes a few moments ...)
	$(eval repo	 := $(strip $(shell gh repo view | head -1 | cut -f2 -d':')))
	$(eval api_url   := https://api.github.com)
	$(eval id	 := $(shell curl -s $(api_url)/repos/$(repo) | jq '.id'))
	$(eval id_url	 := https://data.caltech.edu/badge/latestdoi/$(id))
	$(eval doi_url	 := $(shell curl -sILk $(id_url) | grep Locat | cut -f2 -d' '))
	$(eval doi	 := $(subst https://doi.org/,,$(doi_url)))
	$(eval doi_tail  := $(lastword $(subst ., ,$(doi))))
	$(info Gathering data -- this takes a few moments ... Done.)

report: vars
	@echo name	= $(name)
	@echo version	= $(version)
	@echo url	= $(url)
	@echo desc	= $(desc)
	@echo author	= $(author)
	@echo email	= $(email)
	@echo license	= $(license)
	@echo branch	= $(branch)
	@echo repo	= $(repo)
	@echo id	= $(id)
	@echo id_url	= $(id_url)
	@echo doi_url	= $(doi_url)
	@echo doi	= $(doi)
	@echo doi_tail	= $(doi_tail)
	@echo initfile = $(initfile)


# make lint & make test ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

lint:
	flake8 commonpy

test:
	pytest -v --cov=commonpy -l tests/


# make install ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

install:
	python3 -m pip install -e .[dev]


# make release ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

release: | test-branch release-on-github print-instructions

test-branch: vars
ifneq ($(branch),main)
	$(error Current git branch != main. Merge changes into main first!)
endif

update-init: vars
	@sed -i .bak -e "s|^\(__version__ *=\).*|\1 '$(version)'|"  $(initfile)
	@sed -i .bak -e "s|^\(__description__ *=\).*|\1 '$(desc)'|" $(initfile)
	@sed -i .bak -e "s|^\(__url__ *=\).*|\1 '$(url)'|"	    $(initfile)
	@sed -i .bak -e "s|^\(__author__ *=\).*|\1 '$(author)'|"    $(initfile)
	@sed -i .bak -e "s|^\(__email__ *=\).*|\1 '$(email)'|"	    $(initfile)
	@sed -i .bak -e "s|^\(__license__ *=\).*|\1 '$(license)'|"  $(initfile)

update-meta: vars
	@sed -i .bak -e "/version/ s/[0-9].[0-9][0-9]*.[0-9][0-9]*/$(version)/" codemeta.json

update-citation: vars
	$(eval date  := $(shell date "+%F"))
	@sed -i .bak -e "/^date-released/ s/[0-9][0-9-]*/$(date)/" CITATION.cff
	@sed -i .bak -e "/^version/ s/[0-9].[0-9][0-9]*.[0-9][0-9]*/$(version)/" CITATION.cff

edited := codemeta.json $(initfile) CITATION.cff

commit-updates: vars
	git add $(edited)
	git diff-index --quiet HEAD $(edited) || \
	    git commit -m"Update stored version number" $(edited)

release-on-github: | vars update-init update-meta update-citation commit-updates
	$(eval tmp_file  := $(shell mktemp /tmp/release-notes-$(name).XXXX))
	git push -v --all
	git push -v --tags
	$(info ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓)
	$(info ┃ Write release notes in the file that gets opened in your  ┃)
	$(info ┃ editor. Close the editor to complete the release process. ┃)
	$(info ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛)
	sleep 2
	$(EDITOR) $(tmp_file)
	gh release create v$(version) -t "Release $(version)" -F $(tmp_file)

print-instructions: vars
	$(info ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓)
	$(info ┃ Next steps:                                             ┃)
	$(info ┃ 1. Visit https://github.com/$(repo)/releases )
	$(info ┃ 2. Check the release                                    ┃)
	$(info ┃ 3. Wait a few seconds to let web services do their work ┃)
	$(info ┃ 4. Run "make update-doi" to update the DOI in README.md ┃)
	$(info ┃ 5. Run "make packages" and check the results            ┃)
	$(info ┃ 6. Run "make test-pypi" to push to test.pypi.org        ┃)
	$(info ┃ 7. Check https://test.pypi.org/$(repo) )
	$(info ┃ 8. Run "make pypi" to push to pypi for real             ┃)
	$(info ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛)
	@echo ""

update-doi: vars
	sed -i .bak -e 's|/api/record/[0-9]\{1,\}|/api/record/$(doi_tail)|' README.md
	sed -i .bak -e 's|edu/records/[0-9]\{1,\}|edu/records/$(doi_tail)|' README.md
	sed -i .bak -e '/doi:/ s|10.22002/[0-9]\{1,\}|10.22002/$(doi_tail)|' CITATION.cff
	git add README.md CITATION.cff
	git commit -m"Update DOI in README and CITATION.cff files" README.md CITATION.cff
	git push -v --all

packages: | vars clean
	python3 setup.py sdist bdist_wheel
	python3 -m twine check dist/$(name)-$(version).tar.gz
	python3 -m twine check dist/$(name)-$(version)-py3-none-any.whl

test-pypi: packages
	python3 -m twine upload --repository testpypi dist/$(name)-$(version)*.{whl,gz}

pypi: packages
	python3 -m twine upload dist/$(name)-$(version)*.{gz,whl}


# Cleanup and miscellaneous directives ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

clean: clean-dist clean-build clean-release clean-other

really-clean: clean really-clean-dist

clean-dist: vars
	-rm -fr dist/$(name) dist/$(name).zip dist/*.tar.gz dist/*.whl \
	dist/$(name)-${version}-macos-python3.*{,.zip}

really-clean-dist:;
	-rm -fr dist

clean-build:;
	-rm -rf build

clean-release: vars
	-rm -rf $(name).egg-info codemeta.json.bak $(initfile).bak README.md.bak

clean-other: vars
	-rm -fr __pycache__ $(name)/__pycache__ .eggs
	-rm -rf .cache

.PHONY: release release-on-github update-init update-meta \
	vars print-instructions update-doi packages test-pypi pypi clean \
	clean-dist really-clean-dist clean-build clean-release clean-other
