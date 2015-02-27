# Sublime3-pydoc
Sublime 3 Pydoc plugin. This plugin autocompletes Docstrings if using python function definitions.

# Description

DocPy autocompletes a docstring for any python function definition and inserts default arguments which can then be replaced.

# Installation

Either way install it using Package Control or download it.

## Package Control

Open the install dialog pressing <kbd>Ctrl</kbd><kbd>Shift</kbd><kbd>P</kbd> and type in "Install Package" and then <kbd>Enter</kbd>

## Manual Install

Download the package unzip the package files into the sublime directory: 

~/.config/sublime-text-3/Packages/DocPy

# Completion

Currently only function completion is currently available.

To activate the completion just right after ( or near ) any function definition type in the leading ''' or """ and then simply press <kbd>Enter</kbd>

The default behaviour is that the given arguments will be written out with a placeholder when autocompleting.

![](https://raw.github.com/richermans/Sublime3-pydoc/master/imgs/autocomplete_empty.gif)

Autocompletion also works with default parameters, which prints out the default value.

![](https://raw.github.com/richermans/Sublime3-pydoc/master/imgs/autocomplete_default.gif)

