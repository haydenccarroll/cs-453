// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from irobot_create_msgs:msg/Dock.idl
// generated code does not contain a copyright notice

#ifndef IROBOT_CREATE_MSGS__MSG__DETAIL__DOCK__STRUCT_H_
#define IROBOT_CREATE_MSGS__MSG__DETAIL__DOCK__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"

/// Struct defined in msg/Dock in the package irobot_create_msgs.
/**
  * This message contains information about whether the robot is docked or sees the dock in its sensors.
 */
typedef struct irobot_create_msgs__msg__Dock
{
  /// Header stamp is when dock info was queried.
  std_msgs__msg__Header header;
  /// Whether robot sees dock in its sensors used for docking
  bool dock_visible;
  /// Whether the robot is docked
  bool is_docked;
} irobot_create_msgs__msg__Dock;

// Struct for a sequence of irobot_create_msgs__msg__Dock.
typedef struct irobot_create_msgs__msg__Dock__Sequence
{
  irobot_create_msgs__msg__Dock * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} irobot_create_msgs__msg__Dock__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // IROBOT_CREATE_MSGS__MSG__DETAIL__DOCK__STRUCT_H_
