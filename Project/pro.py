

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
