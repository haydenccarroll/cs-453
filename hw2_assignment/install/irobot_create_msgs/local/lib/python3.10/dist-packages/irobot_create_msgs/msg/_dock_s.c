// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from irobot_create_msgs:msg/Dock.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "irobot_create_msgs/msg/detail/dock__struct.h"
#include "irobot_create_msgs/msg/detail/dock__functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool irobot_create_msgs__msg__dock__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[34];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("irobot_create_msgs.msg._dock.Dock", full_classname_dest, 33) == 0);
  }
  irobot_create_msgs__msg__Dock * ros_message = _ros_message;
  {  // header
    PyObject * field = PyObject_GetAttrString(_pymsg, "header");
    if (!field) {
      return false;
    }
    if (!std_msgs__msg__header__convert_from_py(field, &ros_message->header)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // dock_visible
    PyObject * field = PyObject_GetAttrString(_pymsg, "dock_visible");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->dock_visible = (Py_True == field);
    Py_DECREF(field);
  }
  {  // is_docked
    PyObject * field = PyObject_GetAttrString(_pymsg, "is_docked");
    if (!field) {
      return false;
    }
    assert(PyBool_Check(field));
    ros_message->is_docked = (Py_True == field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * irobot_create_msgs__msg__dock__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of Dock */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("irobot_create_msgs.msg._dock");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "Dock");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  irobot_create_msgs__msg__Dock * ros_message = (irobot_create_msgs__msg__Dock *)raw_ros_message;
  {  // header
    PyObject * field = NULL;
    field = std_msgs__msg__header__convert_to_py(&ros_message->header);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "header", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // dock_visible
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->dock_visible ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "dock_visible", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // is_docked
    PyObject * field = NULL;
    field = PyBool_FromLong(ros_message->is_docked ? 1 : 0);
    {
      int rc = PyObject_SetAttrString(_pymessage, "is_docked", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
