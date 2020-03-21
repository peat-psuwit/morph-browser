add_subdirectory(autopilot)
add_subdirectory(unittests)

# ToDo: move to different targets / folders
file(GLOB_RECURSE TESTS_NONCOMPILED *.py *.qml)
add_custom_target(tests-noncompiled ALL SOURCES ${TESTS_NONCOMPILED})
