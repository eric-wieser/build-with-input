Build with input
================

A plugin for sublime text which allows build systems to run scripts that accept input. For instance, with the following file

```python
first = raw_input('first name: ')
last = raw_input('last name: ')
print "Hello, %s %s" % (first, last)
```

Push <kbd>ctrl + b</kbd>. Without this plugin, you would get an `EOFError`. Instead, the build output window appears, waiting for input. To give it input, click on it and push <kbd>enter</kbd>. An input box appears. Upon pushing enter or esc, you're returned back to the build output.

It is currently not possible for sublime text to show both the input and output window at the same time.