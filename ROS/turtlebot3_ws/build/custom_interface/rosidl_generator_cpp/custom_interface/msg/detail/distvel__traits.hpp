// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from custom_interface:msg/Distvel.idl
// generated code does not contain a copyright notice

#ifndef CUSTOM_INTERFACE__MSG__DETAIL__DISTVEL__TRAITS_HPP_
#define CUSTOM_INTERFACE__MSG__DETAIL__DISTVEL__TRAITS_HPP_

#include "custom_interface/msg/detail/distvel__struct.hpp"
#include <stdint.h>
#include <rosidl_runtime_cpp/traits.hpp>
#include <sstream>
#include <string>
#include <type_traits>

namespace rosidl_generator_traits
{

inline void to_yaml(
  const custom_interface::msg::Distvel & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: distancia
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "distancia: ";
    value_to_yaml(msg.distancia, out);
    out << "\n";
  }

  // member: velocidad
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "velocidad: ";
    value_to_yaml(msg.velocidad, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const custom_interface::msg::Distvel & msg)
{
  std::ostringstream out;
  to_yaml(msg, out);
  return out.str();
}

template<>
inline const char * data_type<custom_interface::msg::Distvel>()
{
  return "custom_interface::msg::Distvel";
}

template<>
inline const char * name<custom_interface::msg::Distvel>()
{
  return "custom_interface/msg/Distvel";
}

template<>
struct has_fixed_size<custom_interface::msg::Distvel>
  : std::integral_constant<bool, true> {};

template<>
struct has_bounded_size<custom_interface::msg::Distvel>
  : std::integral_constant<bool, true> {};

template<>
struct is_message<custom_interface::msg::Distvel>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // CUSTOM_INTERFACE__MSG__DETAIL__DISTVEL__TRAITS_HPP_
