def reflection(translation, reflection_axis=None):
    transformation_matrix = identity_matrix()  

    transformation_matrix = custom_translate(transformation_matrix, translation)

    if reflection_axis:
        reflection_matrix = identity_matrix()
        if reflection_axis == "x":
            reflection_matrix[0][0] = -1  # انعكاس حول المحور X
        elif reflection_axis == "y":
            reflection_matrix[1][1] = -1  # انعكاس حول المحور Y
        elif reflection_axis == "z":
            reflection_matrix[2][2] = -1  # انعكاس حول المحور Z
        transformation_matrix = np.dot(transformation_matrix, reflection_matrix)  

    return transformation_matrix

# دالة لتكبير أو تصغير النقاط بنفس ال scale
def scale_points(points, scale_factor):
  
    scaled_points = []

    for point in points:
        # تطبيق الـ scaling على كل نقطة
        scaled_point = [coord * scale_factor for coord in point]
        scaled_points.append(scaled_point)

    return scaled_points


# تقوم بتكبير أو تصغير النقاط بناءً على عوامل مختلفة لكل من المحاور x و y و z.
def scale_points_individual(points, scale_x, scale_y, scale_z):    
   
    scaled_points = []

    for point in points:
        # تطبيق الـ scaling لكل محور على حدة
        scaled_point = [
            point[0] * scale_x,  # تطبيق scaling على محور x
            point[1] * scale_y,  # تطبيق scaling على محور y
            point[2] * scale_z   # تطبيق scaling على محور z
        ]
        scaled_points.append(scaled_point)

    return scaled_points
