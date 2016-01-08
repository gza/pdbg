# Project TODO #

  * Watch panel; see the value of variables in the current stack frame.
  * Restrict the number of lines in the log textview.

# Feature Ideas #

These features might not be added.  Yet they just might ...

## Interesting Ways to Get Source Files ##

DBGp does not have a command to get "all the source". So more interesting methods must be used to allow the user to get their source files.

  * Clicking on an include 'BLAH' in the source view widget requests the file. This would require knowing the include path. Xdebug supports eval, which could be used to break apart the return of get\_include\_path.  This would make the app PHP specific.
  * A simple script could be written that indexes a project's source files.  The output of this script could be imported into pDBG to populate the Known URIs list.