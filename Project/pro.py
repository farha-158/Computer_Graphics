# دالة لإنشاء مصفوفة دوران
def rotation_matrix(angle, axis, clockwise_positive=True):
    theta = math.radians(angle)  # تحويل الزاوية من درجات إلى راديان
    c = math.cos(theta)  # حساب جيب تمام الزاوية
    s = math.sin(theta)  # حساب جيب الزاوية

    s_pos = s if clockwise_positive else -s  # تحديد اتجاه الدوران الموجب
    s_neg = -s if clockwise_positive else s

    matrix = identity_matrix()  # إنشاء مصفوفة وحدة كأساس
    if axis == 'x':  # إذا كان الدوران حول المحور X
        matrix[1][1] = c
        matrix[1][2] = s_pos
        matrix[2][1] = s_neg
        matrix[2][2] = c
    elif axis == 'y':  # إذا كان الدوران حول المحور Y
        matrix[0][0] = c
        matrix[0][2] = s_neg
        matrix[2][0] = s_pos
        matrix[2][2] = c
    elif axis == 'z':  # إذا كان الدوران حول المحور Z
        matrix[0][0] = c
        matrix[0][1] = s_pos
        matrix[1][0] = s_neg
        matrix[1][1] = c

    return matrix  # إعادة مصفوفة الدوران

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




def apply_3d_shear(vertices, sh_xy=0.0, sh_xz=0.0, sh_yx=0.0, sh_yz=0.0, sh_zx=0.0, sh_zy=0.0):
    sheared_vertices = []  # قائمة لتخزين الرؤوس المشوهة
    for x, y, z in vertices:  # التكرار عبر جميع الرؤوس
        new_x = x + sh_yx * y + sh_zx * z  # حساب الإحداثي X بعد التشويه
        new_y = y + sh_xy * x + sh_zy * z  # حساب الإحداثي Y بعد التشويه
        new_z = z + sh_xz * x + sh_yz * y  # حساب الإحداثي Z بعد التشويه
        sheared_vertices.append([new_x, new_y, new_z])  # إضافة الرأس الجديد إلى القائمة
    return sheared_vertices  # إعادة الرؤوس المشوهة




