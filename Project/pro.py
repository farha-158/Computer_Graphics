import pygame  # استيراد مكتبة pygame للتعامل مع واجهة المستخدم الرسومية
from pygame.locals import *  # استيراد الثوابت والوظائف من pygame
from OpenGL.GL import *  # استيراد وظائف OpenGL للرسم ثلاثي الأبعاد
from OpenGL.GLU import *  # استيراد وظائف OpenGL الإضافية مثل المنظور
import numpy as np  # استيراد مكتبة numpy للتعامل مع المصفوفات
import math  # استيراد مكتبة math لإجراء العمليات الرياضية

# تعريف رؤوس المكعب في الفضاء ثلاثي الأبعاد
vertices = [
    [1, 1, -1],  # الرأس الأول
    [1, -1, -1],  # الرأس الثاني
    [-1, -1, -1],  # الرأس الثالث
    [-1, 1, -1],  # الرأس الرابع
    [1, 1, 1],  # الرأس الخامس
    [1, -1, 1],  # الرأس السادس
    [-1, -1, 1],  # الرأس السابع
    [-1, 1, 1],  # الرأس الثامن
]

# تعريف الحواف التي تربط بين الرؤوس
edges = [
    (0, 1), (1, 2), (2, 3), (3, 0),  # حواف الوجه الخلفي
    (4, 5), (5, 6), (6, 7), (7, 4),  # حواف الوجه الأمامي
    (0, 4), (1, 5), (2, 6), (3, 7)   # حواف تصل بين الوجه الأمامي والخلفي
]

# دالة لرسم المكعب باستخدام OpenGL
def draw_cube(scaled_vertices):
    glBegin(GL_LINES)  # بدء رسم الخطوط
    for edge in edges:  # التكرار عبر جميع الحواف
        for vertex in edge:  # لكل رأس في الحافة
            glVertex3fv(scaled_vertices[vertex])  # تحديد موقع الرأس
    glEnd()  # إنهاء رسم الخطوط

# دالة لإنشاء مصفوفة وحدة (4x4)
def identity_matrix():
    return np.identity(4, dtype=np.float32)  # مصفوفة وحدة بأبعاد 4x4

# دالة لإنشاء مصفوفة دوران
def rotation_matrix(angle, axis):
    theta = math.radians(angle)  # تحويل الزاوية من درجات إلى راديان
    cos = math.cos(theta)  # حساب جيب تمام الزاوية
    sin = math.sin(theta)  # حساب جيب الزاوية

    matrix = identity_matrix()  # إنشاء مصفوفة وحدة كأساس
    if axis == 'x':  # إذا كان الدوران حول المحور X
        matrix[1][1] = cos
        matrix[1][2] = -sin
        matrix[2][1] = sin
        matrix[2][2] = cos
    elif axis == 'y':  # إذا كان الدوران حول المحور Y
        matrix[0][0] = cos
        matrix[0][2] = sin
        matrix[2][0] = -sin
        matrix[2][2] = cos
    elif axis == 'z':  # إذا كان الدوران حول المحور Z
        matrix[0][0] = cos
        matrix[0][1] = -sin
        matrix[1][0] = sin
        matrix[1][1] = cos

    return matrix  # إعادة مصفوفة الدوران

# دالة لتطبيق التشويه ثلاثي الأبعاد على الرؤوس
def apply_3d_shear(vertices, sh_xy=0.0, sh_xz=0.0, sh_yx=0.0, sh_yz=0.0, sh_zx=0.0, sh_zy=0.0):
    sheared_vertices = []  # قائمة لتخزين الرؤوس المشوهة
    for x, y, z in vertices:  # التكرار عبر جميع الرؤوس
        new_x = x + sh_yx * y + sh_zx * z  # حساب الإحداثي X بعد التشويه
        new_y = y + sh_xy * x + sh_zy * z  # حساب الإحداثي Y بعد التشويه
        new_z = z + sh_xz * x + sh_yz * y  # حساب الإحداثي Z بعد التشويه
        sheared_vertices.append([new_x, new_y, new_z])  # إضافة الرأس الجديد إلى القائمة
    return sheared_vertices  # إعادة الرؤوس المشوهة

# دالة لتكبير أو تصغير النقاط
def scale_points(points, scale_factor):
    scaled_points = []  # قائمة لتخزين النقاط المكبرة/المصغرة
    for point in points:  # التكرار عبر جميع النقاط
        scaled_point = [coord * scale_factor for coord in point]  # ضرب الإحداثيات في عامل التكبير/التصغير
        scaled_points.append(scaled_point)  # إضافة النقطة الجديدة إلى القائمة
        
    return scaled_points  # إعادة النقاط المكبرة/المصغرة

