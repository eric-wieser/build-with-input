Build with input
================

A plugin for sublime text which allows build systems to run scripts that accept input. For instance, with the following file

![](https://raw.github.com/eric-wieser/build-with-input/screenshots/first.png)

Push <kbd>ctrl</kbd> + <kbd>b</kbd>. Without this plugin, you would get an `EOFError`. Instead, the build output window appears, waiting for input.

![](https://raw.github.com/eric-wieser/build-with-input/screenshots/second.png)

To give it input, click on it and push <kbd>enter</kbd>. An input box appears.

![](https://raw.github.com/eric-wieser/build-with-input/screenshots/third.png)

Upon pushing <kbd>enter</kbd> after typing your input, or <kbd>esc</kbd> to abort, you're returned back to the build output, ready to give more input.

![](https://raw.github.com/eric-wieser/build-with-input/screenshots/fourth.png)

![](https://raw.github.com/eric-wieser/build-with-input/screenshots/fifth.png)

It is currently not possible for sublime text to show both the input and output window at the same time.

---

This plugin works by monkey-patching the code of the original `exec.py` file. Often this fails to happen correctly on startup. As a temporary workaround, you can force sublimetext to reload `exec_patcher.py` by opening, editing and resaving it.