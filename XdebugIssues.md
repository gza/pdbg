The following bugs/issues exist in Xdebug:

  * the property\_set implementation sets the success attribute twice on unsupported type. this causes lxml to puke an exception.
  * there is no way to know which types from typemap\_get can be set in property\_set.
  * stderr is not implemented.
  * how errors are handled is inconsistent (ie some set an attribute on response, some put a message in a node in response).
  * property\_get does not return a dollar sign in the name attribute, whereas context\_get does.