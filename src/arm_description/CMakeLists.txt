cmake_minimum_required(VERSION 3.8)
project(arm_description)

find_package(ament_cmake REQUIRED)

# Install all resource folders so ROS 2 can find them after build
install(DIRECTORY
  urdf
  meshes
  launch
  config
  scripts
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