# def scale_points_individual(points, scale_x, scale_y, scale_z):    
   
#     scaled_points = []

#     for point in points:
#         # تطبيق الـ scaling لكل محور على حدة
#         scaled_point = [
#             point[0] * scale_x,  # تطبيق scaling على محور x
#             point[1] * scale_y,  # تطبيق scaling على محور y
#             point[2] * scale_z   # تطبيق scaling على محور z
#         ]
#         scaled_points.append(scaled_point)

#     return scaled_points

# دالة لتحريك الكائن في الفضاء ثلاثي الأبعاد
def custom_translate(matrix, translation):
    translation_matrix = identity_matrix()  # إنشاء مصفوفة وحدة كأساس للترجمة
    translation_matrix[0][3] = translation[0]  # تعديل قيمة الترجمة على المحور X
    translation_matrix[1][3] = translation[1]  # تعديل قيمة الترجمة على المحور Y
    translation_matrix[2][3] = translation[2]  # تعديل قيمة الترجمة على المحور Z
    return np.dot(matrix, translation_matrix)  # دمج مصفوفة الترجمة مع المصفوفة الأصلية


# دالة لتطبيق الانعكاس
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

# دالة لتطبيق التحويلات على المكعب
def transform_cube(scale, angles, translation, shear_values, reflection_axis):
    global vertices  # استخدام متغير الرؤوس العام

    # تغيير حجم الرؤوس
    scaled_vertices = scale_points(vertices, scale[0])

    # تطبيق التشويه
    sheared_vertices = apply_3d_shear(
        scaled_vertices,
        sh_xy=shear_values.get('xy', 0.0),
        sh_xz=shear_values.get('xz', 0.0),
        sh_yx=shear_values.get('yx', 0.0),
        sh_yz=shear_values.get('yz', 0.0),
        sh_zx=shear_values.get('zx', 0.0),
        sh_zy=shear_values.get('zy', 0.0)
    )

    transformation_matrix = identity_matrix()  # إنشاء مصفوفة وحدة كأساس للتحويلات

    # تطبيق الترجمة
    transformation_matrix = custom_translate(transformation_matrix, translation)

    # تطبيق الانعكاس إذا تم تحديد محور
    transformation_matrix = reflection(translation, reflection_axis)
    # تطبيق الدوران حول المحاور المحددة
    for angle, axis in zip(angles, ['x', 'y', 'z']):
        rotation_matrix_ = rotation_matrix(angle, axis)  # إنشاء مصفوفة الدوران
        transformation_matrix = np.dot(transformation_matrix, rotation_matrix_)  # دمج مصفوفة الدوران

    # تحميل مصفوفة التحويل إلى OpenGL
    glLoadMatrixf(transformation_matrix.T)  # تمرير المصفوفة إلى OpenGL (منقولة)

    # رسم المكعب بعد التحويلات
    draw_cube(sheared_vertices)

