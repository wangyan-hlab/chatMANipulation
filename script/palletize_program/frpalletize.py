import numpy as np
from frmovewrapper.frmove import FRCobot
from frmovewrapper.robotmath import euler_to_homomat, euler_from_homomat


class FRPalletize(object):
    """
        A Palletization template

        Author: wangyan
        Date: 2023/05/25
    """

    def __init__(self, params) -> None:

        self.rbt = FRCobot()
        # 读取参数配置
        self.params = params


    def get_target_point(self, box_point, p_pallet_origin, suction_point):
        """
            获得机器人坐标系下的目标吸取点
        """
        [x, y, z] = box_point
        tran_pallet_to_robot = euler_to_homomat(p_pallet_origin)  # 原点和第一个箱子几何中心重合
        tran_suction_to_box = np.linalg.inv(tran_pallet_to_robot) @ euler_to_homomat(suction_point)
        tran_box_to_pallet = euler_to_homomat([x,y,z,0,0,0])
        target_point_homomat = tran_pallet_to_robot @ tran_box_to_pallet @ tran_suction_to_box
        target_point = euler_from_homomat(target_point_homomat)
        
        return target_point


    def robot_motion(self, robot, point, motion_type):

        if motion_type == 'ptp':
            robot.MoveJ(point, target_flag='desc')
        elif motion_type == 'line':
            robot.MoveL(point, target_flag='desc')
        else:
            raise ValueError("无效的机械臂运动方式,必须是'ptp'或'line'")


    def execute_palletize(self):

        # 工件参数
        box_length = self.params['工件配置']['长度']
        box_width = self.params['工件配置']['宽度']
        box_height = self.params['工件配置']['高度']
        suction_point = self.params['工件配置']['吸盘位置']

        # 托盘参数
        pallet_length = self.params['托盘配置']['前边长度']
        pallet_width = self.params['托盘配置']['侧边长度']
        pallet_height = self.params['托盘配置']['高度']
        p_trans = self.params['托盘配置']['工位过渡点']

        # 模式参数
        box_interval = self.params['模式配置']['工件间隔']
        nrow = self.params['模式配置']['每层行数']
        ncol = self.params['模式配置']['每层列数']
        nlayer = self.params['模式配置']['码垛层数']

        # 机械臂移动参数
        p_home = self.params['机器人移动配置']['作业原点']
        p_path_1 = self.params['机器人移动配置']['路径点1']
        first_corner = self.params['机器人移动配置']['起始方位']
        move_direction = self.params['机器人移动配置']['移动方向']
        motion = self.params['机器人移动配置']['运动方式']
        pattern = self.params['机器人移动配置']['运动路径']
        work_direction = self.params['机器人移动配置']['堆叠方式']
        
        # 数据预检查
        if (nrow*box_width > pallet_width):
            raise ValueError("[Warning] 工件超出托盘侧边范围!")
        if (ncol*box_length > pallet_length):
            raise ValueError("[Warning] 工件超出托盘前边范围!")

        # 计算工件在托盘上的访问位置和顺序
        box_points = []
        # 选择堆叠方式: 码垛--load / 卸垛--unload
        if work_direction == 'load':
            start_layer, end_layer, step_layer = 0, nlayer, 1
        elif work_direction == 'unload':
            start_layer, end_layer, step_layer = nlayer-1, -1, -1
        else:
            raise ValueError("无效的堆叠方式")

        for layer in range(start_layer, end_layer, step_layer):
            # 计算当前层高度
            z = layer * box_height
            # 16 situations: 4 corners x 2 move_directions x 2 patterns
            # 选择起始方位,方位代表的位置如下图所示: [0,0] / [0,1] / [1,0] / [1,1]
            # ==================
            # |[0,0]      [0,1]|
            # |                |
            # |                |
            # |                |
            # |[1,0]      [1,1]|
            # ==================
            if first_corner == [0,0]:
                # 选择运动方向: 'Y'--沿托盘前边 / ‘X’--沿托盘侧边
                if move_direction == 'Y':
                    for row in range(nrow):
                        x = row * (box_width+box_interval)
                        # 选择每层的运动路径: 头到尾--headtail / 弓字形--zigzag
                        if pattern == 'headtail':
                            start_col, end_col, step_col = 0, ncol, 1
                        elif pattern == 'zigzag':
                            # 根据行号和顺序变量确定每行的起始点和方向
                            if row % 2 == 0:
                                start_col, end_col, step_col = 0, ncol, 1
                            else:
                                start_col, end_col, step_col = ncol-1, -1, -1
                        else:
                            raise ValueError("无效的运动路径,必须是'headtail'或'zigzag'")
                        for col in range(start_col, end_col, step_col):
                            y = col * (box_length + box_interval)
                            box_points.append[x,y,z]
                elif move_direction == 'X':
                    for col in range(ncol):
                        y = col * (box_length + box_interval)
                        if pattern == 'headtail':
                            start_row, end_row, step_row = 0, nrow, 1
                        elif pattern == 'zigzag':
                            if col % 2 == 0:
                                start_row, end_row, step_row = 0, nrow, 1
                            else:
                                start_row, end_row, step_row = nrow-1, -1, -1
                        else:
                            raise ValueError("无效的运动方式,必须是'headtail'或'zigzag'")
                        for row in range(start_row, end_row, step_row):
                            x = row * (box_width+box_interval)
                            box_points.append[x,y,z]
                else:
                    raise ValueError("无效的移动方向,必须是'X'或'Y'")

            elif first_corner == [0,1]:
                if move_direction == 'Y':
                    for row in range(nrow):
                        x = row * (box_width+box_interval)
                        if pattern == 'headtail':
                            start_col, end_col, step_col = 0, -ncol, -1
                        elif pattern == 'zigzag':
                            if row % 2 == 0:
                                start_col, end_col, step_col = 0, -ncol, -1
                            else:
                                start_col, end_col, step_col = -ncol+1, 1, 1
                        else:
                            raise ValueError("无效的运动路径,必须是'headtail'或'zigzag'")
                        for col in range(start_col, end_col, step_col):
                            y = col * (box_length + box_interval)
                            box_points.append[x,y,z]
                elif move_direction == 'X':
                    for col in range(0,-ncol,-1):
                        y = col * (box_length + box_interval)
                        if pattern == 'headtail':
                            start_row, end_row, step_row = 0, nrow, 1
                        elif pattern == 'zigzag':
                            if col % 2 == 0:
                                start_row, end_row, step_row = 0, nrow, 1
                            else:
                                start_row, end_row, step_row = nrow-1, -1, -1
                        else:
                            raise ValueError("无效的运动方式,必须是'headtail'或'zigzag'")
                        for row in range(start_row, end_row, step_row):
                            x = row * (box_width+box_interval)
                            box_points.append([x,y,z])
                else:
                    raise ValueError("无效的移动方向,必须是'X'或'Y'")

            elif first_corner == [1,0]:
                if move_direction == 'Y':
                    for row in range(0,-nrow,-1):
                        x = row * (box_width+box_interval)
                        if pattern == 'headtail':
                            start_col, end_col, step_col = 0, ncol, 1
                        elif pattern == 'zigzag':
                            if row % 2 == 0:
                                start_col, end_col, step_col = 0, ncol, 1
                            else:
                                start_col, end_col, step_col = ncol-1, -1, -1
                        else:
                            raise ValueError("无效的运动路径,必须是'headtail'或'zigzag'")
                        for col in range(start_col, end_col, step_col):
                            y = col * (box_length + box_interval)
                            box_points.append[x,y,z]
                elif move_direction == 'X':
                    for col in range(ncol):
                        y = col * (box_length + box_interval)
                        if pattern == 'headtail':
                            start_row, end_row, step_row = 0, -nrow, -1
                        elif pattern == 'zigzag':
                            if col % 2 == 0:
                                start_row, end_row, step_row = 0, -nrow, -1
                            else:
                                start_row, end_row, step_row = -nrow+1, 1, 1
                        else:
                            raise ValueError("无效的运动方式,必须是'headtail'或'zigzag'")
                        for row in range(start_row, end_row, step_row):
                            x = row * (box_width+box_interval)
                            box_points.append[x,y,z]
                else:
                    raise ValueError("无效的移动方向,必须是'X'或'Y'")

            elif first_corner == [1,1]:
                if move_direction == 'Y':
                    for row in range(0,-nrow,-1):
                        x = row * (box_width+box_interval)
                        if pattern == 'headtail':
                            start_col, end_col, step_col = 0, -ncol, -1
                        elif pattern == 'zigzag':
                            if row % 2 == 0:
                                start_col, end_col, step_col = 0, -ncol, -1
                            else:
                                start_col, end_col, step_col = -ncol+1, 1, 1
                        else:
                            raise ValueError("无效的运动路径,必须是'headtail'或'zigzag'")
                        for col in range(start_col, end_col, step_col):
                            y = col * (box_length + box_interval)
                            box_points.append[x,y,z]
                elif move_direction == 'X':
                    for col in range(0,-ncol,-1):
                        y = col * (box_length + box_interval)
                        if pattern == 'headtail':
                            start_row, end_row, step_row = 0, -nrow, -1
                        elif pattern == 'zigzag':
                            if col % 2 == 0:
                                start_row, end_row, step_row = 0, -nrow, -1
                            else:
                                start_row, end_row, step_row = -nrow+1, 1, 1
                        else:
                            raise ValueError("无效的运动方式,必须是'headtail'或'zigzag'")
                        for row in range(start_row, end_row, step_row):
                            x = row * (box_width+box_interval)
                            box_points.append[x,y,z]
                else:
                    raise ValueError("无效的移动方向,必须是'X'或'Y'")
            
            else:
                raise ValueError("无效的起始方位,必须是[0,0]/[0,1]/[1,0]/[1,1]")
        
        # 计算机器人坐标系下的目标点坐标
        target_points = [self.get_target_point(box_point, p_pallet_origin=p_path_1, suction_point=suction_point) 
                            for box_point in box_points]
        
        for target_point in target_points:
            # 机械臂移动到作业原点
            self.robot_motion(self.rbt, p_home, motion_type=motion)
            # 拿起工件
            # robot_pickup()
            # 机械臂移动到工位过渡点
            self.robot_motion(self.rbt, p_trans, motion_type=motion)
            # 移动机器人到目标点
            self.robot_motion(self.rbt, target_point, motion_type=motion)
            # 释放工件
            # robot_putdown()
            # 机械臂移动到工位过渡点
            self.robot_motion(self.rbt, p_trans, motion_type=motion)

