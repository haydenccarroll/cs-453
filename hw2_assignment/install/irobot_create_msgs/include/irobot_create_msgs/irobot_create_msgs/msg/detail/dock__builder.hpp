// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from irobot_create_msgs:msg/Dock.idl
// generated code does not contain a copyright notice

#ifndef IROBOT_CREATE_MSGS__MSG__DETAIL__DOCK__BUILDER_HPP_
#define IROBOT_CREATE_MSGS__MSG__DETAIL__DOCK__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "irobot_create_msgs/msg/detail/dock__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace irobot_create_msgs
{

namespace msg
{

namespace builder
{

class Init_Dock_is_docked
{
public:
  explicit Init_Dock_is_docked(::irobot_create_msgs::msg::Dock & msg)
  : msg_(msg)
  {}
  ::irobot_create_msgs::msg::Dock is_docked(::irobot_create_msgs::msg::Dock::_is_docked_type arg)
  {
    msg_.is_docked = std::move(arg);
    return std::move(msg_);
  }

private:
  ::irobot_create_msgs::msg::Dock msg_;
};

class Init_Dock_dock_visible
{
public:
  explicit Init_Dock_dock_visible(::irobot_create_msgs::msg::Dock & msg)
  : msg_(msg)
  {}
  Init_Dock_is_docked dock_visible(::irobot_create_msgs::msg::Dock::_dock_visible_type arg)
  {
    msg_.dock_visible = std::move(arg);
    return Init_Dock_is_docked(msg_);
  }

private:
  ::irobot_create_msgs::msg::Dock msg_;
};

class Init_Dock_header
{
public:
  Init_Dock_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Dock_dock_visible header(::irobot_create_msgs::msg::Dock::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_Dock_dock_visible(msg_);
  }

private:
  ::irobot_create_msgs::msg::Dock msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::irobot_create_msgs::msg::Dock>()
{
  return irobot_create_msgs::msg::builder::Init_Dock_header();
}

}  // namespace irobot_create_msgs

#endif  // IROBOT_CREATE_MSGS__MSG__DETAIL__DOCK__BUILDER_HPP_
