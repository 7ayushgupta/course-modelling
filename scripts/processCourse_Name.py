def buildCourse_Name(course_name_raw):
  course_name_ = "missing"
  if (course_name_raw.lower() == "generic" or course_name_raw.lower() == "false"):
    course_name_ = "missing"
  else:
    course_name_ = course_name_raw.lower()
  return course_name_
