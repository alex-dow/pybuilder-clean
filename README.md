PyBuilder PrettySetup Plugin
============================

What is it?
-----------

The first thing I noticed when I started using PyBuilder, was that the generated setup.py was poorly formatted

This plugin aims to fix that by exposing a new task called "prettySetup", which you can then use after your publish task to create a new, nicer looking setup.py file.

I do plan to offer a patch to PyBuilder to apply to the core distutils plugin, but if they choose not to use it, at least this is still here.

Usuage
------

pyb prettySetup
