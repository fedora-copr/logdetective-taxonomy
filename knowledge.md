# Resolving RPM build problems

LogDetective helps you understand why your RPM build failed using the build
log. It analyzes logs using a Large Language Model (LLM) and Drain template
miner. Based on your input log, LogDetective will explain why the build failed
and will suggest a solution.

LogDetective team is building a data set with annotated logs of failures that
will help us produce high quality suggestions that target Fedora, CentOS Stream
and Red Hat Enterprise Linux ecosystems.

Here is an example of an error from the RPM build process:
```
No matching package to install: 'go-vendor-tools'
Not all dependencies satisfied
Error: Some packages could not be found
```

This snippet contains the error message: that the go-vendor-tools package could
not be installed.
In order to fix this, double check the package name. Make sure to build
go-vendor-tools first if it is a dependency of the current package.

Here is another example of an error from the RPM build process:
```
error: Couldn't download https://github.com/hyprwm/${name}/archive/v0.2.0/hyprlock-0.2.0.tar.
```

The reason the build failed, there is a typo in the `%{name}` macro. It is
incorrectly spelled as `${name}`.
