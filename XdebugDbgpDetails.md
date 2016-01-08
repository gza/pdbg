# Introduction #

Xdebug's support of DBGp is not complete. Some core commands and many extended commands are not supported. Others have bugs. This page details Xdebug's DBGp support.

## General Issues ##

  * How errors are handled is inconsistent (ie some set an attribute on response, some put a message in a node in response).
  * There is no way to know from typemap\_get which types can be set with property\_set.

## Core Commands ##

### stderr ###

This command is not supported at all. The implementation in the Xdebug source is just a hardcoded error response. (2.0.3)

### property\_get ###

This command does not return a dollar sign prefix on variable names, whereas context\_get does.

### property\_set ###

The implementation of this command sets the success attribute twice on an unsupported type. this causes lxml to puke an exception.

Cannot set a null value. (ie, you cannot pass null as a type).

### context\_get ###

When remote\_mode is jit, calling context\_get does not return any variables in context 0 (Locals). But it does return superglobal data.

## Extended Commands ##

### eval ###

Supported by Xdebug. When the resulting property value is an array, only the first dimension of the array is returned. (2.0.3)

### expr ###

Not supported (2.0.3)