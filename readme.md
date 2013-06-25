Build with input
================

A plugin for sublime text 2/3 which allows build systems to run scripts that accept input. 

## Introduction

For instance, with the following file

![](https://raw.github.com/eric-wieser/build-with-input/screenshots/first.png)

Push <kbd>ctrl</kbd> + <kbd>b</kbd>. Without this plugin, you would get an `EOFError`. Instead, the build output window appears, waiting for input.

![](https://raw.github.com/eric-wieser/build-with-input/screenshots/second.png)

To give it input, click on it and push <kbd>F12</kbd>. An input box appears.

![](https://raw.github.com/eric-wieser/build-with-input/screenshots/third.png)

Upon pushing <kbd>enter</kbd> after typing your input, or <kbd>esc</kbd> to abort, you're returned back to the build output, ready to give more input.

![](https://raw.github.com/eric-wieser/build-with-input/screenshots/fourth.png)

![](https://raw.github.com/eric-wieser/build-with-input/screenshots/fifth.png)

It is currently not possible for sublime text to show both the input and output window at the same time.

## Install

For __ST2__, simply clone the repository to your `Packages` directory.

For __ST3__, do the same and checkout to ST3 branch.

## Notes

This plugin works by monkey-patching the code of the original `exec.py` file. Often this fails to happen correctly on startup. As a temporary workaround, you can force sublimetext to reload `exec_patcher.py` by opening, editing and resaving it.

Original repository can be found [here](https://github.com/eric-wieser/build-with-input).
