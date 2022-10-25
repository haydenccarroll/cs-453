// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from irobot_create_msgs:action/DockServo.idl
// generated code does not contain a copyright notice

#ifndef IROBOT_CREATE_MSGS__ACTION__DETAIL__DOCK_SERVO__STRUCT_H_
#define IROBOT_CREATE_MSGS__ACTION__DETAIL__DOCK_SERVO__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

/// Struct defined in action/DockServo in the package irobot_create_msgs.
typedef struct irobot_create_msgs__action__DockServo_Goal
{
  uint8_t structure_needs_at_least_one_member;
} irobot_create_msgs__action__DockServo_Goal;

// Struct for a sequence of irobot_create_msgs__action__DockServo_Goal.
typedef struct irobot_create_msgs__action__DockServo_Goal__Sequence
{
  irobot_create_msgs__action__DockServo_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} irobot_create_msgs__action__DockServo_Goal__Sequence;


// Constants defined in the message

/// Struct defined in action/DockServo in the package irobot_create_msgs.
typedef struct irobot_create_msgs__action__DockServo_Result
{
  bool is_docked;
} irobot_create_msgs__action__DockServo_Result;

// Struct for a sequence of irobot_create_msgs__action__DockServo_Result.
typedef struct irobot_create_msgs__action__DockServo_Result__Sequence
{
  irobot_create_msgs__action__DockServo_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} irobot_create_msgs__action__DockServo_Result__Sequence;


// Constants defined in the message

/// Struct defined in action/DockServo in the package irobot_create_msgs.
typedef struct irobot_create_msgs__action__DockServo_Feedback
{
  bool sees_dock;
} irobot_create_msgs__action__DockServo_Feedback;

// Struct for a sequence of irobot_create_msgs__action__DockServo_Feedback.
typedef struct irobot_create_msgs__action__DockServo_Feedback__Sequence
{
  irobot_create_msgs__action__DockServo_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} irobot_create_msgs__action__DockServo_Feedback__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "irobot_create_msgs/action/detail/dock_servo__struct.h"

/// Struct defined in action/DockServo in the package irobot_create_msgs.
typedef struct irobot_create_msgs__action__DockServo_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  irobot_create_msgs__action__DockServo_Goal goal;
} irobot_create_msgs__action__DockServo_SendGoal_Request;

// Struct for a sequence of irobot_create_msgs__action__DockServo_SendGoal_Request.
typedef struct irobot_create_msgs__action__DockServo_SendGoal_Request__Sequence
{
  irobot_create_msgs__action__DockServo_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} irobot_create_msgs__action__DockServo_SendGoal_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/DockServo in the package irobot_create_msgs.
typedef struct irobot_create_msgs__action__DockServo_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} irobot_create_msgs__action__DockServo_SendGoal_Response;

// Struct for a sequence of irobot_create_msgs__action__DockServo_SendGoal_Response.
typedef struct irobot_create_msgs__action__DockServo_SendGoal_Response__Sequence
{
  irobot_create_msgs__action__DockServo_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} irobot_create_msgs__action__DockServo_SendGoal_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/DockServo in the package irobot_create_msgs.
typedef struct irobot_create_msgs__action__DockServo_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} irobot_create_msgs__action__DockServo_GetResult_Request;

// Struct for a sequence of irobot_create_msgs__action__DockServo_GetResult_Request.
typedef struct irobot_create_msgs__action__DockServo_GetResult_Request__Sequence
{
  irobot_create_msgs__action__DockServo_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} irobot_create_msgs__action__DockServo_GetResult_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "irobot_create_msgs/action/detail/dock_servo__struct.h"

/// Struct defined in action/DockServo in the package irobot_create_msgs.
typedef struct irobot_create_msgs__action__DockServo_GetResult_Response
{
  int8_t status;
  irobot_create_msgs__action__DockServo_Result result;
} irobot_create_msgs__action__DockServo_GetResult_Response;

// Struct for a sequence of irobot_create_msgs__action__DockServo_GetResult_Response.
typedef struct irobot_create_msgs__action__DockServo_GetResult_Response__Sequence
{
  irobot_create_msgs__action__DockServo_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} irobot_create_msgs__action__DockServo_GetResult_Response__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "irobot_create_msgs/action/detail/dock_servo__struct.h"

/// Struct defined in action/DockServo in the package irobot_create_msgs.
typedef struct irobot_create_msgs__action__DockServo_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  irobot_create_msgs__action__DockServo_Feedback feedback;
} irobot_create_msgs__action__DockServo_FeedbackMessage;

// Struct for a sequence of irobot_create_msgs__action__DockServo_FeedbackMessage.
typedef struct irobot_create_msgs__action__DockServo_FeedbackMessage__Sequence
{
  irobot_create_msgs__action__DockServo_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} irobot_create_msgs__action__DockServo_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // IROBOT_CREATE_MSGS__ACTION__DETAIL__DOCK_SERVO__STRUCT_H_