# الحلقة الرئيسية للبرنامج
def main():
    pygame.init()  # تهيئة مكتبة pygame
    display = (800, 600)  # إعداد أبعاد نافذة العرض
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)  # إنشاء نافذة باستخدام OpenGL
    
    # إعداد الإسقاط المنظوري لتحديد زاوية العرض
    gluPerspective(30, (display[0] / display[1]), 0.1, 100.0)
    
    # تحريك الكاميرا للخلف على المحور Z لعرض المكعب
    glTranslatef(0.0, 0.0, -20)

    # إعدادات البداية للمكعب
    scale = [0.5, 0.5, 0.5]  # حجم المكعب (تكبير/تصغير)
    angles = [30, 30, 0]  # زوايا الدوران حول المحاور X و Y و Z
    translation = [0, 0, 0]  # الإزاحة الأولية للمكعب
    shear_values = {'xy': 0.0, 'xz': 0.0, 'yx': 0.0, 'yz': 0.0, 'zx': 0.0, 'zy': 0.0}  # قيم التشويه
    reflection_axis = None  # إعداد محوري افتراضي للانعكاس، لا يتم استخدامه افتراضيًا

    running = True
    while running:  # حلقة التشغيل الرئيسية
        for event in pygame.event.get():  # التعامل مع أحداث pygame
            if event.type == pygame.QUIT:  # إذا تم إغلاق النافذة
                running = False  # إنهاء الحلقة

        keys = pygame.key.get_pressed()  # الحصول على حالة المفاتيح المضغوطة

        # التحكم في الدوران
        if keys[pygame.K_LEFT]:  # إذا تم الضغط على السهم الأيسر
            angles[1] += 1  # زيادة زاوية الدوران حول المحور Y
        if keys[pygame.K_RIGHT]:  # إذا تم الضغط على السهم الأيمن
            angles[1] -= 1  # تقليل زاوية الدوران حول المحور Y
        if keys[pygame.K_UP]:  # إذا تم الضغط على السهم العلوي
            angles[0] += 1  # زيادة زاوية الدوران حول المحور X
        if keys[pygame.K_DOWN]:  # إذا تم الضغط على السهم السفلي
            angles[0] -= 1  # تقليل زاوية الدوران حول المحور X
        if keys[pygame.K_COMMA]:  # إذا تم الضغط على زر الفاصلة
            angles[2] += 1  # زيادة زاوية الدوران حول المحور Z
        if keys[pygame.K_PERIOD]:  # إذا تم الضغط على زر النقطة
            angles[2] -= 1  # تقليل زاوية الدوران حول المحور Z

        # التحكم في الحجم
        if keys[pygame.K_i]:  # إذا تم الضغط على زر "I"
            scale = [s + 0.01 for s in scale]  # زيادة الحجم على جميع المحاور
        if keys[pygame.K_k]:  # إذا تم الضغط على زر "K"
            scale = [max(0.1, s - 0.01) for s in scale]  # تقليل الحجم مع الحفاظ على الحد الأدنى
        if keys[pygame.K_u]:  # إذا تم الضغط على زر "U"
            scale[2] += 0.01  # زيادة الحجم على المحور Z فقط
        if keys[pygame.K_j]:  # إذا تم الضغط على زر "J"
            scale[2] = max(0.1, scale[2] - 0.01)  # تقليل الحجم على المحور Z مع الحفاظ على الحد الأدنى

        # التحكم في الترجمة
        if keys[pygame.K_a]:  # إذا تم الضغط على زر "A"
            translation[0] -= 0.1  # تحريك الكائن على المحور X بالسالب
        if keys[pygame.K_d]:  # إذا تم الضغط على زر "D"
            translation[0] += 0.1  # تحريك الكائن على المحور X بالموجب
        if keys[pygame.K_w]:  # إذا تم الضغط على زر "W"
            translation[1] += 0.1  # تحريك الكائن على المحور Y بالموجب
        if keys[pygame.K_s]:  # إذا تم الضغط على زر "S"
            translation[1] -= 0.1  # تحريك الكائن على المحور Y بالسالب
        if keys[pygame.K_q]:  # إذا تم الضغط على زر "Q"
            translation[2] += 0.1  # تحريك الكائن للأمام (على المحور Z)
        if keys[pygame.K_e]:  # إذا تم الضغط على زر "E"
            translation[2] -= 0.1  # تحريك الكائن للخلف (على المحور Z)

        # التحكم بالتشويه
            # XY
        if keys[pygame.K_r]:
            shear_values['xy'] += 0.01
        if keys[pygame.K_f]:
            shear_values['xy'] -= 0.01
            # XZ
        if keys[pygame.K_t]:
            shear_values['xz'] += 0.01
        if keys[pygame.K_g]:
            shear_values['xz'] -= 0.01
            # YZ
        if keys[pygame.K_y]:
            shear_values['yz'] += 0.01
        if keys[pygame.K_h]:
            shear_values['yz'] -= 0.01
            # YX
        if keys[pygame.K_m]:
            shear_values['yx'] += 0.01
        if keys[pygame.K_n]:
            shear_values['yx'] -= 0.01
            # ZX
        if keys[pygame.K_b]:
            shear_values['zx'] += 0.01
        if keys[pygame.K_v]:
            shear_values['zx'] -= 0.01
            # ZY
        if keys[pygame.K_o]:
            shear_values['zy'] += 0.01
        if keys[pygame.K_l]:
            shear_values['zy'] -= 0.01



        # التحكم في الانعكاس
        if keys[pygame.K_x]:  # إذا تم الضغط على زر "X"
            reflection_axis = "x"  # تحديد الانعكاس على المحور X
        elif keys[pygame.K_c]:  # إذا تم الضغط على زر "Y"
            reflection_axis = "y"  # تحديد الانعكاس على المحور Y
        elif keys[pygame.K_z]:  # إذا تم الضغط على زر "Z"
            reflection_axis = "z"  # تحديد الانعكاس على المحور Z
        else:
            reflection_axis = None  # لا تحديد الانعكاس 
        # تحديث الشاشة
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # مسح الشاشة لتحضيرها للإطار التالي
        transform_cube(scale, angles, translation, shear_values, reflection_axis)  # تطبيق التحويلات على المكعب
        pygame.display.flip()  # تحديث عرض الشاشة
        pygame.time.wait(10)  # تأخير بسيط لزيادة الاستجابة

    pygame.quit()  # إنهاء مكتبة pygame عند الخروج من الحلقة
if __name__ == "__main__":
    main()  # استدعاء الدالة الرئيسية لتشغيل البرنامج
